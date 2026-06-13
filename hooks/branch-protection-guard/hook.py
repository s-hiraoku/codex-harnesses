#!/usr/bin/env python3
"""Example stdin hook that blocks direct git writes to protected branches."""

from __future__ import annotations

import os
import re
import subprocess
import sys

PROTECTED_BRANCHES = ("main", "master", "production", "release")
PUSH_TO_PROTECTED = re.compile(
    r"\bgit\s+push\b[^\n]*\b(?:origin\s+)?(?:" + "|".join(PROTECTED_BRANCHES) + r")\b"
)
COMMIT_PATTERN = re.compile(r"\bgit\s+commit\b")


def current_branch() -> str | None:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def main() -> int:
    if os.environ.get("CODEX_HARNESSES_ALLOW_PROTECTED_BRANCH", "").strip() == "1":
        return 0

    text = sys.stdin.read()
    if not text or "git" not in text:
        return 0

    if PUSH_TO_PROTECTED.search(text):
        print("blocked: git push targets a protected branch", file=sys.stderr)
        return 2

    if COMMIT_PATTERN.search(text):
        branch = current_branch()
        if branch in PROTECTED_BRANCHES:
            print(f"blocked: git commit on protected branch {branch!r}", file=sys.stderr)
            return 2
        if branch is None:
            print(
                "blocked: git commit attempted but branch could not be determined",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
