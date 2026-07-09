---
name: retrospective-codify
description: Convert review feedback, CI failures, bug fixes, or task retrospectives into a durable project feedback ledger, then make future implementation work consult that ledger before planning.
---

# Retrospective Codify

Use this workflow when a task produced feedback that should change how future implementation starts. The goal is not to archive every comment; it is to extract reusable implementation rules from concrete review findings, CI failures, regressions, or user corrections.

## Workflow

1. Identify the feedback source.
   - Use PR review comments, CodeRabbit or Codex findings, CI failure analysis, bug reports, user corrections, or a completed task retrospective.
   - Separate one-off requests from reusable failure patterns.
2. Read the project feedback ledger.
   - Prefer `ledger/review-feedback.md` when present.
   - If the project uses another durable task-memory path, use that path and name it in the final report.
   - If no feedback ledger exists and the pattern is worth keeping, create a compact one.
3. Extract reusable lessons.
   - For each candidate, write the specific issue, root cause, general implementation rule, evidence, and verification signal.
   - Keep rules operational: future agents should know what to check before coding, not just what went wrong.
   - Do not store secrets, long pasted comments, private user data, or full logs.
4. Deduplicate before appending.
   - If an existing entry covers the same class of failure, update `Last seen`, `Evidence`, or `Implementation rule` instead of adding a parallel entry.
   - If the same pattern recurs, strengthen the rule so it is harder to miss during planning.
5. Feed the ledger into future work.
   - When starting implementation, read active feedback-ledger entries before planning.
   - Carry relevant active rules into the plan, tests, and self-review checklist.
   - If no entries apply, say that the ledger was checked and no relevant prior feedback was found.
6. Close or retire stale entries.
   - Mark an entry `Retired` only when project structure, tooling, or policy makes the rule obsolete.
   - Do not delete history unless it contains sensitive content that should not have been recorded.

## Entry Format

Use this compact Markdown shape:

```md
### YYYY-MM-DD - Short Pattern Name

- Status: Active
- Source: PR review, CI failure, user correction, bug report, or retrospective
- Trigger: when this kind of implementation work starts
- Issue: what went wrong in the concrete task
- Cause: why the original implementation missed it
- Implementation rule: what future work must check or do before coding
- Evidence: concise links, file paths, PR numbers, or command names
- Verification: check that proves the rule was applied
```

## Final Report

Include:

- feedback sources reviewed
- ledger path updated or consulted
- entries added, updated, skipped as one-off, or retired
- implementation rules future work should apply
- any sensitive details intentionally omitted
