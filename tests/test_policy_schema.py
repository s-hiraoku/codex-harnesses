from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_schema() -> dict[str, object]:
    return json.loads((ROOT / "schemas/policy.schema.json").read_text())


def load_policy(path: Path) -> object:
    return yaml.safe_load(path.read_text())


def policy_files() -> list[Path]:
    return sorted((ROOT / "policies").glob("*.yaml")) + sorted(
        (ROOT / "examples").glob("*/policies/*.yaml")
    )


def test_policy_schema_is_valid_json_schema() -> None:
    schema = load_schema()

    jsonschema.Draft202012Validator.check_schema(schema)


def test_policy_examples_validate_against_schema() -> None:
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    paths = policy_files()

    assert paths, "expected at least one policy example"
    for path in paths:
        errors = sorted(validator.iter_errors(load_policy(path)), key=lambda error: error.path)
        assert not errors, f"{path.relative_to(ROOT)} failed schema validation: {errors}"


def test_all_policy_examples_are_discovered() -> None:
    paths = policy_files()

    assert {path.name for path in paths} >= {"default.yaml", "strict.yaml", "experimental.yaml"}
    assert ROOT / "examples/strict-repo/policies/strict.yaml" in paths
    assert ROOT / "examples/nextjs-project/policies/default.yaml" in paths
