# Adoption Checklist

Use this checklist when adding Codex harnesses to an existing project.

## 1. Pick a Starting Shape

- [ ] Minimal project: inspect `examples/minimal-codex-project`
- [ ] Frontend project: inspect `examples/frontend-project`
- [ ] Next.js project: inspect `examples/nextjs-project`
- [ ] Strict repository: inspect `examples/strict-repo`

Copy only what you need. A small accurate harness is better than a broad stale one.

## 2. Add Durable Guidance

- [ ] Copy an `AGENTS.md` template into the target repository.
- [ ] Replace generic commands with real project commands.
- [ ] Remove instructions that are temporary or issue-specific.
- [ ] Add safety expectations for destructive commands, secrets, and git operations.

## 3. Choose Skills

- [ ] Install only the skills that match repeated work with APM, `gh skill install`, or `npx skills add`.
- [ ] Preview or inspect skill contents before installing them.
- [ ] Keep skills focused on workflow, verification, and reporting.
- [ ] Keep project-specific state out of skills.

## 4. Wire Hooks Carefully

- [ ] Review hook payload scripts before registration.
- [ ] Confirm that copying the hook file alone does not register it with Codex.
- [ ] Decide which lifecycle event should call each hook.
- [ ] Test blocked and allowed cases locally.
- [ ] Document that hooks are examples unless hardened for the project.

See `hook-hardening.md` before relying on example hooks in important repositories.

## 5. Add Policy

- [ ] Copy a policy from `policies/`.
- [ ] Validate it against `schemas/policy.schema.json`.
- [ ] Make approval, sandboxing, verification, and git behavior explicit.
- [ ] Decide which parts are guidance and which parts are enforced.

## 6. Add a Task Ledger

- [ ] Copy `ledger/` or create a project-local `.codex/tasks/current.md`.
- [ ] Record current goal, progress, blockers, and next step.
- [ ] Decide when ledger updates are required, such as large, risky, security-sensitive, or interrupted tasks.
- [ ] Add checkpoints before pauses and after risky edits.

## 7. Make Verification Real

- [ ] Copy or adapt `scripts/verify.sh`.
- [ ] Ensure lint, typecheck, test, and build commands match the project.
- [ ] Run verification locally.
- [ ] Add CI that runs the same verification script in strict mode.

## 8. First Task Trial

- [ ] Run one small real task through the harness.
- [ ] Check whether Codex had enough durable guidance.
- [ ] Check whether verification ran at the right time.
- [ ] Remove any harness files that were not useful.
