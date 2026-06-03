# Harness Model

This repository uses a simple separation of responsibilities.

## AGENTS.md

`AGENTS.md` is durable project guidance. It should describe stable conventions, verification commands, safety expectations, and repository-specific practices.

It should not become a task tracker or a dumping ground for temporary instructions.

## Skills

Skills are reusable workflows. In this repository they are packaged inside the installable plugin at `plugins/codex-harnesses/skills/<name>/SKILL.md` and should include frontmatter with `name` and `description`.

Use skills for repeated task types such as feature work, bug fixing, refactoring, release checks, documentation updates, code review, and post-PR follow-up.

## Plugin Marketplace

`marketplace.json` exposes `plugins/codex-harnesses` as an installable Codex plugin. The marketplace is the preferred distribution path for the reusable workflows. The rest of the repository remains a copyable harness kit for project-local guidance, policies, ledgers, scripts, and examples.

## MCP

MCP is the external tools and knowledge layer. It is where Codex can access systems such as GitHub, documentation, browser automation, local repo tools, or memory stores.

This repository documents MCP strategy but does not implement an MCP server.

## Hooks

Hooks are deterministic lifecycle enforcement points. The plugin includes hook payload examples under `plugins/codex-harnesses/hooks/`. They are useful for blocking likely secrets, stopping dangerous commands, or requiring verification before a session ends.

Hooks should be treated as code, tested like code, and documented with clear failure modes.

## Policies

Policies describe permission and safety rules. They should make approval, sandboxing, verification, and git-risk expectations explicit.

## Task Ledger

The task ledger is resumable task memory. It records current state, decisions, risks, and verification results so work can continue after a long run, interruption, or context loss.

## Verification

Verification is the repeatable lint, typecheck, test, and build loop. Prefer commands that fail loudly and deterministically over instructions that rely on the model remembering to check.
