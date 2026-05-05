# Task Ledger Patterns

The task ledger keeps long-running Codex work resumable. Hooks stop accidents. The ledger stops drift.

Use the ledger for task state that must survive context loss, handoff, interruption, or a long verification loop.

## What Belongs in the Ledger

Put these in the ledger:

- current goal and scope
- active plan and next step
- decisions that affect future edits
- risks and mitigations
- verification commands and outcomes
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

