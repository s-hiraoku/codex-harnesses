# codex-harnesses

[![Verify](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/verify.yml/badge.svg)](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/verify.yml)
[![GitHub Pages](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/pages.yml/badge.svg)](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/pages.yml)

`codex-harnesses` is a collection of practical harnesses for long-running, reliable, safe, and high-quality Codex-driven software development.

Codex should not be expected to succeed by intelligence alone.

This repository provides reusable examples for project guidance, task workflows, deterministic lifecycle checks, safety policies, task ledgers, and verification loops. It is a harness collection, not a multi-agent router.

## Quick Start

1. Add this repository as a Codex plugin marketplace.
2. Install the `codex-harnesses` plugin from that marketplace.
3. Pick a starting shape from `examples/`.
4. Copy the matching `AGENTS.md`, `scripts/verify.sh`, policy, and ledger files into your project.
5. Replace generic verification commands with real project commands.
6. Add only the hook examples that match repeated work and have been reviewed.
7. Run one small real task through the harness and tighten anything that was vague.

For a local checkout, add the marketplace root:

```sh
codex plugin marketplace add /path/to/codex-harnesses
```

The marketplace manifest is `marketplace.json`, and it exposes `plugins/codex-harnesses`.

The GitHub Pages user guide lives in `docs/` and is built with MkDocs. Once Pages is enabled with GitHub Actions as the source, it publishes to [s-hiraoku.github.io/codex-harnesses](https://s-hiraoku.github.io/codex-harnesses/).

For plugin installation details, see `docs/plugin-marketplace.md`.
For a detailed adoption pass, see `docs/adoption-checklist.md`.

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
- `marketplace.json`: Codex marketplace manifest for installing the plugin.
- `plugins/codex-harnesses/`: installable Codex plugin containing reusable workflows and examples.
- `plugins/codex-harnesses/skills/`: reusable task workflows, each in a directory with `SKILL.md`.
- MCP: the layer for external tools and knowledge access, including diagramming tools such as Excalidraw.
- `plugins/codex-harnesses/hooks/`: deterministic example scripts that can be wired into the Codex lifecycle.
- `policies/`: permission and safety rule examples.
- `ledger/`: resumable task memory for long-running work.
- `scripts/`: verification and checkpoint utilities.

## Using AGENTS.md Templates

Copy one template from `templates/agents/` into a project as `AGENTS.md`, then edit it down to match the project.

- `strict`: conservative guidance for important repositories.
- `frontend`: frontend-specific expectations for UI, accessibility, and verification.
- `library`: guidance for package/library development.

Keep project guidance durable. Avoid adding one-off task instructions that belong in an issue, prompt, or ledger entry.

For concrete setup guidance, see `docs/usage.md`.
For notes on Codex environment configuration boundaries, see `docs/codex-config.md`.
For a step-by-step adoption pass, see `docs/adoption-checklist.md`.
For long-running task memory patterns, see `docs/task-ledger-patterns.md`.

## Using The Plugin

The installable plugin lives at `plugins/codex-harnesses` and is exposed by `marketplace.json`. Skills live under `plugins/codex-harnesses/skills/<name>/SKILL.md`. Each skill contains frontmatter with `name` and `description`, followed by a reusable workflow.

Use skills when a task pattern repeats:

- feature implementation
- goal management for long-running or PR-bound work
- bug fixing
- safe refactoring
- release readiness checks
- documentation updates
- code review
- post-PR CI and review follow-up
- Excalidraw blog diagram creation and export
- meta-analysis that packages repeated Codex work into reusable assets

After opening a PR, run the `pr-guardian` workflow by default to monitor checks and address actionable feedback until the PR is mergeable or a blocker is documented.

Run the `meta-packager` workflow after enough real Codex sessions have accumulated to identify repeated work. It inspects recent sessions, memories, and existing assets, then creates only high-confidence skills, subagents, or automations.

Install the `codex-harnesses` plugin from the marketplace and enable only the workflows that match repeated work. Keep each skill focused on workflow, expected verification, and final reporting.

## Using Hooks

Hooks are deterministic enforcement points. The examples in `plugins/codex-harnesses/hooks/` are intentionally small and are not guaranteed production-ready integrations.
They are payload scripts, not automatic Codex lifecycle registration. Copying this repository does not make them run by itself; the target Codex environment must explicitly wire each script to the lifecycle event that should call it.

Included examples:

- `secret-guard`: blocks likely secrets in stdin.
- `dangerous-command-guard`: blocks obviously dangerous shell commands in stdin.
- `stop-verify`: runs `scripts/verify.sh` from the repository root.

Adapt them before relying on them in high-risk environments.

For production hardening guidance, see `docs/hook-hardening.md`.

## Using Task Ledgers

The `ledger/` templates help long-running tasks survive context loss and handoff.

- `current.md`: active task state and checkpoints.
- `decisions.md`: durable decisions and rationale.
- `risks.md`: known risks and mitigations.
- `verification.md`: commands run and outcomes.

Use `scripts/checkpoint.sh` to append a timestamped checkpoint to `ledger/current.md`.
For small one-shot edits, a final verification summary may be enough. For larger, security-sensitive, risky, or interrupted work, update the ledger as part of the workflow so future sessions can continue from recorded state instead of chat history.

For operating patterns, see `docs/task-ledger-patterns.md`.

## Suggested Workflow

1. Start with a small `AGENTS.md`.
2. Pick a skill that matches the task.
3. Record the task in `ledger/current.md`.
4. Work in small steps.
5. Run targeted checks frequently.
6. Update docs and ledger entries as behavior changes.
7. Run `scripts/verify.sh` before finalizing.
8. Summarize changed files, verification, risks, and next steps.

The included GitHub Actions workflow runs the same repository verification script on pushes to `main` and on pull requests. When copying this harness into another repository, keep local and CI verification aligned by running the project-adapted `scripts/verify.sh` from CI as well.

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
