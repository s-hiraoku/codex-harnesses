# User Guide

This guide shows how the harness pieces fit together and how to adopt them in an existing project.

## Mental Model

Use this separation:

- `AGENTS.md`: durable project guidance
- Skills: reusable task workflows
- MCP: external tools and knowledge access
- Hooks: deterministic lifecycle scripts
- Policies: permission and safety rules
- Task Ledger: long-running task memory
- Verification: lint, typecheck, test, and build loops

Each layer should do one job. Do not use `AGENTS.md` as a task ledger, do not use skills as project memory, and do not treat example hooks as production security controls without hardening.

## What to Copy First

For most projects, start with:

1. one `AGENTS.md` template
2. `scripts/verify.sh`
3. `ledger/`
4. one policy file
5. one or two skills that match repeated work

Add hooks only after you have reviewed and tested the payload scripts.

## Recommended Adoption Path

1. Pick an example project shape from [Examples](examples.md).
2. Copy the relevant files into your target repository.
3. Replace generic commands with real project commands.
4. Run `bash scripts/verify.sh`.
5. Run one small real task through Codex.
6. Update `AGENTS.md`, ledger templates, and verification commands based on what was unclear.
7. Add CI and strict verification.

## Choosing a Starting Example

- Minimal project: use when you only need durable guidance and task memory.
- Frontend project: use when browser verification and UI guidance matter.
- Next.js project: use when server/client boundaries, route handlers, server actions, and environment variables need explicit guidance.
- Strict repository: use when safety, review, and verification expectations should be conservative.

See [Examples](examples.md) for the full list.

## Daily Workflow

For a typical task:

1. Select the matching skill.
2. Record the goal and next step in the task ledger.
3. Inspect the current code and tests.
4. Make small changes.
5. Run targeted verification.
6. Update docs or ledger entries when behavior changes.
7. Run repository verification before finalizing.
8. Summarize changed files, verification, risks, and next steps.

## Safety Notes

Hooks are enforcement payloads, not complete safety systems. Use them with:

- sandboxing
- approval policy
- code review
- git isolation
- CI verification

For production use, read [Hook Hardening](hook-hardening.md).

## Long-Running Work

For long-running tasks, the ledger is the recovery point. It should record the current goal, decisions, risks, verification results, and the exact next step.

Read [Task Ledger Patterns](task-ledger-patterns.md) before using Codex for multi-hour or multi-session work.

