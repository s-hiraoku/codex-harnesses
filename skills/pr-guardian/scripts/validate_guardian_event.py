#!/usr/bin/env python3
"""Validate and normalize a PR Guardian terminal event."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

EVENTS = {"actionable", "merge_ready", "timeout", "blocked"}


def require_type(value: dict[str, Any], key: str, expected: type) -> Any:
    item = value.get(key)
    if not isinstance(item, expected):
        raise ValueError(f"{key} must be {expected.__name__}")
    return item


def require_non_negative(value: dict[str, Any], key: str) -> int:
    item = value.get(key)
    if not isinstance(item, int) or isinstance(item, bool) or item < 0:
        raise ValueError(f"{key} must be a non-negative integer")
    return item


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include a timezone: {value}")
    return parsed


def validate_event(
    event: Any,
    *,
    expected_repo: str | None = None,
    expected_pr: int | None = None,
    expected_job: str | None = None,
    expected_head: str | None = None,
    after_sequence: int | None = None,
) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("terminal event must be one JSON object")
    if event.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if event.get("event") not in EVENTS:
        raise ValueError(f"event must be one of {sorted(EVENTS)}")

    for key in ("job_id", "repo", "head_sha", "observed_at", "reason"):
        if not require_type(event, key, str).strip():
            raise ValueError(f"{key} must not be empty")
    if require_non_negative(event, "pr") == 0:
        raise ValueError("pr must be positive")
    if require_non_negative(event, "sequence") == 0:
        raise ValueError("sequence must be positive")
    if expected_repo is not None and event["repo"] != expected_repo:
        raise ValueError("repo does not match expected target")
    if expected_pr is not None and event["pr"] != expected_pr:
        raise ValueError("pr does not match expected target")
    if expected_job is not None and event["job_id"] != expected_job:
        raise ValueError("job_id does not match expected job")
    if expected_head is not None and event["head_sha"] != expected_head:
        raise ValueError("head_sha does not match expected head")
    if after_sequence is not None and event["sequence"] <= after_sequence:
        raise ValueError("sequence is stale")

    delta = require_type(event, "delta", dict)
    for key in ("checks", "reviews", "threads"):
        require_type(delta, key, list)

    gate = require_type(event, "gate", dict)
    require_type(gate, "is_draft", bool)
    require_type(gate, "required_checks_passed", bool)
    require_type(gate, "expected_reviews_current", bool)
    require_non_negative(gate, "unresolved_thread_count")
    require_non_negative(gate, "actionable_comment_count")
    require_type(gate, "stabilized", bool)

    evidence = require_type(event, "evidence", dict)
    require_type(evidence, "pagination_complete", bool)
    review_complete_at = require_type(evidence, "review_evidence_complete_at", str)
    expected_reviews = require_type(evidence, "expected_reviews", list)
    required_checks = require_type(evidence, "required_checks", list)
    unresolved_threads = require_type(evidence, "unresolved_threads", list)
    actionable_comments = require_type(evidence, "actionable_comments", list)
    snapshots = require_type(evidence, "stabilization_snapshots", list)

    telemetry = require_type(event, "telemetry", dict)
    for key in ("cycles", "head_resets", "passive_wait_ms", "active_runner_ms"):
        require_non_negative(telemetry, key)
    for key in ("started_at", "finished_at"):
        if not require_type(telemetry, key, str).strip():
            raise ValueError(f"telemetry.{key} must not be empty")
    requests = require_type(telemetry, "github_requests", dict)
    total = require_non_negative(requests, "total")
    graphql = require_non_negative(requests, "graphql")
    rest = require_non_negative(requests, "rest")
    if total != graphql + rest:
        raise ValueError("github_requests.total must equal graphql + rest")

    if event["event"] == "merge_ready":
        if gate["is_draft"]:
            raise ValueError("merge_ready requires a non-draft PR")
        if gate.get("mergeable") != "MERGEABLE":
            raise ValueError("merge_ready requires gate.mergeable=MERGEABLE")
        if gate.get("merge_state_status") not in {"CLEAN", "HAS_HOOKS", "UNSTABLE"}:
            raise ValueError("merge_ready requires a clean merge state")
        if gate.get("review_decision") == "CHANGES_REQUESTED":
            raise ValueError("merge_ready cannot have requested changes")
        if not gate["required_checks_passed"]:
            raise ValueError("merge_ready requires passing required checks")
        if not gate["expected_reviews_current"]:
            raise ValueError("merge_ready requires current-head review evidence")
        if gate["unresolved_thread_count"] != 0:
            raise ValueError("merge_ready requires zero unresolved threads")
        if gate["actionable_comment_count"] != 0:
            raise ValueError("merge_ready requires zero undisposed actionable comments")
        if not gate["stabilized"]:
            raise ValueError("merge_ready requires stabilization")
        if not evidence["pagination_complete"]:
            raise ValueError("merge_ready requires complete pagination")
        if gate["unresolved_thread_count"] != len(unresolved_threads):
            raise ValueError("unresolved thread count contradicts evidence")
        if gate["actionable_comment_count"] != len(actionable_comments):
            raise ValueError("actionable comment count contradicts evidence")
        for review in expected_reviews:
            if not isinstance(review, dict):
                raise ValueError("expected review evidence must be objects")
            if review.get("state") not in {"APPROVED", "CHANGES_REQUESTED", "COMMENTED"}:
                raise ValueError("expected review is not terminal")
            if review.get("commit_id") != event["head_sha"]:
                raise ValueError("expected review is not for head_sha")
        passing = {"SUCCESS", "SKIPPED", "NEUTRAL"}
        for check in required_checks:
            if not isinstance(check, dict):
                raise ValueError("required check evidence must be objects")
            if check.get("status") not in {"COMPLETED", "SUCCESS"}:
                raise ValueError("required check is not complete")
            conclusion = check.get("conclusion")
            if conclusion is not None and conclusion not in passing:
                raise ValueError("required check is not passing")
        if len(snapshots) != 2 or not all(isinstance(item, dict) for item in snapshots):
            raise ValueError("merge_ready requires two stabilization snapshots")
        first, second = snapshots
        for snapshot in snapshots:
            if snapshot.get("head_sha") != event["head_sha"]:
                raise ValueError("stabilization snapshot is not for head_sha")
            if not isinstance(snapshot.get("activity_fingerprint"), str):
                raise ValueError("stabilization snapshot needs an activity fingerprint")
        if first["activity_fingerprint"] != second["activity_fingerprint"]:
            raise ValueError("stabilization activity changed")
        review_time = parse_time(review_complete_at)
        first_time = parse_time(str(first.get("observed_at")))
        second_time = parse_time(str(second.get("observed_at")))
        if (first_time - review_time).total_seconds() < 60:
            raise ValueError("first stabilization snapshot needs a 60-second quiet period")
        if (second_time - first_time).total_seconds() < 30:
            raise ValueError("stabilization snapshots must be at least 30 seconds apart")

    return event


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "event_file", nargs="?", type=Path, help="JSON event file; stdin if omitted"
    )
    parser.add_argument("--repo", help="Expected owner/repo")
    parser.add_argument("--pr", type=int, help="Expected pull request number")
    parser.add_argument("--job-id", help="Expected durable job identifier")
    parser.add_argument("--head-sha", help="Expected head SHA")
    parser.add_argument("--after-sequence", type=int, help="Require a newer event sequence")
    args = parser.parse_args()

    try:
        source = args.event_file.read_text() if args.event_file else sys.stdin.read()
        event = validate_event(
            json.loads(source),
            expected_repo=args.repo,
            expected_pr=args.pr,
            expected_job=args.job_id,
            expected_head=args.head_sha,
            after_sequence=args.after_sequence,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"invalid guardian event: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(event, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
