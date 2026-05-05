# Harness Model

This repository uses a simple separation of responsibilities.

## AGENTS.md

`AGENTS.md` is durable project guidance. It should describe stable conventions, verification commands, safety expectations, and repository-specific practices.

It should not become a task tracker or a dumping ground for temporary instructions.

## Skills

Skills are reusable workflows. A skill belongs in `skills/<name>/SKILL.md` and should include frontmatter with `name` and `description`.

Use skills for repeated task types such as feature work, bug fixing, refactoring, release checks, documentation updates, code review, and post-PR follow-up.

## MCP

MCP is the external tools and knowledge layer. It is where Codex can access systems such as GitHub, documentation, browser automation, local repo tools, or memory stores.

This repository documents MCP strategy but does not implement an MCP server.

## Hooks

Hooks are deterministic lifecycle enforcement points. They are useful for blocking likely secrets, stopping dangerous commands, or requiring verification before a session ends.

Hooks should be treated as code, tested like code, and documented with clear failure modes.

## Policies

Policies describe permission and safety rules. They should make approval, sandboxing, verification, and git-risk expectations explicit.

## Task Ledger

The task ledger is resumable task memory. It records current state, decisions, risks, and verification results so work can continue after a long run, interruption, or context loss.

## Verification

Verification is the repeatable lint, typecheck, test, and build loop. Prefer commands that fail loudly and deterministically over instructions that rely on the model remembering to check.
