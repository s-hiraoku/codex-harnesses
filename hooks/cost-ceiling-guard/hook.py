#!/usr/bin/env python3
"""Example stdin hook that caps cumulative tool calls in a rolling window."""

from __future__ import annotations

import contextlib
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_CEILING = 5000
WINDOW_SECONDS = 24 * 60 * 60
WRITE_EVERY = 10


def ledger_path() -> Path:
    override = os.environ.get("CODEX_HARNESSES_COST_PATH", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".codex-harnesses" / "cost-ledger.json"


def fresh_window() -> dict[str, int]:
    return {"window_start": int(time.time()), "count": 0}


def load_ledger(path: Path) -> dict[str, int]:
    if not path.is_file():
        return fresh_window()
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return fresh_window()
    if not isinstance(data, dict):
        return fresh_window()
    return {
        "window_start": int(data.get("window_start", int(time.time()))),
        "count": int(data.get("count", 0)),
    }


def save_ledger(path: Path, data: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def main() -> int:
    with contextlib.suppress(Exception):
        sys.stdin.read()

    ceiling_raw = os.environ.get("CODEX_HARNESSES_COST_CEILING", "").strip()
    try:
        ceiling = int(ceiling_raw) if ceiling_raw else DEFAULT_CEILING
    except ValueError:
        ceiling = DEFAULT_CEILING

    path = ledger_path()
    data = load_ledger(path)
    now = int(time.time())
    if now - data["window_start"] > WINDOW_SECONDS:
        data = fresh_window()

    data["count"] += 1
    near_ceiling = data["count"] >= ceiling - 100
    if data["count"] == 1 or data["count"] % WRITE_EVERY == 0 or near_ceiling:
        save_ledger(path, data)

    if data["count"] > ceiling:
        print(
            "blocked: cost ceiling exceeded "
            f"({data['count']} tool calls in current 24h window, ceiling {ceiling})",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
