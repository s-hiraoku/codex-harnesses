from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOP_LEVEL_KEYS = {"mode", "guards", "verification", "git"}
EXPECTED_NESTED_KEYS = {
    "mode": {"approval", "sandbox"},
    "guards": {"block_secrets", "block_dangerous_commands", "require_verification_on_stop"},
    "verification": {"require_lint", "require_typecheck", "require_tests", "require_build"},
    "git": {"allow_force_push", "allow_reset_hard", "prefer_worktree"},
}
APPROVAL_VALUES = {"on-request", "explicit", "always", "never"}
SANDBOX_VALUES = {"read-only", "workspace-write", "danger-full-access"}


def load_schema() -> dict[str, object]:
    return json.loads((ROOT / "schemas/policy.schema.json").read_text())


def policy_files() -> list[Path]:
    return sorted((ROOT / "policies").glob("*.yaml")) + sorted(
        (ROOT / "examples").glob("*/policies/*.yaml")
    )


def parse_simple_policy_yaml(path: Path) -> dict[str, dict[str, str | bool]]:
    data: dict[str, dict[str, str | bool]] = {}
    current_section: str | None = None

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if not line.startswith(" "):
            section, separator, value = line.partition(":")
            assert separator == ":", f"invalid section line in {path}: {line}"
            assert value == "", f"top-level policy sections must not have scalar values: {line}"
            current_section = section
            data[current_section] = {}
            continue

        assert current_section is not None, f"nested value without section in {path}: {line}"
        key, separator, value = line.strip().partition(":")
        assert separator == ":", f"invalid nested line in {path}: {line}"
        parsed_value: str | bool = value.strip()
        if parsed_value == "true":
            parsed_value = True
        elif parsed_value == "false":
            parsed_value = False
        data[current_section][key] = parsed_value

    return data


def test_policy_schema_matches_expected_contract() -> None:
    schema = load_schema()

    assert schema["type"] == "object"
    assert set(schema["required"]) == EXPECTED_TOP_LEVEL_KEYS
    assert schema["additionalProperties"] is False

    properties = schema["properties"]
    assert set(properties) == EXPECTED_TOP_LEVEL_KEYS

    for section, expected_keys in EXPECTED_NESTED_KEYS.items():
        section_schema = properties[section]
        assert section_schema["type"] == "object"
        assert set(section_schema["required"]) == expected_keys
        assert section_schema["additionalProperties"] is False
        assert set(section_schema["properties"]) == expected_keys


def test_policy_examples_match_schema_contract() -> None:
    paths = policy_files()
    assert paths, "expected at least one policy example"

    for path in paths:
        policy = parse_simple_policy_yaml(path)
        assert set(policy) == EXPECTED_TOP_LEVEL_KEYS
        assert set(policy["mode"]) == EXPECTED_NESTED_KEYS["mode"]
        assert policy["mode"]["approval"] in APPROVAL_VALUES
        assert policy["mode"]["sandbox"] in SANDBOX_VALUES

        for section in ("guards", "verification", "git"):
            assert set(policy[section]) == EXPECTED_NESTED_KEYS[section]
            for value in policy[section].values():
                assert isinstance(value, bool), f"{path.relative_to(ROOT)} has non-boolean value"


def test_policy_schema_json_is_valid() -> None:
    schema = load_schema()
    paths = policy_files()

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"].endswith("/schemas/policy.schema.json")
    assert paths
