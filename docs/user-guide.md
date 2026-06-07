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
2. Copy the relevant harness files into your target repository.
3. Install repeated-work skills with APM, `gh skill`, or `npx skills`.
4. Replace generic commands with real project commands.
5. Run `bash scripts/verify.sh`.
6. Run one small real task through Codex.
7. Update `AGENTS.md`, ledger templates, and verification commands based on what was unclear.
8. Add CI and strict verification.

## Choosing a Starting Example

- Minimal project: use when you only need durable guidance and task memory.
- Frontend project: use when browser verification and UI guidance matter.
- Next.js project: use when server/client boundaries, route handlers, server actions, and environment variables need explicit guidance.
- Strict repository: use when safety, review, and verification expectations should be conservative.

See [Examples](examples.md) for the full list.

## Installing Skills

Use one of these three installer paths instead of a repository-specific shell installer.

APM is the best fit when a team wants project setup declared in a versioned manifest:

```yaml
# apm.yml
name: your-project
version: 1.0.0
dependencies:
  apm:
    - s-hiraoku/codex-harnesses/skills/feature-implementation
    - s-hiraoku/codex-harnesses/skills/bug-fix
    - s-hiraoku/codex-harnesses/skills/review
```

```sh
apm install
```

GitHub CLI is useful when installing one skill at a time:

```sh
gh skill preview s-hiraoku/codex-harnesses feature-implementation
gh skill install s-hiraoku/codex-harnesses feature-implementation --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses implement-to-merge-ready --agent codex --scope project
```

Use `--scope user` for user-wide installation.

The Skills CLI is useful when an npm-based command is easier in the environment:

```sh
npx skills add s-hiraoku/codex-harnesses --list
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation
npx skills add s-hiraoku/codex-harnesses --agent codex --skill implement-to-merge-ready
```

Use `--global` for user-wide installation. Install only the skills that match repeated work, such as `implement-to-merge-ready` for implementation tasks that should continue through PR creation and merge-readiness follow-up.

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
