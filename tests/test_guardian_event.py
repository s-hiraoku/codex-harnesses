from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "pr-guardian" / "scripts" / "validate_guardian_event.py"
SPEC = importlib.util.spec_from_file_location("validate_guardian_event", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def event(kind: str = "actionable") -> dict[str, Any]:
    return {
        "schema_version": 1,
        "event": kind,
        "job_id": "owner-repo-pr-50",
        "sequence": 2,
        "repo": "owner/repo",
        "pr": 50,
        "head_sha": "a" * 40,
        "observed_at": "2026-08-14T00:00:00Z",
        "reason": "required check failed",
        "delta": {"checks": [], "reviews": [], "threads": []},
        "gate": {
            "is_draft": False,
            "mergeable": "MERGEABLE",
            "merge_state_status": "BLOCKED",
            "review_decision": None,
            "required_checks_passed": False,
            "expected_reviews_current": False,
            "unresolved_thread_count": 0,
            "actionable_comment_count": 1,
            "stabilized": False,
        },
        "evidence": {
            "pagination_complete": True,
            "review_evidence_complete_at": "2026-08-13T23:58:00Z",
            "expected_reviews": [],
            "required_checks": [],
            "unresolved_threads": [],
            "actionable_comments": [],
            "stabilization_snapshots": [],
        },
        "telemetry": {
            "cycles": 4,
            "head_resets": 1,
            "github_requests": {"total": 24, "graphql": 8, "rest": 16},
            "started_at": "2026-08-13T23:55:00Z",
            "finished_at": "2026-08-14T00:00:00Z",
            "passive_wait_ms": 240000,
            "active_runner_ms": 60000,
        },
    }


def test_accepts_actionable_event_with_poll_telemetry() -> None:
    candidate = event()

    assert MODULE.validate_event(candidate) is candidate


def test_merge_ready_requires_every_preserved_gate() -> None:
    candidate = event("merge_ready")
    candidate["gate"].update(
        {
            "merge_state_status": "CLEAN",
            "required_checks_passed": True,
            "expected_reviews_current": True,
            "actionable_comment_count": 0,
            "stabilized": True,
        }
    )
    candidate["evidence"]["stabilization_snapshots"] = [
        {
            "head_sha": candidate["head_sha"],
            "activity_fingerprint": "stable",
            "observed_at": "2026-08-13T23:59:00Z",
        },
        {
            "head_sha": candidate["head_sha"],
            "activity_fingerprint": "stable",
            "observed_at": "2026-08-13T23:59:30Z",
        },
    ]

    assert MODULE.validate_event(candidate) is candidate

    candidate["gate"]["expected_reviews_current"] = False
    with pytest.raises(ValueError, match="current-head review evidence"):
        MODULE.validate_event(candidate)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("is_draft", True, "non-draft"),
        ("merge_state_status", "BLOCKED", "clean merge state"),
        ("review_decision", "CHANGES_REQUESTED", "requested changes"),
        ("unresolved_thread_count", 1, "zero unresolved threads"),
        ("actionable_comment_count", 1, "zero undisposed actionable comments"),
    ],
)
def test_merge_ready_rejects_other_blocked_gates(
    field: str, value: Any, message: str
) -> None:
    candidate = event("merge_ready")
    candidate["gate"].update(
        {
            "merge_state_status": "CLEAN",
            "required_checks_passed": True,
            "expected_reviews_current": True,
            "actionable_comment_count": 0,
            "stabilized": True,
            field: value,
        }
    )
    candidate["evidence"]["stabilization_snapshots"] = [
        {
            "head_sha": candidate["head_sha"],
            "activity_fingerprint": "stable",
            "observed_at": "2026-08-13T23:59:00Z",
        },
        {
            "head_sha": candidate["head_sha"],
            "activity_fingerprint": "stable",
            "observed_at": "2026-08-13T23:59:30Z",
        },
    ]

    with pytest.raises(ValueError, match=message):
        MODULE.validate_event(candidate)


def test_rejects_inconsistent_github_request_count() -> None:
    candidate = event()
    candidate["telemetry"]["github_requests"]["total"] = 23

    with pytest.raises(ValueError, match="must equal"):
        MODULE.validate_event(candidate)


def test_rejects_stale_or_mismatched_event_target() -> None:
    candidate = event()

    with pytest.raises(ValueError, match="repo does not match"):
        MODULE.validate_event(candidate, expected_repo="other/repo")
    with pytest.raises(ValueError, match="sequence is stale"):
        MODULE.validate_event(candidate, after_sequence=2)
    with pytest.raises(ValueError, match="head_sha does not match"):
        MODULE.validate_event(candidate, expected_head="b" * 40)
