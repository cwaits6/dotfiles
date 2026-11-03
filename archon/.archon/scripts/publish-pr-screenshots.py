"""Host a PR's chosen screenshots in <repo>-pr-assets and show them on the PR.

Reads <artifacts>/pr-screenshots/manifest.json:
  {"notes": "optional text above the images",
   "shots": [{"screen": "Profile", "width": 390, "before": "a.png", "after": "b.png"}]}
`before` may be null for a new screen. Paths are relative to <artifacts>/screenshots.

Exits 0 on every path so a screenshot problem never costs the run; a failed
upload says so on the PR instead. Does nothing unless the repo is public and the
assets repo exists and is public, so private screenshots have nowhere to go.

Links are pinned to the assets commit, which a later push or cleanup cannot move.
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MAX_IMAGES = 12
START = "<!-- pr-screenshots:start -->"
END = "<!-- pr-screenshots:end -->"


def gh(*args, payload=None):
    r = subprocess.run(
        ["gh", *args],
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
    )
    if r.returncode:
        raise RuntimeError(f"gh {args[0]} {args[1] if len(args) > 1 else ''}: {r.stderr.strip()[:300]}")
    return json.loads(r.stdout) if r.stdout.strip() else None


def api(method, path, payload=None):
    args = ["api", "-X", method, path]
    return gh(*args, "--input", "-", payload=payload) if payload is not None else gh(*args)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def to_webp(src, dst):
    subprocess.run(["cwebp", "-quiet", "-q", "82", str(src), "-o", str(dst)], check=True, capture_output=True)


def commit_files(assets, pr, files):
    """One commit through the Git Data API. A parallel run moving main only fails the fast-forward."""
    blobs = [
        {
            "path": f"pr/{pr}/{name}",
            "mode": "100644",
            "type": "blob",
            "sha": api(
                "POST",
                f"repos/{assets}/git/blobs",
                {"content": base64.b64encode(data).decode(), "encoding": "base64"},
            )["sha"],
        }
        for name, data in files.items()
    ]
    for attempt in range(5):
        head = api("GET", f"repos/{assets}/git/ref/heads/main")["object"]["sha"]
        base = api("GET", f"repos/{assets}/git/commits/{head}")["tree"]["sha"]
        tree = api("POST", f"repos/{assets}/git/trees", {"base_tree": base, "tree": blobs})["sha"]
        commit = api(
            "POST",
            f"repos/{assets}/git/commits",
            {"message": f"chore: add screenshots for PR {pr}", "tree": tree, "parents": [head]},
        )["sha"]
        try:
            api("PATCH", f"repos/{assets}/git/refs/heads/main", {"sha": commit, "force": False})
            return commit
        except RuntimeError:
            if attempt == 4:
                raise
            time.sleep(2 + attempt * 3)


def table(shots, url):
    def cell(name, label):
        return f'<img src="{url(name)}" alt="{label}" width="320">' if name else "New screen"

    rows = ["| Screen | Before | After |", "| --- | --- | --- |"]
    for s in shots:
        title = f"{s['screen']}, {s['width']}"
        rows.append(
            f"| {title} | {cell(s.get('before_name'), 'Before: ' + title)} | {cell(s['after_name'], 'After: ' + title)} |"
        )
    return "\n".join(rows)


def with_section(body, content):
    """Fill the last Screenshots section, or add one above CodeRabbit's generated summary."""
    block = f"{START}\n{content}\n{END}"
    if START in body and END in body:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, body, flags=re.S)
    headings = list(re.finditer(r"^## Screenshots[ \t]*$", body, flags=re.M))
    if headings:
        start = headings[-1].end()
        stop = re.compile(r"^(## |<!-- )", flags=re.M).search(body, start)
        end = stop.start() if stop else len(body)
        return f"{body[:start]}\n\n{block}\n\n{body[end:]}"
    marker = body.find("<!-- This is an auto-generated comment: release notes by coderabbit")
    section = f"## Screenshots\n\n{block}\n\n"
    return f"{body[:marker]}{section}{body[marker:]}" if marker >= 0 else f"{body.rstrip()}\n\n{section}"


def set_body(repo, pr, content):
    body = gh("pr", "view", str(pr), "--repo", repo, "--json", "body")["body"]
    api("PATCH", f"repos/{repo}/pulls/{pr}", {"body": with_section(body, content)})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifacts", default=os.environ.get("INPUTS_ARTIFACTS") or os.environ.get("ARTIFACTS_DIR") or ".")
    p.add_argument("--pr", type=int)
    args = p.parse_args()

    root = Path(args.artifacts)
    manifest = root / "pr-screenshots" / "manifest.json"
    if not manifest.exists():
        return print(json.dumps({"state": "skipped", "reason": "no manifest"}))

    source = gh("repo", "view", "--json", "nameWithOwner,visibility")
    repo = source["nameWithOwner"]
    assets = f"{repo}-pr-assets"
    pr = args.pr or gh("pr", "view", "--json", "number")["number"]
    try:
        public = api("GET", f"repos/{assets}")["visibility"] == "public"
    except RuntimeError:
        public = False
    if source["visibility"] != "PUBLIC" or not public:
        return print(json.dumps({"state": "skipped", "reason": f"{repo} or {assets} is not a public repo"}))

    try:
        data = json.loads(manifest.read_text())
        shots = data["shots"]
        if not shots or sum(1 + bool(s.get("before")) for s in shots) > MAX_IMAGES:
            raise ValueError(f"manifest needs 1 to {MAX_IMAGES} images")
        files = {}
        base = root / "screenshots"
        with tempfile.TemporaryDirectory() as tmp:
            for s in shots:
                for side in ("before", "after"):
                    if not s.get(side):
                        continue
                    name = f"{slug(s['screen'])}-{s['width']}-{side}.webp"
                    out = Path(tmp) / name
                    to_webp(base / s[side], out)
                    files[name] = out.read_bytes()
                    s[f"{side}_name"] = name
        commit = commit_files(assets, pr, files)
        url = lambda name: f"https://raw.githubusercontent.com/{assets}/{commit}/pr/{pr}/{name}"
        notes = (data.get("notes") or "").strip()
        set_body(repo, pr, f"{notes}\n\n{table(shots, url)}" if notes else table(shots, url))
        print(json.dumps({"state": "published", "commit": commit, "images": len(files), "bytes": sum(map(len, files.values()))}))
    except Exception as e:  # noqa: BLE001 - this step must never fail the run
        print(f"publish failed: {e}", file=sys.stderr)
        try:
            set_body(repo, pr, f"The screenshot upload failed ({e}). The images are in the run's `screenshots/` directory.")
        except Exception as note_error:  # noqa: BLE001
            print(f"could not note the failure on the PR: {note_error}", file=sys.stderr)
        print(json.dumps({"state": "failed", "reason": str(e)}))


if __name__ == "__main__":
    main()
