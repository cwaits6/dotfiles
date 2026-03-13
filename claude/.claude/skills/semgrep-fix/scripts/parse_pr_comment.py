#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Parse semgrep findings from a GitHub PR comment posted by the CI workflow.

Usage:
  parse_pr_comment.py <pr-number>          # auto-detects repo from git remote
  parse_pr_comment.py <pr-number> <repo>   # explicit owner/repo

Outputs findings in the same format as parse_findings.py so the skill
workflow is identical regardless of source.

Requires: gh CLI authenticated
"""

import json
import re
import subprocess
import sys


SEMGREP_HEADER = "## Semgrep findings requiring manual fixes"


def get_pr_comments(pr_number: str, repo: str | None = None) -> list[dict]:
    cmd = ["gh", "pr", "view", pr_number, "--json", "comments"]
    if repo:
        cmd += ["--repo", repo]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching PR: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout).get("comments", [])


def parse_comment(body: str) -> list[dict]:
    """Extract structured findings from the semgrep PR comment markdown."""
    findings = []
    # Each finding line looks like:
    # - **rule.id** — `path/file.js:42`
    #   Message text
    pattern = re.compile(
        r"-\s+\*\*(.+?)\*\*\s+—\s+`([^:]+):(\d+)`\s*\n\s+(.+)"
    )
    for m in pattern.finditer(body):
        findings.append({
            "rule": m.group(1),
            "path": m.group(2),
            "line": int(m.group(3)),
            "message": m.group(4).strip(),
        })
    return findings


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_pr_comment.py <pr-number> [owner/repo]")
        sys.exit(1)

    pr_number = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else None

    comments = get_pr_comments(pr_number, repo)
    semgrep_comment = next(
        (c for c in comments if SEMGREP_HEADER in c.get("body", "")), None
    )

    if not semgrep_comment:
        print("No semgrep findings comment found on this PR.")
        sys.exit(0)

    findings = parse_comment(semgrep_comment["body"])
    if not findings:
        print("Semgrep comment found but no parseable findings.")
        sys.exit(0)

    for i, f in enumerate(findings, 1):
        print(f"\n[{i}] {f['rule']}")
        print(f"    File   : {f['path']}:{f['line']}")
        print(f"    Message: {f['message']}")

    print(f"\nTotal: {len(findings)} finding(s) requiring manual fixes")


if __name__ == "__main__":
    main()
