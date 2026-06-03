from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins/codex-harnesses"
MARKETPLACE = ROOT / "marketplace.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def test_plugin_manifest_points_to_packaged_skills() -> None:
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin/plugin.json")

    assert manifest["name"] == "codex-harnesses"
    assert manifest["skills"] == "./skills/"
    assert (PLUGIN_ROOT / "skills/feature-implementation/SKILL.md").is_file()


def test_marketplace_exposes_codex_harnesses_plugin() -> None:
    marketplace = load_json(MARKETPLACE)
    plugins = marketplace["plugins"]

    assert marketplace["name"] == "codex-harnesses"
    assert isinstance(plugins, list)
    assert plugins == [
        {
            "name": "codex-harnesses",
            "source": {
                "source": "local",
                "path": "./plugins/codex-harnesses",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Developer Tools",
        }
    ]
