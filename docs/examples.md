# Examples

The `examples/` directory contains copyable starting shapes for target repositories.

## Minimal Codex Project

Path: `examples/minimal-codex-project/`

Use this when a project only needs:

- `AGENTS.md`
- a small task ledger at `.codex/tasks/current.md`

This is the lightest adoption path.

## Frontend Project

Path: `examples/frontend-project/`

Use this for UI-heavy projects that need:

- frontend-focused `AGENTS.md`
- a `scripts/verify.sh` placeholder for lint, typecheck, tests, and build
- browser and viewport verification expectations

Replace the placeholder verification script with the project’s real package manager commands.

## Next.js Project

Path: `examples/nextjs-project/`

Use this for Next.js applications that need:

- server/client component boundary guidance
- route handler and server action safety expectations
- environment variable caution
- package-manager-aware verification
- project-local task ledger
- balanced policy example

## Strict Repository

Path: `examples/strict-repo/`

Use this for important repositories where unsafe edits, skipped verification, or destructive git operations would be costly.

It includes:

- conservative `AGENTS.md`
- strict policy example

## How to Choose

Start with the smallest example that covers the real risk.

Do not copy every harness file by default. A small accurate harness is better than a large stale one.

