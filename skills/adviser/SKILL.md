---
name: adviser
description: Route an independent review-only agent to a stronger model tier or reasoning effort at key decision points, then continue the task in the main agent. Use when the user asks for an adviser, advisor, second opinion, stronger review, or Claude Code /advisor-like behavior; before committing to a consequential approach on a multi-step task; when work is stuck or changing direction; and before declaring substantial work complete.
---

# Adviser

Use a fresh, review-only agent at a strictly stronger model tier or reasoning effort. “Fresh” means newly spawned for that consultation and uninvolved in prior task actions. “Review-only” is an instruction-level role, not a sandbox or tool-permission boundary, unless the runtime separately restricts that agent's tools. The main agent remains the executor and owns every tool call, edit, decision, and final answer.

This skill emulates native Advisor's decision pattern, not its server implementation. It uses the user-defined escalation policy below and fails closed when it cannot prove that the requested route is stronger under that policy. It cannot guarantee that the backend honored a requested route, complete transcript delivery, same-turn sub-inference, native usage accounting, prompt-cache behavior, or Advisor UI.

## Routing Table

Resolve the caller's effective model and reasoning effort, then apply exactly one row. Do not infer aliases, silently inherit the caller configuration, lower effort, or substitute an unlisted model.

| Caller model | Caller effort | Adviser model | Adviser effort |
| --- | --- | --- | --- |
| `gpt-5.6-luna` | `low` | `gpt-5.6-sol` | `low` |
| `gpt-5.6-luna` | `medium` | `gpt-5.6-sol` | `medium` |
| `gpt-5.6-luna` | `high` | `gpt-5.6-sol` | `high` |
| `gpt-5.6-luna` | `xhigh` | `gpt-5.6-sol` | `xhigh` |
| `gpt-5.6-luna` | `max` | `gpt-5.6-sol` | `max` |
| `gpt-5.6-terra` | `low` | `gpt-5.6-sol` | `low` |
| `gpt-5.6-terra` | `medium` | `gpt-5.6-sol` | `medium` |
| `gpt-5.6-terra` | `high` | `gpt-5.6-sol` | `high` |
| `gpt-5.6-terra` | `xhigh` | `gpt-5.6-sol` | `xhigh` |
| `gpt-5.6-terra` | `max` | `gpt-5.6-sol` | `max` |
| `gpt-5.6-terra` | `ultra` | `gpt-5.6-sol` | `ultra` |
| `gpt-5.6-sol` | `low` | `gpt-5.6-sol` | `medium` |
| `gpt-5.6-sol` | `medium` | `gpt-5.6-sol` | `high` |
| `gpt-5.6-sol` | `high` | `gpt-5.6-sol` | `xhigh` |
| `gpt-5.6-sol` | `xhigh` | `gpt-5.6-sol` | `max` |
| `gpt-5.6-sol` | `max` | `gpt-5.6-sol` | `ultra` |
| `gpt-5.6-sol` | `ultra` | unavailable | unavailable |

`gpt-5.6-sol/ultra` is the defined ceiling. An unknown model, unknown effort, unavailable target, or ceiling result is not an Adviser consultation. Report that no strictly stronger route is available and use the separated self-review fallback only if useful.

## Workflow

1. Orient before consulting. Read the task and gather the minimum evidence the adviser needs. File discovery, source retrieval, and inspecting current state are orientation; editing, committing to an interpretation, and declaring completion are substantive work.
2. Decide whether consultation adds value at the current decision point. Favor long multi-step work, consequential or ambiguous choices, recurring failures, and independent completion checks. Skip short mechanical tasks and work where every step genuinely requires the strongest available main model.
3. Build a review packet with the user goal, constraints, inspected facts and relevant tool results, current assumptions, proposed decision, unresolved questions, verification plan, and—at completion—changed artifacts, diff summary, test results, and known risks. Exclude secrets and irrelevant transcript content.
4. Resolve this skill's filesystem directory as `<skill-dir>`. Run `python3 <skill-dir>/scripts/route_adviser.py` to resolve the caller's current `turn_context` and select the table row. Pass explicit `--model` and `--effort` only in tests or when the runtime supplied both values authoritatively. The rollout JSONL is an internal Codex format; stop the Adviser path if it is absent, ambiguous, malformed, or unsupported.
5. Spawn one fresh adviser with the fullest available conversation inheritance (`fork_turns: "all"`), the routed model and effort, and the review packet explicitly when the spawn tool exposes both routing fields. Otherwise pipe the packet to `python3 <skill-dir>/scripts/run_adviser.py`, which launches an ephemeral, read-only Codex reviewer with the selected route. Do not use an unpinned spawn as a fallback.
6. Instruct the adviser to return review text only and not edit files, run commands, spawn agents, invoke another adviser, or take ownership of the task. Do not claim it received a complete transcript: compaction, fork limits, or an explicitly bounded packet may remove context.
7. Weigh the advice. Adopt useful recommendations, but prefer repository evidence, primary sources, and empirical results when they conflict with unsupported advice. Record any material change of approach in the normal task commentary or plan.
8. Reconcile material conflicts. If evidence points one way and the adviser points another, send one follow-up to the same adviser when possible so it can defend or revise its exact claim. State the conflict and ask which constraint breaks the tie. Use a fresh routed adviser only when the original is unavailable. Do not silently switch directions or loop over minor disagreements.
9. Reconsult when material ambiguity blocks a decision, the same failure recurs, the approach stops converging, or a materially different approach is under consideration.
10. Before declaring substantial work complete, make the deliverable durable and run relevant verification. Consult again when an independent completion check is valuable. Fix actionable findings and rerun only checks affected by those fixes.
11. Report Adviser use briefly in the final answer: timing, caller and adviser routes, material advice followed or rejected, context limitations, and residual risk.

Typical high-value checkpoints are after orientation but before choosing an approach, and after verification but before declaring completion. These are model-driven defaults, not a fixed quota or mandatory two-call rule. Honor an explicit user request to consult before continuing or to skip Adviser for the task.

## Adviser Prompt Contract

Use a bounded prompt like this when spawning the reviewer:

```text
Act as the Adviser: an independent, review-only strategic reviewer. Return review text only. Do not edit files, run commands, or take over execution. Review the supplied packet and available inherited context. Identify incorrect assumptions, missed constraints, evidence conflicts, likely failure modes, and the best next approach. Be concrete and concise. Distinguish evidence-backed findings from uncertainty. End with: recommendation, critical risks, evidence conflicts, and completion checks.
```

At the completion gate, replace “best next approach” with a request to decide whether the result is ready to report complete and to list only actionable gaps.

## Fallback

If routing or fresh-agent execution is unavailable, perform a clearly separated second-pass review using the same contract, state that stronger-model independence was unavailable, and do not imply that an Adviser consultation ran.

## Final Report

Include the number and timing of consultations, caller route, requested Adviser route, whether the runtime verified the effective route, material advice followed or rejected, context-delivery limitations, verification status and checks rerun after adviser-driven changes, and any residual risk or degraded fallback. Do not report a requested route as verified effective without runtime evidence. Do not rerun unchanged checks solely for ceremony.
