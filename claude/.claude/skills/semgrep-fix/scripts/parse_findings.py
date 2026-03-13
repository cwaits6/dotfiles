#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Parse semgrep JSON output into a readable summary for Claude."""

import json
import sys
from pathlib import Path


def parse(results_path: str, summary_only: bool = False) -> None:
    data = json.loads(Path(results_path).read_text())
    results = data.get("results", [])

    if not results:
        print("No findings.")
        return

    if summary_only:
        # One-liner for git commit message
        files = {r["path"] for r in results}
        print(f"{len(results)} finding(s) across {len(files)} file(s): " +
              ", ".join(sorted(r["check_id"].split(".")[-1] for r in results)))
        return

    for i, r in enumerate(results, 1):
        has_fix = "fix" in r.get("extra", {})
        lines = r["extra"].get("lines", "").strip()
        print(f"\n[{i}] {r['check_id']}")
        print(f"    File   : {r['path']}:{r['start']['line']}-{r['end']['line']}")
        print(f"    Severity: {r['extra'].get('severity', 'unknown')}")
        print(f"    Autofix: {'yes' if has_fix else 'no'}")
        print(f"    Message: {r['extra'].get('message', '').strip()}")
        if lines:
            print(f"    Code   : {lines[:120]}")
        if has_fix:
            print(f"    Fix    : {r['extra']['fix'][:120]}")

    print(f"\nTotal: {len(results)} finding(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_findings.py <semgrep-results.json> [--summary]")
        sys.exit(1)
    summary = "--summary" in sys.argv
    parse(sys.argv[1], summary_only=summary)
