# codex-harnesses

`codex-harnesses` is a collection of practical harnesses for long-running, reliable, safe, and high-quality Codex-driven software development.

Codex should not be expected to succeed by intelligence alone.

This repository provides reusable examples for project guidance, task workflows, deterministic lifecycle checks, safety policies, task ledgers, and verification loops. It is a harness collection, not a multi-agent router.

## Why Harnesses

Long-running software work fails when context drifts, verification is skipped, safety rules are vague, or project conventions live only in chat history. Harnesses move the important parts into durable files and deterministic checks.

Use this repository to help Codex:

- keep durable guidance close to the code
- reuse task workflows instead of re-explaining them
- record long-running task state in a ledger
- run checks before stopping
- block obviously unsafe commands and leaked secrets
- separate guidance, tools, memory, enforcement, and verification

## Harness Model

- `AGENTS.md`: durable project guidance that should stay small and practical.
- `skills/`: reusable task workflows, each in a directory with `SKILL.md`.
- MCP: the layer for external tools and knowledge access.
- `hooks/`: deterministic scripts that run during the Codex lifecycle.
- `policies/`: permission and safety rule examples.
- `ledger/`: resumable task memory for long-running work.
- `scripts/`: verification and checkpoint utilities.

## Using AGENTS.md Templates

Copy one template from `templates/agents/` into a project as `AGENTS.md`, then edit it down to match the project.

- `strict`: conservative guidance for important repositories.
- `frontend`: frontend-specific expectations for UI, accessibility, and verification.
- `library`: guidance for package/library development.

Keep project guidance durable. Avoid adding one-off task instructions that belong in an issue, prompt, or ledger entry.

For concrete copy commands and setup guidance, see `docs/usage.md`.
For notes on Codex environment configuration boundaries, see `docs/codex-config.md`.
For a step-by-step adoption pass, see `docs/adoption-checklist.md`.

## Using Skills

Skills live under `skills/<name>/SKILL.md`. Each skill contains frontmatter with `name` and `description`, followed by a reusable workflow.

Use skills when a task pattern repeats:

- feature implementation
- bug fixing
- safe refactoring
- release readiness checks
- documentation updates

Install or copy the skills that match your Codex setup. Keep each skill focused on workflow, expected verification, and final reporting.

## Using Hooks

Hooks are deterministic enforcement points. The examples in `hooks/` are intentionally small and are not guaranteed production-ready integrations.

Included examples:

- `secret-guard`: blocks likely secrets in stdin.
- `dangerous-command-guard`: blocks obviously dangerous shell commands in stdin.
- `stop-verify`: runs `scripts/verify.sh` from the repository root.

Adapt them before relying on them in high-risk environments.

## Using Task Ledgers

The `ledger/` templates help long-running tasks survive context loss and handoff.

- `current.md`: active task state and checkpoints.
- `decisions.md`: durable decisions and rationale.
- `risks.md`: known risks and mitigations.
- `verification.md`: commands run and outcomes.

Use `scripts/checkpoint.sh` to append a timestamped checkpoint to `ledger/current.md`.

## Suggested Workflow

1. Start with a small `AGENTS.md`.
2. Pick a skill that matches the task.
3. Record the task in `ledger/current.md`.
4. Work in small steps.
5. Run targeted checks frequently.
6. Update docs and ledger entries as behavior changes.
7. Run `scripts/verify.sh` before finalizing.
8. Summarize changed files, verification, risks, and next steps.

The included GitHub Actions workflow runs the same repository verification script on pushes to `main` and on pull requests.

## Non-Goals

This repository does not:

- implement a multi-agent router
- provide a production hook runtime
- implement an MCP server
- replace project-specific tests or review
- guarantee safety without sandboxing, policy, and human review

## Current Status

This is the first usable version. The repository contains templates and examples designed to be copied, adapted, and tightened for real projects.

The next layer of usefulness is in `examples/`, which shows minimal, frontend, Next.js, and strict target-project layouts for common adoption paths.
