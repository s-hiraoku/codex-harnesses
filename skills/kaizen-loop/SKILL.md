---
name: kaizen-loop
description: "Run a continuous product improvement loop: evaluate a product or codebase end to end, identify product-quality improvement opportunities, present prioritized recommendations for user approval, then implement only approved improvements through the plan, goal, UI design, testing, review, PR, and merge-readiness workflow. Use when the user asks Codex to assess an app/product, find what can be improved, run a product evaluation, or iteratively improve a product with approval gates."
---

# Kaizen Loop

## Overview

Use this workflow when the task starts with product evaluation rather than a known implementation request. First evaluate the product as a user, engineer, and maintainer; then present concrete improvement candidates; after the user approves one or more items, execute those improvements with `implement-to-merge-ready` and repeat the evaluation loop.

## Workflow

1. Establish evaluation scope.
   - Identify the product, target user, primary workflows, success criteria, repository, branch, and deployment or local run path.
   - Read local instructions such as `AGENTS.md` before inspecting or editing.
   - Inspect `git status` and preserve unrelated user changes.
   - Ask only when the evaluation target or approval boundary is unclear.

2. Set an evaluation goal.
   - Use goal tracking for product-wide evaluation or any task expected to continue into implementation and PR work.
   - Write the goal to include evaluation, recommendation, approval gate, approved implementation, verification, PR creation, and merge-readiness follow-up.
   - Do not mark the goal complete until the approved loop is finished or the user declines all implementation.

3. Build a product understanding.
   - Read product docs, routes, screens, tests, analytics assumptions, configuration, and recent changes.
   - Run the app locally when practical.
   - For frontend products, inspect key screens in a real browser across representative desktop and mobile viewports.
   - For APIs or libraries, inspect public interfaces, examples, error behavior, docs, and test coverage.

4. Evaluate the product across relevant dimensions.
   - User value: whether the product solves the target job clearly and efficiently.
   - UX and UI: navigation, hierarchy, information density, visual quality, accessibility, responsive behavior, empty/loading/error states, and copy.
   - Correctness: core workflows, edge cases, data handling, permissions, failure modes, and regressions.
   - Performance and reliability: loading, interaction latency, caching, concurrency, offline or degraded states when relevant.
   - Engineering quality: architecture fit, maintainability, test coverage, observability, docs, configuration, and release risk.
   - Security and privacy: authentication, authorization, secrets, input validation, data exposure, and dependency risk.

5. Produce an evaluation report before editing.
   - Lead with the highest-impact findings.
   - For each improvement candidate, include: problem, user or business impact, evidence, likely fix direction, estimated scope, risk, and suggested verification.
   - Separate must-fix defects from product improvements and speculative ideas.
   - Do not implement evaluation findings before user approval unless the user already granted explicit blanket approval.

6. Ask for approval to proceed.
   - Present a short prioritized list of recommended improvements.
   - Ask the user which items to implement.
   - Treat silence or ambiguity as no approval for implementation.
   - If the user approves multiple items, group them into the smallest coherent PRs. Avoid bundling unrelated improvements.

7. Implement approved improvements.
   - Use `implement-to-merge-ready` for each approved change or coherent group.
   - For UI improvements where visual direction matters, use `ui-imagegen-director` before coding.
   - Keep the implementation tied to the approved finding. Do not opportunistically fix unapproved items.
   - Run targeted and repository-level verification appropriate to the change.

8. Review, open PRs, and bring them toward merge-ready.
   - Self-review the diff against the approved scope and evaluation evidence.
   - Open regular ready-for-review PRs by default. Do not create draft PRs unless explicitly requested.
   - Monitor CI and review feedback. Fix actionable failures or comments and re-check.
   - Report blockers clearly when the PR cannot be made mergeable.

9. Re-evaluate after approved changes.
   - Re-run the relevant parts of the product evaluation after implementation.
   - Confirm whether the approved problems were resolved.
   - Identify any newly visible improvement opportunities.
   - Present the next improvement candidates to the user and wait for approval before repeating the loop.

## Recommendation Format

Use this format for the approval gate:

```text
Evaluation summary:
- <one short product-level assessment>

Recommended improvements:
1. <title> [impact: high|medium|low, scope: small|medium|large]
   Problem: <what is wrong>
   Evidence: <what was observed>
   Fix direction: <what should change>
   Verification: <how to know it worked>

2. ...

Please tell me which item numbers to implement.
```

## Skill Composition

Use narrower skills when available and relevant:

- `goal-manager` for evaluation and implementation objective tracking.
- `modern-web-guidance`, Browser, and Playwright for frontend product evaluation.
- `ui-imagegen-director` for visually significant UI improvement proposals and implementation direction.
- `review` for product-quality and code-quality review.
- `release-check` when evaluating readiness for production or release.
- `implement-to-merge-ready` for approved implementation work through PR stabilization.
- `pr-guardian` after PR creation when CI or review follow-up is needed.

## Guardrails

- Evaluation may inspect broadly, but implementation must stay within approved scope.
- Do not fabricate user research, metrics, analytics, security findings, or benchmark results.
- Label inferences clearly when evidence is indirect.
- Prefer concrete, verifiable improvements over broad redesign advice.
- Separate quick wins from larger product bets.
- Do not merge PRs unless the user explicitly asks and repository policy permits it.

## Final Report

Include:

- evaluation scope and evidence gathered
- approved improvements implemented
- PR URLs, branches, and CI/review status
- verification run before and after implementation
- resolved product issues
- remaining recommendations awaiting approval
- goal status, when goal tracking was used
