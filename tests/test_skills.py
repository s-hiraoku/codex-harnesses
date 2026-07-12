from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REQUIRED_SKILL_NAMES = {
    "adviser",
    "feature-implementation",
    "frontend-design",
    "implement-to-merge-ready",
    "jina-read-url",
    "jina-reader",
    "kaizen-loop",
    "goal-manager",
    "ui-imagegen-director",
    "bug-fix",
    "refactor-safely",
    "release-check",
    "docs-updater",
    "review",
    "pr-guardian",
    "empirical-prompt-tuning",
    "meta-packager",
    "retrospective-codify",
    "security-review",
    "tdd",
    "simplify",
    "deslop",
    "fix-ci",
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


def test_pr_guardian_waits_for_current_head_review_stabilization() -> None:
    text = (SKILLS / "pr-guardian" / "SKILL.md").read_text()

    assert "review `commit.oid` equals the pinned head SHA" in text
    assert "discard all earlier review-completion and quiet-period evidence" in text
    assert "fetch the head SHA, checks, merge state, review decision, comments, reviews, and all review threads twice" in text
    assert "A rate limit, timeout, or missing current-head terminal review is `pending external review`" in text
