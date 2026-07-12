---
name: adviser
description: Consult an independent review-only subagent at key decision points, then continue the task in the main agent. Use when the user asks for an adviser, advisor, second opinion, stronger review, or Claude Code /advisor-like behavior; before committing to a consequential approach on a multi-step task; when work is stuck or changing direction; and before declaring substantial work complete.
---

# Adviser

Use a fresh, review-only subagent as an independent strategic reviewer. “Fresh” means newly spawned for that consultation and uninvolved in prior task actions. “Review-only” is an instruction-level role, not a sandbox or tool-permission boundary, unless the runtime separately restricts that subagent's tools. The main agent remains the executor and owns every tool call, edit, decision, and final answer.

This skill emulates native Advisor's decision pattern, not its server implementation. It cannot guarantee a stronger model, complete transcript delivery, same-turn sub-inference, native usage accounting, prompt-cache behavior, or Advisor UI. Treat the consultation as an independent review; report model strength as `stronger`, `same-tier`, or `unknown` only when the runtime provides enough evidence. Unknown model strength does not make the adviser unavailable: if a fresh subagent returns advice, count the consultation and label its capability `unknown`.

## Workflow

1. Orient before consulting. Read the task and gather the minimum evidence the adviser needs. File discovery, source retrieval, and inspecting current state are orientation; editing, committing to an interpretation, and declaring completion are substantive work.
2. Decide whether consultation adds value at the current decision point. Favor long multi-step work, consequential or ambiguous choices, recurring failures, and independent completion checks. Skip short mechanical tasks and work where every step genuinely requires the strongest available main model.
3. Build a review packet with the user goal, constraints, inspected facts and relevant tool results, current assumptions, proposed decision, unresolved questions, verification plan, and—at completion—changed artifacts, diff summary, test results, and known risks. Exclude secrets and irrelevant transcript content.
4. Spawn one fresh adviser with the fullest available conversation inheritance (`fork_turns: "all"`) and include the review packet explicitly. Do not claim it received a complete transcript: compaction, fork limits, or omitted tool output may remove context. Instruct it to return review text only and not edit files, run commands, or take ownership of the task. If the runtime supports per-agent tool restrictions, disable mutating tools as defense in depth. Continue with capability `unknown` when model metadata is absent; use the self-review fallback only when no fresh subagent can launch and return advice.
5. Weigh the advice. Adopt useful recommendations, but prefer repository evidence, primary sources, and empirical results when they conflict with unsupported advice. Record any material change of approach in the normal task commentary or plan.
6. Reconcile material conflicts. If evidence points one way and the adviser points another, send one follow-up to the same adviser when possible so it can defend or revise its exact claim. State the conflict and ask which constraint breaks the tie. Use a fresh adviser only when the original is unavailable. Do not silently switch directions or loop over minor disagreements.
7. Reconsult when material ambiguity blocks a decision, the same failure recurs, the approach stops converging, or a materially different approach is under consideration.
8. Before declaring substantial work complete, make the deliverable durable and run relevant verification. Consult again when an independent completion check is valuable. Fix actionable findings and rerun only checks affected by those fixes.
9. Report Adviser use briefly in the final answer: timing, capability class, material advice followed or rejected, context limitations, and residual risk.

Typical high-value checkpoints are after orientation but before choosing an approach, and after verification but before declaring completion. These are model-driven defaults, not a fixed quota or mandatory two-call rule. Honor an explicit user request to consult before continuing or to skip Adviser for the task.

## Adviser Prompt Contract

Use a bounded prompt like this when spawning the reviewer:

```text
Act as the Adviser: an independent, review-only strategic reviewer. Return review text only. Do not edit files, run commands, or take over execution. Review the supplied packet and available inherited context. Identify incorrect assumptions, missed constraints, evidence conflicts, likely failure modes, and the best next approach. Be concrete and concise. Distinguish evidence-backed findings from uncertainty. End with: recommendation, critical risks, evidence conflicts, and completion checks.
```

At the completion gate, replace “best next approach” with a request to decide whether the result is ready to report complete and to list only actionable gaps.

## Fallback

If fresh subagents are unavailable, perform a clearly separated second-pass review using the same contract, state that independence was unavailable, and do not imply that a separate adviser model ran.

## Final Report

Include the number and timing of consultations, capability class (`stronger`, `same-tier`, or `unknown`), material advice followed or rejected, context-delivery limitations, verification status and checks rerun after adviser-driven changes, and any residual risk or degraded fallback. Do not rerun unchanged checks solely for ceremony.
