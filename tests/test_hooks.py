from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_hook(path: str, text: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / path)],
        input=text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_secret_guard_allows_plain_text() -> None:
    result = run_hook("hooks/secret-guard/hook.py", "ordinary project notes")

    assert result.returncode == 0


def test_secret_guard_blocks_openai_style_key() -> None:
    result = run_hook("hooks/secret-guard/hook.py", "OPENAI_API_KEY=sk-123456789012345678901234")

    assert result.returncode == 2
    assert "likely secret" in result.stderr


def test_dangerous_command_guard_allows_safe_command() -> None:
    result = run_hook("hooks/dangerous-command-guard/hook.py", "git status --short")

    assert result.returncode == 0


def test_dangerous_command_guard_blocks_hard_reset() -> None:
    result = run_hook("hooks/dangerous-command-guard/hook.py", "git reset --hard")

    assert result.returncode == 2
    assert "dangerous command" in result.stderr

