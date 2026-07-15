#!/usr/bin/env python3
"""Resolve a strictly stronger Adviser model and reasoning effort."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SOL_MODEL = "gpt-5.6-sol"
MODEL_EFFORTS = {
    "gpt-5.6-luna": ("low", "medium", "high", "xhigh", "max"),
    "gpt-5.6-terra": ("low", "medium", "high", "xhigh", "max", "ultra"),
    SOL_MODEL: ("low", "medium", "high", "xhigh", "max", "ultra"),
}
SOL_ESCALATION = {
    "low": "medium",
    "medium": "high",
    "high": "xhigh",
    "xhigh": "max",
    "max": "ultra",
}
THREAD_ID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class RouteError(ValueError):
    """Raised when a strictly stronger Adviser route cannot be proven."""


@dataclass(frozen=True)
class Route:
    caller_model: str
    caller_effort: str
    adviser_model: str
    adviser_effort: str
    escalation: str


def route_adviser(model: str, effort: str) -> Route:
    supported_efforts = MODEL_EFFORTS.get(model)
    if supported_efforts is None:
        raise RouteError(f"unsupported caller model: {model}")
    if effort not in supported_efforts:
        raise RouteError(f"unsupported effort for {model}: {effort}")

    if model in {"gpt-5.6-luna", "gpt-5.6-terra"}:
        return Route(model, effort, SOL_MODEL, effort, "model")

    adviser_effort = SOL_ESCALATION.get(effort)
    if adviser_effort is None:
        raise RouteError(
            "gpt-5.6-sol/ultra is already at the routing ceiling; "
            "no strictly stronger Adviser route is defined"
        )
    return Route(model, effort, SOL_MODEL, adviser_effort, "effort")


def _rollout_path(codex_home: Path, thread_id: str) -> Path:
    if not THREAD_ID_PATTERN.fullmatch(thread_id):
        raise RouteError(f"invalid CODEX_THREAD_ID: {thread_id}")
    candidates = list(codex_home.glob(f"sessions/**/rollout-*-{thread_id}.jsonl"))
    candidates.extend(codex_home.glob(f"archived_sessions/rollout-*-{thread_id}.jsonl"))
    if not candidates:
        raise RouteError(f"rollout not found for CODEX_THREAD_ID={thread_id}")
    if len(candidates) != 1:
        raise RouteError(f"ambiguous rollout match for CODEX_THREAD_ID={thread_id}")
    return candidates[0]


def read_caller_context(codex_home: Path, thread_id: str) -> tuple[str, str]:
    context: tuple[str, str] | None = None
    rollout_text = _rollout_path(codex_home, thread_id).read_text(encoding="utf-8")
    lines = rollout_text.splitlines()
    if rollout_text and not rollout_text.endswith("\n"):
        lines.pop()
    for line_number, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise RouteError(f"invalid rollout JSON at line {line_number}") from error
        if event.get("type") != "turn_context":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        model = payload.get("model")
        effort = payload.get("effort")
        if isinstance(model, str) and isinstance(effort, str):
            context = (model, effort)

    if context is None:
        raise RouteError("the rollout has no turn_context containing model and effort")
    return context


def resolve_route(
    model: str | None,
    effort: str | None,
    codex_home: Path,
    thread_id: str | None,
) -> Route:
    if (model is None) != (effort is None):
        raise RouteError("--model and --effort must be supplied together")
    if model is None:
        if not thread_id:
            raise RouteError("CODEX_THREAD_ID is required when model and effort are omitted")
        model, effort = read_caller_context(codex_home, thread_id)
    return route_adviser(model, effort)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resolve the deterministic Adviser escalation route as JSON."
    )
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--thread-id", default=os.environ.get("CODEX_THREAD_ID"))
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        route = resolve_route(args.model, args.effort, args.codex_home, args.thread_id)
    except RouteError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(asdict(route), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
