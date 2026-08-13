# Guardian Event Contract

Use a non-LLM guardian process for all passive GitHub waiting and change detection. Codex starts or reactivates the runner once, handles only terminal events that require reasoning, and never reconstructs state by polling the process.

## Runner responsibilities

The runner owns CI watching, sleeps, GitHub API polling, current-head tracking, bot-review completion, unresolved-thread checks, and the stabilization window. A head change clears all review-completion and stabilization evidence before the next decision.

Persist enough job state that the process can be detached from the initiating Codex invocation. Deliver completion through a host notification or a durable terminal-event file/queue. Intermediate logs are operational data, not prompts for Codex. Before starting work, require `kaizen-loop guardian capabilities --json` to report `{"terminal_event_schema_versions":[1]}` and durable completion notification support; an older runner must fail before monitoring starts.

## Terminal event

Emit exactly one JSON object for each transition that should wake Codex. Use `schema_version: 1` and one of these events:

- `actionable`: CI failed, actionable feedback arrived, or a required conversation needs a response or fix.
- `merge_ready`: every mergeability gate in `SKILL.md` passed for the reported head after stabilization.
- `timeout`: the configured wait window expired.
- `blocked`: authentication, rate limiting, malformed GitHub data, permissions, runner failure, or another external condition prevents progress.

Required fields:

```json
{
  "schema_version": 1,
  "event": "actionable",
  "job_id": "owner-repo-pr-123",
  "sequence": 2,
  "repo": "owner/repo",
  "pr": 123,
  "head_sha": "full commit SHA",
  "observed_at": "2026-01-01T00:00:00Z",
  "reason": "required check failed",
  "delta": {
    "checks": [],
    "reviews": [],
    "threads": []
  },
  "gate": {
    "is_draft": false,
    "mergeable": "MERGEABLE",
    "merge_state_status": "BLOCKED",
    "review_decision": null,
    "required_checks_passed": false,
    "expected_reviews_current": false,
    "unresolved_thread_count": 0,
    "actionable_comment_count": 1,
    "stabilized": false
  },
  "evidence": {
    "pagination_complete": true,
    "review_evidence_complete_at": "2025-12-31T23:58:00Z",
    "expected_reviews": [],
    "required_checks": [
      {"name": "test", "status": "COMPLETED", "conclusion": "FAILURE"}
    ],
    "unresolved_threads": [],
    "actionable_comments": ["https://github.com/owner/repo/pull/123#issuecomment-1"],
    "stabilization_snapshots": []
  },
  "telemetry": {
    "cycles": 4,
    "head_resets": 1,
    "github_requests": {
      "total": 24,
      "graphql": 8,
      "rest": 16
    },
    "started_at": "2025-12-31T23:55:00Z",
    "finished_at": "2026-01-01T00:00:00Z",
    "passive_wait_ms": 240000,
    "active_runner_ms": 60000
  }
}
```

Count `github_requests` as actual HTTP/API requests, including pagination and retries, rather than loop iterations. `delta` contains only changes since the previous event or job start; include identifiers and URLs needed to diagnose or respond without repeated discovery calls.

For `merge_ready`, require a non-draft PR, `MERGEABLE`, a clean merge state, no requested changes, passing required checks, current-head expected reviews, complete pagination, zero unresolved threads, zero undisposed actionable comments, and completed stabilization. Each expected terminal review must name the reported `head_sha`. Include two stabilization snapshots with that head and the same activity fingerprint, taken at least 30 seconds apart after a 60-second quiet period. For `timeout` and `blocked`, include the final current-head gate and a concrete recovery action in `reason` or `delta`.

## Consumer rules

Accept `merge_ready` only when the runner exits successfully and the terminal event passes `scripts/validate_guardian_event.py` with the expected repo, PR, job, minimum sequence, and observed head. Then perform one event-triggered current-head lookup and require it to still equal `head_sha`; this is freshness confirmation, not a passive polling loop. Reject a target mismatch, stale sequence, unsupported schema version, missing field, multiple terminal objects, contradictory gate/evidence, truncated output, or successful exit without an event as `blocked: incompatible guardian runner`.

Do not feed routine poll logs back to Codex. Logs should separately expose GitHub request counts, passive wait time, runner-active time, and Codex action time so monitoring cost is distinguishable from reasoning and fix work.
