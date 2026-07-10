# codex-harnesses

[![Verify](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/verify.yml/badge.svg)](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/verify.yml)
[![GitHub Pages](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/pages.yml/badge.svg)](https://github.com/s-hiraoku/codex-harnesses/actions/workflows/pages.yml)

`codex-harnesses` is a collection of practical harnesses for long-running, reliable, safe, and high-quality Codex-driven software development.

Codex should not be expected to succeed by intelligence alone.

This repository provides reusable examples for project guidance, task workflows, deterministic lifecycle checks, safety policies, task ledgers, and verification loops. It is a harness collection, not a multi-agent router.

## Quick Start

1. Pick a starting shape from `examples/`.
2. Copy the matching `AGENTS.md`, `scripts/verify.sh`, policy, and ledger files into your project.
3. Install only the skills that match repeated work with APM, `gh skill`, or `npx skills`.
4. Replace generic verification commands with real project commands.
5. Add only the hooks that match repeated work and have been reviewed.
6. Run one small real task through the harness and tighten anything that was vague.

For skills, use one of the recommended installer paths:

```sh
apm install s-hiraoku/codex-harnesses/skills/feature-implementation
gh skill install s-hiraoku/codex-harnesses feature-implementation --agent codex --scope project
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation
```

The GitHub Pages user guide lives in `docs/` and is built with MkDocs. Once Pages is enabled with GitHub Actions as the source, it publishes to [s-hiraoku.github.io/codex-harnesses](https://s-hiraoku.github.io/codex-harnesses/).

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

For concrete setup guidance, see `docs/usage.md`.
For notes on Codex environment configuration boundaries, see `docs/codex-config.md`.
For a step-by-step adoption pass, see `docs/adoption-checklist.md`.
For long-running task memory patterns, see `docs/task-ledger-patterns.md`.

## Using Skills

Skills live under `skills/<name>/SKILL.md`. Each skill contains frontmatter with `name` and `description`, followed by a reusable workflow.

Use skills when a task pattern repeats:

- feature implementation
- frontend design and UI usability work
- implementation delivery from plan to merge-ready PR
- continuous product evaluation and approved improvement loops
- goal management for long-running or PR-bound work
- bug fixing
- safe refactoring
- release readiness checks
- documentation updates
- code review
- security review
- test-driven development
- CI repair
- simplification and deslop cleanup after implementation
- reading public URLs that normal tools cannot parse cleanly with Jina Reader
- image-generated UI direction before frontend implementation
- post-PR CI and review follow-up
- meta-analysis that packages repeated Codex work into reusable assets
- independent Adviser consultations before consequential decisions and completion

After opening a PR, run the `pr-guardian` workflow by default to monitor checks and address actionable feedback until the PR is mergeable or a blocker is documented.

Run the `meta-packager` workflow after enough real Codex sessions have accumulated to identify repeated work. It inspects recent sessions, memories, and existing assets, then proposes the smallest useful skill, subagent, hook, or automation. Create only explicitly approved high-confidence items.

Install only the skills that match your repeated work. Keep each skill focused on workflow, expected verification, and final reporting.

Recommended install methods:

1. APM, for teams that want one project manifest:

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

2. GitHub CLI, for installing a named skill directly:

```sh
gh skill preview s-hiraoku/codex-harnesses feature-implementation
gh skill install s-hiraoku/codex-harnesses feature-implementation --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses frontend-design --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses implement-to-merge-ready --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses kaizen-loop --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses adviser --agent codex --scope project
```

Use `--scope user` instead of `--scope project` when the skills should be available across projects.

3. Skills CLI, for an npm-based installer path:

```sh
npx skills add s-hiraoku/codex-harnesses --list
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation
npx skills add s-hiraoku/codex-harnesses --agent codex --skill frontend-design
npx skills add s-hiraoku/codex-harnesses --agent codex --skill implement-to-merge-ready
npx skills add s-hiraoku/codex-harnesses --agent codex --skill kaizen-loop
npx skills add s-hiraoku/codex-harnesses --agent codex --skill adviser
```

Use `--global` for user-wide installation. Repeat the chosen command for other skills such as `goal-manager`, `adviser`, `bug-fix`, `review`, `security-review`, `tdd`, `fix-ci`, `simplify`, `deslop`, `jina-reader`, `jina-read-url`, `ui-imagegen-director`, `refactor-safely`, `release-check`, `docs-updater`, `pr-guardian`, and `meta-packager`. Use `adviser` for Claude Code `/advisor`-style independent consultations around important decisions and completion. Use `kaizen-loop` when Codex should evaluate a product, propose improvements, and implement only user-approved changes.

For Vercel or Next.js frontend projects, pair this harness with Vercel's official frontend skills instead of copying them into this repository:

```sh
npx skills add vercel-labs/agent-skills --global --agent codex --skill vercel-react-best-practices vercel-composition-patterns vercel-react-view-transitions web-design-guidelines
npx skills add vercel-labs/next-skills --global --agent codex --skill next-best-practices
```

Add `next-cache-components` or `next-upgrade` from `vercel-labs/next-skills` only when that project is actively using Next.js 16 cache components or running a framework upgrade.

## Using MCP Recipes

This repository includes a disabled-by-default MCP starter recipe at `mcp/recipes/curated.mcp.json` with entries for GitHub, Playwright, Context7, Serena, Sequential Thinking, and Sentry.

Copy it into a target project's MCP configuration and move only the servers you need from `_disabled` into `mcpServers`. See `docs/mcp-recipes.md` for auth, permission, and usage notes.

### Evaluating Skills

Use `empirical-prompt-tuning` after creating or substantially revising a skill. It evaluates the instruction with fresh executors, fixed scenarios, and a failure-pattern ledger so changes are based on observed ambiguity instead of author preference.

Generate an evaluation pack for a target skill:

```sh
scripts/evaluate-skill.sh skills/feature-implementation
```

The pack is written under `ledger/skill-evaluations/<skill>/<timestamp>/` with scenario, executor prompt, results, and failure-ledger templates. Fill in baseline scenarios plus a hold-out convergence scenario, dispatch a fresh executor per baseline scenario, then record the metrics and apply one theme of fixes per iteration.

## Using Hooks

Hooks are deterministic enforcement points. The examples in `hooks/` are intentionally small and are not guaranteed production-ready integrations.
They are payload scripts, not automatic Codex lifecycle registration. Copying this repository does not make them run by itself; the target Codex environment must explicitly wire each script to the lifecycle event that should call it.

Included examples:

- `secret-guard`: blocks likely secrets in stdin.
- `dangerous-command-guard`: blocks obviously dangerous shell commands in stdin.
- `branch-protection-guard`: blocks direct git writes to protected branches.
- `prompt-injection-detector`: flags common prompt-injection phrases in stdin.
- `mcp-tool-allowlist`: blocks MCP tool names outside an explicit allowlist.
- `cost-ceiling-guard`: caps cumulative tool calls in a rolling window.
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
