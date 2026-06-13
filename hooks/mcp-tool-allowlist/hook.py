#!/usr/bin/env python3
"""Example stdin hook that enforces an MCP tool allowlist.

Input may be a raw tool name or a JSON object containing `tool_name`.
"""

from __future__ import annotations

import fnmatch
import json
import os
import sys


def parse_tool_name(raw: str) -> str:
    text = raw.strip()
    if not text:
        return ""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(payload, dict) and isinstance(payload.get("tool_name"), str):
        return payload["tool_name"]
    return ""


def parse_allowlist() -> list[str]:
    raw = os.environ.get("CODEX_HARNESSES_MCP_ALLOW", "").strip()
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> int:
    tool_name = parse_tool_name(sys.stdin.read())
    if not tool_name.startswith("mcp__"):
        return 0

    allowlist = parse_allowlist()
    if not allowlist:
        print(
            f"blocked: MCP tool {tool_name!r} called without CODEX_HARNESSES_MCP_ALLOW",
            file=sys.stderr,
        )
        return 2

    if any(fnmatch.fnmatch(tool_name, pattern) for pattern in allowlist):
        return 0

    print(f"blocked: MCP tool {tool_name!r} is not in CODEX_HARNESSES_MCP_ALLOW", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
