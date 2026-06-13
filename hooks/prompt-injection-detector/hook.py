#!/usr/bin/env python3
"""Example stdin hook that flags common prompt-injection phrases."""

from __future__ import annotations

import re
import sys

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "ignore previous instructions",
        re.compile(r"(?i)ignore (?:all )?(?:previous|prior|above) (?:instructions|prompts)"),
    ),
    ("disregard system prompt", re.compile(r"(?i)disregard (?:the )?system prompt")),
    (
        "you are now unrestricted",
        re.compile(r"(?i)you are now (?:a |an )?(?:DAN|jailbroken|unrestricted)"),
    ),
    ("developer mode", re.compile(r"(?i)\benable developer mode\b")),
    ("reveal system prompt", re.compile(r"(?i)(?:print|reveal|show) (?:the )?system prompt")),
]


def find_prompt_injection(text: str) -> str | None:
    for label, pattern in PATTERNS:
        if pattern.search(text):
            return label
    return None


def main() -> int:
    text = sys.stdin.read()
    reason = find_prompt_injection(text)
    if reason:
        print(f"blocked: suspected prompt injection ({reason})", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
