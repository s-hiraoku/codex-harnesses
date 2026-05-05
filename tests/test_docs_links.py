from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_PATHS = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def local_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        links.append(target)
    return links


def test_docs_local_markdown_links_resolve() -> None:
    for path in DOC_PATHS:
        for target in local_markdown_links(path.read_text()):
            resolved = (path.parent / target).resolve()
            assert resolved.exists(), f"{path.relative_to(ROOT)} links to missing {target}"

