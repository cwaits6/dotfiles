---
name: semgrep-fix
description: Run Semgrep security scan on the current repo, parse findings, and apply fixes on a new git branch. Use when the user invokes /semgrep-fix, asks to "fix semgrep findings", "run semgrep and fix issues", wants to act on a semgrep PR comment, or wants to fix findings across multiple open PRs.
---

# Semgrep Fix

Scan the current repo (or read existing findings from a PR comment or GitHub issue) and apply fixes. Supports fixing a single PR branch or multiple PRs in parallel via git worktrees.

Always use `uv run` for Python — never call `python` or `python3` directly.

## Step 0: Detect the source of findings

Before scanning, check if findings already exist to avoid redundant work:

```bash
# Are we on a branch with an open PR that has a semgrep comment?
gh pr view --json number,headRefName,comments 2>/dev/null
```

- **Semgrep PR comment found** → parse findings from the comment using `scripts/parse_pr_comment.py` (skip the semgrep scan)
- **On main with a semgrep issue open** → use `gh issue list --label security` to find and read the issue; parse findings from it
- **No existing findings** → run a fresh scan (Step 1)

## Step 1: Fresh scan (fallback)

Only run if Step 0 found no existing findings:

```bash
uvx semgrep scan --config=auto --json --output=/tmp/semgrep-results.json 2>/dev/null
uv run scripts/parse_findings.py /tmp/semgrep-results.json
```

If `semgrep` is not installed and `uvx` fails, fall back to Docker:
```bash
docker run --rm -v "$(pwd)":/src semgrep/semgrep scan --config=auto --json --output=/tmp/semgrep-results.json /src 2>/dev/null
```

If there are **no findings**, report that and stop.

## Step 2: Single PR fix

When fixing the current branch's PR:

```bash
git checkout -b fix/semgrep-$(date +%Y%m%d)   # or commit directly to the PR branch if already on it
```

Work through findings one at a time. Batch multiple findings in the same file before moving on.

**If `fix` is present** (semgrep has a suggested replacement):
- `fix` is the exact replacement for the matched text (`extra.lines`)
- Apply it at the reported line range using the Edit tool

**If no `fix`** (most security rules — these need reasoning):
- Read the file around the reported line range for full context
- Use `extra.message` to understand what the vulnerability is
- Apply the minimal correct fix — don't refactor surrounding code
- Common patterns:
  - Hardcoded secrets → extract to env var reference
  - SQL string concat → parameterized query
  - Missing input validation → add the appropriate check
  - Insecure function → use the safer alternative named in the message

If a finding is too ambiguous to fix safely, skip it and note it in the final report.

Commit when done:
```bash
git add -p
git commit -m "fix: address semgrep security findings

$(uv run scripts/parse_findings.py /tmp/semgrep-results.json --summary)"
git push
```

## Step 3: Multi-PR fix (worktree mode)

When the user wants to fix findings across **multiple open PRs** at once:

```bash
# Find all PRs with semgrep findings comments
gh pr list --json number,headRefName,comments --limit 50
```

Parse that output to find PRs where `comments` contains a body starting with `## Semgrep findings`. For each matching PR:

```bash
# Create an isolated worktree for each PR branch
git worktree add /tmp/semgrep-fix-pr-{NUMBER} {BRANCH_NAME}
```

Fix findings in each worktree independently (use the same Step 2 logic per worktree). When done:

```bash
git -C /tmp/semgrep-fix-pr-{NUMBER} add -A
git -C /tmp/semgrep-fix-pr-{NUMBER} commit -m "fix: address semgrep security findings"
git -C /tmp/semgrep-fix-pr-{NUMBER} push origin {BRANCH_NAME}

# Clean up the worktree
git worktree remove /tmp/semgrep-fix-pr-{NUMBER}
```

After all worktrees are done, run `git worktree prune` to clean up any stale metadata.

## Step 4: Report to user

Summarize: what was fixed per PR/branch, what was skipped and why.
