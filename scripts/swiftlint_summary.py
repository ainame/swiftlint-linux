#!/usr/bin/env python3
"""Summarize SwiftLint JSON output for GitHub Actions.

The script is intentionally dependency-free so it can run on the
preinstalled Python 3 runtime provided by GitHub's Ubuntu images.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List


def load_report(path: str) -> List[Dict[str, Any]]:
    # SwiftLint writes an array of violation records; missing files or
    # malformed JSON should not break the workflow, so we fail softly.
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        print(f"SwiftLint JSON report not found at {path!r}", file=sys.stderr)
        return []
    except json.JSONDecodeError as error:
        print(f"Failed to parse SwiftLint report: {error}", file=sys.stderr)
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def build_summary(violations: List[Dict[str, Any]]) -> str:
    if not violations:
        # Emit a human-friendly message rather than an empty string so
        # the summary remains informative when no issues are found.
        return "No SwiftLint violations found."
    lines: List[str] = []
    for violation in violations[:10]:
        file_path = str(violation.get("file", "(unknown file)"))
        line = violation.get("line", 0) or 0
        severity = violation.get("severity", "warning")
        rule = violation.get("rule_id") or violation.get("type") or "unknown-rule"
        reason = violation.get("reason") or "No description provided."
        lines.append(f"{file_path}:{line}: [{severity}] {rule} - {reason}")
    remaining = len(violations) - len(lines)
    if remaining > 0:
        lines.append(f"+ {remaining} more violation(s)...")
    return "\n".join(lines)


def write_outputs(summary: str, issue_count: int) -> None:
    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        return
    with open(github_output, "a", encoding="utf-8") as handle:
        handle.write("lint-report<<EOF\n")
        handle.write(f"{summary}\n")
        handle.write("EOF\n")
        handle.write(f"issue-count={issue_count}\n")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: swiftlint_summary.py <path-to-json>", file=sys.stderr)
        return 1
    json_path = sys.argv[1]
    violations = load_report(json_path)
    summary = build_summary(violations)
    issue_count = len(violations)
    print(summary)
    print(f"Total violations: {issue_count}")
    write_outputs(summary, issue_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
