from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "adviser" / "scripts" / "route_adviser.py"
SPEC = importlib.util.spec_from_file_location("route_adviser", MODULE_PATH)
assert SPEC and SPEC.loader
route_adviser = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = route_adviser
SPEC.loader.exec_module(route_adviser)


@pytest.mark.parametrize("model", ["gpt-5.6-luna", "gpt-5.6-terra"])
@pytest.mark.parametrize("effort", ["low", "medium", "high", "xhigh", "max"])
def test_luna_and_terra_upgrade_to_sol_without_lowering_effort(model: str, effort: str) -> None:
    route = route_adviser.route_adviser(model, effort)

    assert route.adviser_model == "gpt-5.6-sol"
    assert route.adviser_effort == effort
    assert route.escalation == "model"


def test_terra_ultra_upgrades_to_sol_ultra() -> None:
    route = route_adviser.route_adviser("gpt-5.6-terra", "ultra")

    assert route.adviser_model == "gpt-5.6-sol"
    assert route.adviser_effort == "ultra"


@pytest.mark.parametrize(
    ("caller", "adviser"),
    [
        ("low", "medium"),
        ("medium", "high"),
        ("high", "xhigh"),
        ("xhigh", "max"),
        ("max", "ultra"),
    ],
)
def test_sol_uses_the_next_effort(caller: str, adviser: str) -> None:
    route = route_adviser.route_adviser("gpt-5.6-sol", caller)

    assert route.adviser_model == "gpt-5.6-sol"
    assert route.adviser_effort == adviser
    assert route.escalation == "effort"


@pytest.mark.parametrize(
    ("model", "effort"),
    [
        ("gpt-5.6-sol", "ultra"),
        ("gpt-5.6-luna", "ultra"),
        ("gpt-5.5", "high"),
        ("gpt-5.6-sol", "minimal"),
    ],
)
def test_unproven_routes_fail_closed(model: str, effort: str) -> None:
    with pytest.raises(route_adviser.RouteError):
        route_adviser.route_adviser(model, effort)


def test_reads_the_latest_turn_context_for_the_current_thread(tmp_path: Path) -> None:
    thread_id = "019f0000-0000-7000-8000-000000000000"
    rollout = (
        tmp_path
        / "sessions"
        / "2026"
        / "07"
        / "16"
        / f"rollout-2026-07-16T00-00-00-{thread_id}.jsonl"
    )
    rollout.parent.mkdir(parents=True)
    events = [
        {"type": "turn_context", "payload": {"model": "gpt-5.6-luna", "effort": "low"}},
        {"type": "event_msg", "payload": {"type": "agent_message"}},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-sol", "effort": "medium"}},
    ]
    rollout.write_text("\n".join(json.dumps(event) for event in events) + "\n")

    route = route_adviser.resolve_route(None, None, tmp_path, thread_id)

    assert route.adviser_model == "gpt-5.6-sol"
    assert route.adviser_effort == "high"


def test_requires_model_and_effort_together(tmp_path: Path) -> None:
    with pytest.raises(route_adviser.RouteError, match="supplied together"):
        route_adviser.resolve_route("gpt-5.6-sol", None, tmp_path, None)


def test_rejects_ambiguous_rollout_matches(tmp_path: Path) -> None:
    thread_id = "019f0000-0000-7000-8000-000000000000"
    active = tmp_path / "sessions" / f"rollout-active-{thread_id}.jsonl"
    archived = tmp_path / "archived_sessions" / f"rollout-archived-{thread_id}.jsonl"
    active.parent.mkdir(parents=True)
    archived.parent.mkdir(parents=True)
    active.write_text("{}\n")
    archived.write_text("{}\n")

    with pytest.raises(route_adviser.RouteError, match="ambiguous"):
        route_adviser.read_caller_context(tmp_path, thread_id)


def test_rejects_invalid_thread_id(tmp_path: Path) -> None:
    with pytest.raises(route_adviser.RouteError, match="invalid CODEX_THREAD_ID"):
        route_adviser.read_caller_context(tmp_path, "*")


def test_rejects_malformed_complete_rollout_line(tmp_path: Path) -> None:
    thread_id = "019f0000-0000-7000-8000-000000000000"
    rollout = tmp_path / "sessions" / f"rollout-invalid-{thread_id}.jsonl"
    rollout.parent.mkdir(parents=True)
    rollout.write_text("not-json\n")

    with pytest.raises(route_adviser.RouteError, match="invalid rollout JSON"):
        route_adviser.read_caller_context(tmp_path, thread_id)
