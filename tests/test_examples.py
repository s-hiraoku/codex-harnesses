from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def example_dirs() -> list[Path]:
    return sorted(path for path in EXAMPLES.iterdir() if path.is_dir())


def test_examples_have_readme_and_agents_guidance() -> None:
    paths = example_dirs()

    assert paths, "expected at least one example"
    for path in paths:
        assert (path / "README.md").is_file(), f"{path.name} is missing README.md"
        assert (path / "AGENTS.md").is_file(), f"{path.name} is missing AGENTS.md"


def test_example_verify_scripts_are_executable_and_valid_bash() -> None:
    scripts = sorted(EXAMPLES.glob("*/scripts/verify.sh"))

    assert scripts, "expected at least one example verification script"
    for script in scripts:
        assert os.access(script, os.X_OK), f"{script.relative_to(ROOT)} is not executable"
        subprocess.run(["bash", "-n", str(script)], check=True)


def test_nextjs_example_contains_policy_and_verify_script() -> None:
    nextjs = EXAMPLES / "nextjs-project"

    assert (nextjs / "policies/default.yaml").is_file()
    assert (nextjs / "scripts/verify.sh").is_file()

