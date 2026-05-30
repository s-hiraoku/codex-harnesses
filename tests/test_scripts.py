from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "scripts/verify.sh",
    ROOT / "scripts/checkpoint.sh",
    ROOT / "scripts/skills.sh",
    ROOT / "scripts/evaluate-skill.sh",
]


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


def test_skills_script_installs_named_skills(tmp_path: Path) -> None:
    target = tmp_path / "codex-skills"

    subprocess.run(
        [
            "bash",
            str(ROOT / "scripts/skills.sh"),
            "--target",
            str(target),
            "bug-fix",
            "docs-updater",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (target / "bug-fix/SKILL.md").is_file()
    assert (target / "docs-updater/SKILL.md").is_file()
    assert not (target / "review/SKILL.md").exists()


def test_evaluate_skill_script_creates_evaluation_pack(tmp_path: Path) -> None:
    output = tmp_path / "evaluations"

    result = subprocess.run(
        [
            "bash",
            str(ROOT / "scripts/evaluate-skill.sh"),
            "--output",
            str(output),
            "skills/feature-implementation",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    run_dir = Path(result.stdout.strip().removeprefix("created "))
    assert run_dir.is_dir()
    assert run_dir.parent == output / "feature-implementation"
    assert (run_dir / "README.md").is_file()
    assert (run_dir / "iteration-0-structural-review.md").is_file()
    assert (run_dir / "scenarios.md").is_file()
    assert (run_dir / "executor-prompt.md").is_file()
    assert (run_dir / "results.md").is_file()
    assert (run_dir / "failure-pattern-ledger.md").is_file()

    executor_prompt = (run_dir / "executor-prompt.md").read_text()
    scenarios = (run_dir / "scenarios.md").read_text()
    results = (run_dir / "results.md").read_text()
    assert "skills/feature-implementation/SKILL.md" in executor_prompt
    assert "○ / × / partial" in executor_prompt
    assert "Unclear points (structured)" in executor_prompt
    assert "Hold-out scenario: convergence check only" in scenarios
    assert "Hold-out scenario run:" in results


def test_evaluate_skill_script_uses_unique_run_directories(tmp_path: Path) -> None:
    output = tmp_path / "evaluations"
    command = [
        "bash",
        str(ROOT / "scripts/evaluate-skill.sh"),
        "--output",
        str(output),
        "skills/feature-implementation",
    ]

    first = subprocess.run(command, check=True, capture_output=True, text=True)
    second = subprocess.run(command, check=True, capture_output=True, text=True)

    first_dir = Path(first.stdout.strip().removeprefix("created "))
    second_dir = Path(second.stdout.strip().removeprefix("created "))
    assert first_dir != second_dir
    assert first_dir.is_dir()
    assert second_dir.is_dir()


def test_skills_script_force_skips_same_source_and_destination(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", ".venv", ".pytest_cache"))

    result = subprocess.run(
        [
            "bash",
            "scripts/skills.sh",
            "--target",
            "skills",
            "--force",
            "bug-fix",
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "skip same path" in result.stdout
    assert (repo / "skills/bug-fix/SKILL.md").is_file()
