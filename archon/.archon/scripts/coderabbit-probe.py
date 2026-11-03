"""Classify the current branch PR's CodeRabbit + CI state, once.

Single-shot probe inside the `coderabbit` loop_group of ship-coderabbit. The
engine's `wait:` node owns the time between probes; this script reads state,
declares it, and exits 0 on every path so a flaky read costs one wait, not the run.

States, on stdout as JSON and mirrored to $ARTIFACTS/coderabbit/state (the
loop's until_bash reads the file, never this node's output — a resumed wait
does not re-substitute node outputs):
  waiting     CodeRabbit has not reviewed the head yet, or CI is still running.
              `wait` says how: "hold" + hold_s when a rate-limit notice names
              when reviews replenish (the hold node sleeps exactly that long),
              "short" otherwise (the 5-minute durable wait)
  actionable  unresolved CodeRabbit threads, unaddressed CodeRabbit reviews
              (nitpicks live in the review body, not in threads), or red CI
  done        head reviewed — by CodeRabbit on the PR, or, after the PR's one
              review, by a clean local CLI re-review — nothing unresolved or
              unaddressed, CI green
  skipped     CodeRabbit skipped the head because path filters exclude every
              changed file; nothing unresolved, CI green. It will never review it.
  blocked     the fix agent wrote coderabbit/blocked.md — a decision for a person

Every `@coderabbitai review` request goes through one PR-review slot shared by
all runs on this machine (CodeRabbit runs one PR review at a time per account,
and its rate limit is account-wide). A run requests only while it holds the
slot, in the order runs asked for it, and only when no open PR in the repo
carries a rate-limit notice whose stated wait has not passed. The slot is freed
once the head is reviewed or skipped, the run stops, its PR is rate limited, or
it goes stale.

"Head reviewed" is read from CodeRabbit's summary comment (the hidden
coveredCommitId marker, or the older "between <sha> and <sha>" range), or from a
CodeRabbit review object on the head. A missing review object proves nothing
(clean incremental reviews submit none), nor does a zero inline-comment count.
A rate-limit notice renders like a review, so it is detected by phrase — and it
replaces the summary while still quoting the "between <sha> and <head>" range,
so a rate-limited summary's range is not proof of a review.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BOT = "coderabbitai[bot]"
RANGE = re.compile(r"between ([0-9a-f]{40}) and ([0-9a-f]{40})", re.I)
COVERED = re.compile(r'"coveredCommitId":"([0-9a-f]{40})","kind":"reviewed"', re.I)
RATE_LIMIT = re.compile(r"review limit reached|rate limit(ed)? exceeded|fair usage", re.I)
# Hidden markers CodeRabbit puts on the summary comment when it rewrites it as a
# notice instead of a review.
RATE_LIMITED_SUMMARY = re.compile(r"auto-generated comment: rate limited by coderabbit\.ai", re.I)
PATH_FILTER_SKIP = re.compile(r"auto-generated comment: skip review by coderabbit\.ai.*?skipped due to path filters", re.I | re.S)
# Read only the text just after the rate-limit phrase: the same comment can carry
# "Estimated code review effort ... ~120 minutes", which is not a wait.
WAIT_MINUTES = re.compile(r"(\d+)\s*\**\s*minutes?", re.I)
WAIT_SECONDS = re.compile(r"(\d+)\s*\**\s*seconds?", re.I)
# The hold node sleeps in-process, so one hold never outlasts its node timeout.
MAX_HOLD_S = 60 * 60
# Findings that live only in a review's body. Inline findings are tracked by their
# threads, so a review without these sections needs nothing beyond its threads.
BODY_FINDINGS = re.compile(r"(nitpick|outside diff range|duplicate) comments?\s*\(\d+\)", re.I)
PROCESSING = re.compile(r"currently processing|review in progress", re.I)
# A head CodeRabbit has neither reviewed nor flagged after this long gets one
# `@coderabbitai review` nudge.
NUDGE_AFTER_S = 20 * 60

ART = Path(os.environ.get("INPUTS_ARTIFACTS") or os.environ.get("ARTIFACTS_DIR") or ".") / "coderabbit"

# Shared by every run, so it lives outside the per-run artifact store.
LOCKS = Path(os.environ.get("CODERABBIT_LOCKS") or Path.home() / ".archon" / "locks" / "coderabbit")
SLOT = LOCKS / "slot"  # a directory: mkdir is the atomic acquire
QUEUE = LOCKS / "queue"
# A slot whose review never arrived is taken over after this long.
SLOT_STALE_S = 40 * 60
QUEUE_STALE_S = 3 * 60 * 60
# Essentials refill rate by CodeRabbit PR reviews in the trailing 7 days.
TIERS = [(60, 1), (50, 2), (40, 3), (30, 4), (0, 5)]
# One run takes one PR through the loop, so the run id is the slot key.
ME = ART.parent.name if ART.parent.name not in ("", ".") else ""


def notice_ready_at(body: str, updated_at: str) -> float | None:
    """When a rate-limit notice says reviews replenish, or None if it names no wait."""
    hit = RATE_LIMIT.search(body)
    if not hit:
        return None
    window = body[hit.start():hit.start() + 600]
    m = WAIT_MINUTES.search(window)
    sec = WAIT_SECONDS.search(window)
    if not m and not sec:
        return None
    stated = (int(m.group(1)) * 60 if m else 0) + (int(sec.group(1)) if sec else 0)
    return parse_ts(updated_at) + stated + 60


def account_ready_at(owner_repo: str) -> float:
    """Latest replenish time stated by any open PR's rate-limit notice."""
    ready = 0.0
    for p in gh_json("pr", "list", "--state", "open", "--json", "number"):
        pages = gh_json("api", "--paginate", "--slurp", f"repos/{owner_repo}/issues/{p['number']}/comments")
        for c in (c for page in pages for c in page):
            if c["user"]["login"] == BOT:
                at = notice_ready_at(c["body"], c["updated_at"])
                if at:
                    ready = max(ready, at)
    return ready


def tier_estimate(owner_repo: str) -> dict:
    """CodeRabbit PR reviews seen in the last 7 days, and the refill rate that implies.

    A lower bound: a clean incremental review submits no review object. Cached,
    since every run's probe would otherwise repeat the search.
    """
    cache = LOCKS / "tier.json"
    try:
        cached = json.loads(cache.read_text())
        if time.time() - cached["at"] < 30 * 60:
            return cached
    except (OSError, ValueError, KeyError):
        pass
    since = time.time() - 7 * 86400
    day = datetime.fromtimestamp(since, timezone.utc).strftime("%Y-%m-%d")
    nodes = gh_json(
        "api", "graphql", "-F", f"q=repo:{owner_repo} is:pr updated:>={day}",
        "-f", "query=query($q:String!){search(query:$q,type:ISSUE,first:100){nodes{... on PullRequest"
              "{reviews(last:100){nodes{author{login} submittedAt}}}}}}",
    )["data"]["search"]["nodes"]
    seen = sum(
        1 for n in nodes for r in (n.get("reviews") or {}).get("nodes", [])
        if (r.get("author") or {}).get("login") == "coderabbitai"
        and r["submittedAt"] and parse_ts(r["submittedAt"]) >= since
    )
    out = {"at": time.time(), "reviews_7d_seen": seen, "per_hour": next(rate for floor, rate in TIERS if seen >= floor)}
    LOCKS.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out))
    return out


def slot_owner() -> dict | None:
    try:
        return json.loads((SLOT / "owner.json").read_text())
    except (OSError, ValueError):
        return None


def release_slot() -> None:
    if not ME:
        return
    owner = slot_owner()
    if owner and owner.get("key") == ME:
        shutil.rmtree(SLOT, ignore_errors=True)
    (QUEUE / queue_name(ME)).unlink(missing_ok=True)


def queue_name(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", key)


def take_slot(label: str) -> tuple[bool, str]:
    """Hold the shared slot for ME, in arrival order. Returns (held, why not)."""
    now = time.time()
    QUEUE.mkdir(parents=True, exist_ok=True)
    mine = QUEUE / queue_name(ME)
    if not mine.exists():
        mine.write_text(json.dumps({"at": now, "label": label}))
    owner = slot_owner()
    if owner and owner.get("key") == ME:
        return True, ""
    if SLOT.exists():
        age = now - (owner["at"] if owner else SLOT.stat().st_mtime)
        if age < SLOT_STALE_S:
            who = owner.get("label", "another run") if owner else "another run"
            return False, f"PR review slot held by {who} for {int(age // 60)} min"
        shutil.rmtree(SLOT, ignore_errors=True)
    waiting = []
    for q in QUEUE.iterdir():
        try:
            at = json.loads(q.read_text())["at"]
        except (OSError, ValueError, KeyError):
            at = q.stat().st_mtime
        if now - at > QUEUE_STALE_S:
            q.unlink(missing_ok=True)
        else:
            waiting.append((at, q.name))
    first = min(waiting, default=(now, mine.name))
    if first[1] != mine.name:
        return False, "queued for the PR review slot"
    try:
        SLOT.mkdir(parents=True)
    except FileExistsError:
        return False, "PR review slot was just taken"
    (SLOT / "owner.json").write_text(json.dumps({"key": ME, "label": label, "run": ART.parent.name, "at": now}))
    mine.unlink(missing_ok=True)
    return True, ""


def request_review(number: int, owner_repo: str) -> tuple[str, int]:
    """Post `@coderabbitai review` if the account and the slot allow it.

    Returns (outcome, hold_s): "requested", "queued" (short wait), or "held"
    with the seconds until the account's stated replenish time.
    """
    ready = account_ready_at(owner_repo)
    now = time.time()
    if ready > now:
        return "held", int(min(ready - now, MAX_HOLD_S))
    held, why = take_slot(f"#{number}")
    if not held:
        return f"queued: {why}", 0
    gh("pr", "comment", str(number), "--body", "@coderabbitai review")
    return "requested", 0


def gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if proc.returncode != 0 and not proc.stdout:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {proc.stderr.strip()[:300]}")
    return proc.stdout


def gh_json(*args: str):
    return json.loads(gh(*args))


def declare(state: str, **detail) -> int:
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "state").write_text(state + "\n")
    if state in ("done", "skipped", "blocked"):
        release_slot()
    # Every key a downstream `when:` reads must be present, or the engine fails the node.
    print(json.dumps({"state": state, "wait": "", "hold_s": 0, **detail}))
    return 0


def parse_ts(s: str) -> float:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def main() -> int:
    if (ART / "blocked.md").exists():
        return declare("blocked", detail=(ART / "blocked.md").read_text()[:2000])

    try:
        pr = gh_json("pr", "view", "--json", "number,headRefOid,isDraft,commits")
        number, head = pr["number"], pr["headRefOid"]
        owner_repo = gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").strip()
        owner, repo = owner_repo.split("/")
        comments = gh_json("api", "--paginate", "--slurp", f"repos/{owner_repo}/issues/{number}/comments")
        comments = [c for page in comments for c in page]
        reviews = gh_json("api", "--paginate", "--slurp", f"repos/{owner_repo}/pulls/{number}/reviews")
        reviews = [r for page in reviews for r in page]
        threads = gh_json(
            "api", "graphql",
            "-F", f"owner={owner}", "-F", f"repo={repo}", "-F", f"n={number}",
            "-f", "query=query($owner:String!,$repo:String!,$n:Int!){repository(owner:$owner,name:$repo)"
                  "{pullRequest(number:$n){reviewThreads(first:100){nodes{id isResolved isOutdated path line "
                  "comments(first:1){nodes{author{login} url body}}}}}}}",
        )["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
        checks_proc = subprocess.run(["gh", "pr", "checks", "--json", "name,bucket"], capture_output=True, text=True)
        checks = json.loads(checks_proc.stdout) if checks_proc.stdout.strip() else []
    except (RuntimeError, json.JSONDecodeError, KeyError, ValueError) as err:
        return declare("waiting", wait="short", detail=f"state read failed, retrying next round: {err}")

    if pr["isDraft"]:
        return declare("blocked", detail="PR is still a draft; the delivery tail did not mark it ready.")

    bot_comments = [c for c in comments if c["user"]["login"] == BOT]
    summary = bot_comments[0]["body"] if bot_comments else ""
    summary_is_notice = bool(RATE_LIMITED_SUMMARY.search(summary))
    ranges = [] if summary_is_notice else RANGE.findall(summary)
    covered = [] if summary_is_notice else [c.lower() for c in COVERED.findall(summary)]
    covered += [end.lower() for _, end in ranges]
    # The skip notice names the commit it judged; an older head's skip says nothing
    # about this one.
    path_skipped = bool(PATH_FILTER_SKIP.search(summary)) and f"/commit/{head.lower()}" in summary.lower()
    # A review object on the head is proof; its absence is not (clean incremental
    # reviews submit none).
    reviewed_head = head.lower() in covered or any(
        r["user"]["login"] == BOT and r["commit_id"] == head for r in reviews
    )
    # The PR gets one CodeRabbit review; later fix commits are vouched for by a
    # clean local CLI re-review (the fix node writes the marker), not another PR
    # review. The pr-reviewed marker survives a later notice replacing the summary.
    if reviewed_head:
        ART.mkdir(parents=True, exist_ok=True)
        (ART / "pr-reviewed").touch()
    pr_reviewed_once = bool(covered) or (ART / "pr-reviewed").exists() or any(
        r["user"]["login"] == BOT for r in reviews
    )
    local_reviewed = (ART / f"local-reviewed-{head}").exists()
    head_ok = reviewed_head or (pr_reviewed_once and local_reviewed)
    processing = bool(PROCESSING.search(summary))

    latest_notice = next((c for c in reversed(bot_comments) if RATE_LIMIT.search(c["body"])), None)
    rate_limited = (not head_ok) and latest_notice is not None and (
        not reviews or parse_ts(latest_notice["updated_at"]) >= parse_ts(reviews[-1]["submitted_at"] or "1970-01-01T00:00:00Z")
    )

    unresolved = [
        {"thread_id": t["id"], "path": t["path"], "line": t["line"], "url": t["comments"]["nodes"][0]["url"]}
        for t in threads
        if not t["isResolved"] and t["comments"]["nodes"] and t["comments"]["nodes"][0]["author"]
        and t["comments"]["nodes"][0]["author"]["login"] in ("coderabbitai", BOT)
    ]
    addressed_file = ART / "addressed-reviews.txt"
    addressed = set(addressed_file.read_text().split()) if addressed_file.exists() else set()
    unaddressed = [
        {"review_id": r["id"], "commit": r["commit_id"], "url": r["html_url"]}
        for r in reviews
        if r["user"]["login"] == BOT and str(r["id"]) not in addressed and BODY_FINDINGS.search(r.get("body") or "")
    ]
    ci_pending = [c["name"] for c in checks if c["bucket"] == "pending"]
    ci_red = [f"{c['name']} ({c['bucket']})" for c in checks if c["bucket"] not in ("pass", "skipping", "pending")]

    # A review that landed, or a skip, frees the slot for the next run.
    if head_ok or path_skipped:
        release_slot()
    want_review = (ART / "want-review").exists()
    nudged = None
    slot = ""
    hold_s = 0
    if not head_ok and not processing and not path_skipped:
        now = time.time()
        nudge_marker = ART / f"nudged-{head}"
        due = None
        if rate_limited:
            # The limit is account-wide: holding the slot through the wait would
            # only stall runs that could otherwise be queued behind it.
            release_slot()
            ready_at = notice_ready_at(latest_notice["body"], latest_notice["updated_at"]) or (
                parse_ts(latest_notice["updated_at"]) + 31 * 60
            )
            notice_marker = ART / f"nudged-notice-{latest_notice['id']}-{int(parse_ts(latest_notice['updated_at']))}"
            if now >= ready_at and not notice_marker.exists():
                due = (notice_marker, "rate limit window passed")
            elif now < ready_at:
                hold_s = int(min(ready_at - now, MAX_HOLD_S))
        elif not nudge_marker.exists():
            pushed = max((parse_ts(c["committedDate"]) for c in pr["commits"] if c["oid"] == head), default=now)
            # After the one PR review, nothing reviews a fix push on its own, so a
            # head the local CLI could not vouch for gets a PR review at once.
            if pr_reviewed_once:
                due = (nudge_marker, "fix head not re-reviewed locally")
            elif want_review:
                due = (nudge_marker, "held review requested")
            elif now - pushed >= NUDGE_AFTER_S:
                due = (nudge_marker, "head unreviewed for 20 minutes")
        if due:
            try:
                outcome, wait_s = request_review(number, owner_repo)
            except (RuntimeError, json.JSONDecodeError, KeyError, ValueError, OSError) as err:
                outcome, wait_s = f"queued: gate read failed, retrying next round: {str(err)[:200]}", 0
            if outcome == "requested":
                ART.mkdir(parents=True, exist_ok=True)
                due[0].touch()
                nudged = due[1]
            elif outcome == "held":
                hold_s = wait_s
                slot = "another PR's rate-limit notice has not expired"
            else:
                slot = outcome

    try:
        tier = tier_estimate(owner_repo)
    except (RuntimeError, json.JSONDecodeError, KeyError, ValueError, TypeError) as err:
        tier = {"error": str(err)[:200]}
    owner = slot_owner()

    detail = {
        "pr": number,
        "head": head,
        "reviewed_head": reviewed_head,
        "local_reviewed": local_reviewed,
        "rate_limited": rate_limited,
        "path_skipped": path_skipped,
        "processing": processing,
        "nudged": nudged,
        "slot": slot or ("held by this run" if owner and owner.get("key") == ME else ""),
        "slot_owner": owner.get("label") if owner else None,
        "tier": {k: v for k, v in tier.items() if k != "at"},
        "unresolved_threads": unresolved,
        "unaddressed_reviews": unaddressed,
        "ci_red": ci_red,
        "ci_pending": ci_pending,
    }
    findings = bool(unresolved or unaddressed)
    if ci_red or (findings and (head_ok or rate_limited)):
        return declare("actionable", wait="none", **detail)
    if head_ok and not findings and not ci_pending and checks:
        return declare("done", wait="none", **detail)
    if path_skipped and not findings and not ci_pending and checks:
        return declare("skipped", wait="none", **detail)
    if hold_s:
        return declare("waiting", wait="hold", hold_s=hold_s, **detail)
    return declare("waiting", wait="short", **detail)


if __name__ == "__main__":
    sys.exit(main())
