# Task Ledger Patterns

The task ledger keeps long-running Codex work resumable. Hooks stop accidents. The ledger stops drift.

Use the ledger for task state that must survive context loss, handoff, interruption, or a long verification loop.

For small, low-risk edits, the final response may be enough. For larger, security-sensitive, risky, or interrupted work, treat ledger updates as part of the task rather than optional cleanup.

## What Belongs in the Ledger

Put these in the ledger:

- current goal and scope
- active plan and next step
- decisions that affect future edits
- risks and mitigations
- verification commands and outcomes
- reusable review-feedback lessons that future implementation should check
- blockers and assumptions

Do not put these in the ledger:

- secrets or credentials
- large pasted logs
- temporary scratch notes that no future session needs
- instructions that belong in `AGENTS.md`
- reusable workflows that belong in skills

## Current State Pattern

Use `ledger/current.md` for the active task.

Keep it short enough to read at restart:

```md
## Current Goal

- Goal:
- Status:

## Progress

- YYYY-MM-DD HH:MM: Completed X. Y remains.

## Next Step

- Run command Z and inspect file A.
```

The `Next Step` section is the most important part. A future Codex session should be able to continue from it without reconstructing the task from chat history.

## Decision Pattern

Use `ledger/decisions.md` when a choice will affect later work.

Good decisions include:

- choosing one API shape over another
- deferring a risky migration
- preserving backward compatibility
- changing verification strategy

Each decision should include context, alternatives, rationale, and consequences.

## Risk Pattern

Use `ledger/risks.md` for known uncertainty.

Track:

- what could go wrong
- likely impact
- mitigation
- current status

Close risks when verification or review resolves them.

## Verification Pattern

Use `ledger/verification.md` for commands that matter.

Record:

- command
- scope
- result
- notes or failures

Do not record every tiny command. Record checks that future work should trust or revisit.

Good verification entries are exact enough to rerun:

```md
### 2026-05-05 14:30

- Command: `CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level docs, hooks, policies, examples, and scripts
- Result: passed
- Notes: ran before opening PR
```

## Review Feedback Pattern

Use `ledger/review-feedback.md` for review comments, CI failures, bug reports, user corrections, or retrospectives that should affect future implementation.

Do not archive every comment. Keep only reusable patterns with a concrete implementation rule:

```md
### 2026-07-10 - Example Pattern

- Status: Active
- Last seen: 2026-07-10
- Source: PR review
- Trigger: when touching the same workflow or boundary
- Issue: the change missed a required edge case
- Cause: the plan did not include prior reviewer expectations
- Implementation rule: read this entry before coding and add a targeted check for that edge case
- Evidence: PR number, file path, or command name
- Verification: targeted test or review checklist item
```

Before planning implementation work, skim active entries and carry relevant rules into the plan, tests, and self-review checklist. If feedback recurs, update the existing entry instead of adding a duplicate.

## Checkpoint Pattern

Run `scripts/checkpoint.sh` before pausing, after major milestones, and before risky edits.

A useful checkpoint captures:

- timestamp
- branch
- git status
- latest commit

Checkpoints do not replace progress notes. They provide git context around the progress notes.

## Resume Pattern

When resuming a long-running task:

1. Read `ledger/current.md`.
2. Read open entries in `ledger/risks.md`.
3. Skim recent `ledger/verification.md` entries.
4. Check `git status --short`.
5. Continue from the recorded next step.

If the ledger and git status disagree, trust the working tree and update the ledger before editing.

## Handoff Pattern

Before handing work to another session or human reviewer, add:

- what changed
- what remains
- what was verified
- known risks
- exact next step

Good handoff entries are short, concrete, and command-oriented.
