# Adoption Checklist

Use this checklist when adding Codex harnesses to an existing project.

## 1. Pick a Starting Shape

- [ ] Minimal project: copy `examples/minimal-codex-project`
- [ ] Frontend project: copy `examples/frontend-project`
- [ ] Next.js project: copy `examples/nextjs-project`
- [ ] Strict repository: copy `examples/strict-repo`

Copy only what you need. A small accurate harness is better than a broad stale one.

## 2. Add Durable Guidance

- [ ] Copy an `AGENTS.md` template into the target repository.
- [ ] Replace generic commands with real project commands.
- [ ] Remove instructions that are temporary or issue-specific.
- [ ] Add safety expectations for destructive commands, secrets, and git operations.

## 3. Choose Skills

- [ ] Copy only the skills that match repeated work.
- [ ] Keep skills focused on workflow, verification, and reporting.
- [ ] Keep project-specific state out of skills.

## 4. Wire Hooks Carefully

- [ ] Review hook payload scripts before registration.
- [ ] Decide which lifecycle event should call each hook.
- [ ] Test blocked and allowed cases locally.
- [ ] Document that hooks are examples unless hardened for the project.

## 5. Add Policy

- [ ] Copy a policy from `policies/`.
- [ ] Validate it against `schemas/policy.schema.json`.
- [ ] Make approval, sandboxing, verification, and git behavior explicit.
- [ ] Decide which parts are guidance and which parts are enforced.

## 6. Add a Task Ledger

- [ ] Copy `ledger/` or create a project-local `.codex/tasks/current.md`.
- [ ] Record current goal, progress, blockers, and next step.
- [ ] Add checkpoints before pauses and after risky edits.

## 7. Make Verification Real

- [ ] Copy or adapt `scripts/verify.sh`.
- [ ] Ensure lint, typecheck, test, and build commands match the project.
- [ ] Run verification locally.
- [ ] Add CI that runs verification in strict mode.

## 8. First Task Trial

- [ ] Run one small real task through the harness.
- [ ] Check whether Codex had enough durable guidance.
- [ ] Check whether verification ran at the right time.
- [ ] Remove any harness files that were not useful.

