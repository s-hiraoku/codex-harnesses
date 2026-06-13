from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "mcp/recipes/curated.mcp.json"


def test_curated_mcp_recipe_is_disabled_by_default() -> None:
    data = json.loads(RECIPE.read_text())

    assert data["mcpServers"] == {}
    assert set(data["_disabled"]) == {
        "github",
        "playwright",
        "context7",
        "serena",
        "sequential-thinking",
        "sentry",
    }


def test_curated_mcp_recipe_entries_have_commands_and_docs() -> None:
    data = json.loads(RECIPE.read_text())

    for name, config in data["_disabled"].items():
        assert config["command"], f"{name} is missing command"
        assert config["args"], f"{name} is missing args"
        assert config["_doc"].startswith("docs/mcp-recipes.md#")
