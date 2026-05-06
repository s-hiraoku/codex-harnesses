from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REQUIRED_SKILL_NAMES = {
    "feature-implementation",
    "goal-manager",
    "bug-fix",
    "refactor-safely",
    "release-check",
    "docs-updater",
    "review",
}


def skill_files() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md"))


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    assert lines and lines[0] == "---", "skill frontmatter must start with ---"
    assert "---" in lines[1:], "skill frontmatter must end with ---"
    end_index = lines[1:].index("---") + 1
    entries: dict[str, str] = {}

    for line in lines[1:end_index]:
        key, separator, value = line.partition(":")
        assert separator == ":", f"invalid frontmatter line: {line}"
        entries[key.strip()] = value.strip()

    return entries


def test_required_skills_exist() -> None:
    names = {path.parent.name for path in skill_files()}

    assert names == REQUIRED_SKILL_NAMES


def test_skills_have_name_and_description_frontmatter() -> None:
    for path in skill_files():
        frontmatter = parse_frontmatter(path.read_text())

        assert frontmatter["name"] == path.parent.name
        assert frontmatter["description"]


def test_skills_contain_workflow_and_final_report() -> None:
    for path in skill_files():
        text = path.read_text()

        assert "## Workflow" in text
        assert "## Final Report" in text
