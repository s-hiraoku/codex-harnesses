---
name: adviser
description: Consult an independent reviewer subagent at key decision points, then continue the task in the main agent. Use when the user asks for an adviser, advisor, second opinion, stronger review, or Claude Code /advisor-like behavior; before committing to a consequential approach on a multi-step task; when work is stuck or changing direction; and before declaring substantial work complete.
---

# Adviser

Use a fresh, read-only subagent as an independent strategic reviewer. “Fresh” means newly spawned for that consultation and uninvolved in prior task actions; it does not imply a different model unless the runtime supports model selection. The main agent remains the executor and owns every tool call, edit, decision, and final answer.

## Workflow

1. Orient before consulting. Read the task and gather the minimum evidence the adviser needs. File discovery, source retrieval, and inspecting current state are orientation; editing, committing to an interpretation, and declaring completion are substantive work.
2. Consult before substantive work on a multi-step or consequential task. Spawn one fresh adviser with full conversation inheritance (`fork_turns: "all"`). Ask it to review the task, evidence, assumptions, proposed approach, risks, and verification plan. Tell it not to edit files, run commands, or take ownership of the task.
3. Weigh the advice. Adopt useful recommendations, but prefer repository evidence, primary sources, and empirical results when they conflict with unsupported advice. Record any material change of approach in the normal task commentary or plan.
4. Reconcile conflicts. If evidence points one way and the adviser points another, send one follow-up to the same adviser when possible so it can defend or revise its exact claim. State the conflict and ask which constraint breaks the tie. Use a fresh adviser only when the original is unavailable. Do not silently switch directions.
5. Reconsult when the same failure recurs, the approach stops converging, or a materially different approach is under consideration.
6. Consult before declaring substantial work complete. First make the deliverable durable by saving edits and running the relevant verification. Give a fresh adviser the completed outcome, diff or artifact summary, verification evidence, and known risks. Fix actionable findings before the final answer.
7. Report Adviser use briefly in the final answer: consultations performed, material advice followed or rejected, and any residual limitation.

For work longer than a few steps, target at least two consultations: one after orientation and before choosing the approach, and one after verification and before declaring completion. Do not add ritual consultations to short reactive work whose next action is already dictated by fresh tool output.

## Adviser Prompt Contract

Use a bounded prompt like this when spawning the reviewer:

```text
Act as the Adviser: an independent, read-only strategic reviewer. Do not edit files, run commands, or take over execution. Using the inherited conversation and evidence, identify incorrect assumptions, missed constraints, likely failure modes, and the best next approach. Be concrete and concise. Distinguish evidence-backed findings from uncertainty. End with: recommendation, critical risks, and completion checks.
```

At the completion gate, replace “best next approach” with a request to decide whether the result is ready to report complete and to list only actionable gaps.

## Fallback

If fresh subagents are unavailable, perform a clearly separated second-pass review using the same contract, state that independence was unavailable, and do not imply that a separate adviser model ran.

## Final Report

Include the number and timing of consultations, material advice followed or rejected, verification status and any checks rerun after adviser-driven changes, and any residual risk or degraded fallback. Do not rerun unchanged checks solely for ceremony.
