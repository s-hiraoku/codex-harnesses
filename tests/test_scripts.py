from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [ROOT / "scripts/verify.sh", ROOT / "scripts/checkpoint.sh"]


def test_root_scripts_are_executable_and_valid_bash() -> None:
    for script in SCRIPTS:
        assert script.is_file(), f"{script.relative_to(ROOT)} is missing"
        assert os.access(script, os.X_OK), f"{script.relative_to(ROOT)} is not executable"
        subprocess.run(["bash", "-n", str(script)], check=True)


def test_checkpoint_appends_git_context(tmp_path: Path) -> None:
    assert shutil.which("git"), "git is required for checkpoint script"

    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", ".venv", ".pytest_cache"))
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["bash", "scripts/checkpoint.sh"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

    ledger = (repo / "ledger/current.md").read_text()
    assert "Latest commit: no commit" in ledger
    assert "Short status:" in ledger
