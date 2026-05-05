# Long-Running Codex Tasks

Long-running tasks need resumable state and frequent verification.

## Task Ledger

Use `ledger/current.md` to record the current goal, plan, progress, blockers, and next step. Update it whenever the task changes shape.

Use separate files for:

- durable decisions
- known risks
- verification results

This keeps restart context compact and reviewable.

## Checkpoints

Run `scripts/checkpoint.sh` before pausing, after major milestones, and before risky edits. A checkpoint should capture branch, status, and latest commit.

## Verification

Run targeted verification after meaningful changes and repository-level verification before finalizing. Record important results in `ledger/verification.md`.

## Small Commits

Prefer small commits that represent complete, reviewable steps. Each commit should have a clear reason and passing relevant checks.

## Worktrees

For risky or parallel work, use git worktrees. Worktrees isolate experiments while keeping the main checkout stable.

## Resumption

When resuming, read:

1. `ledger/current.md`
2. recent entries in `ledger/verification.md`
3. open risks in `ledger/risks.md`
4. recent git diff and status

Then continue from the recorded next step instead of restarting the task from memory.

