# Repository Guidance

This repository contains harness examples for Codex-driven software development. Keep changes concise, practical, and developer-facing.

## Principles

- Prefer deterministic checks over vague instructions.
- Separate durable guidance, reusable workflows, external tools, task memory, enforcement, and verification.
- Keep `AGENTS.md` templates small enough to remain useful over time.
- Treat hooks as examples unless they are explicitly hardened and integrated.
- Do not describe this repository as a multi-agent router.

## Editing Expectations

- Update `README.md` or `docs/` when adding or changing harness concepts.
- Keep skill files focused on reusable task workflows.
- Keep policy examples readable and conservative by default.
- Avoid over-engineering. This repository should remain easy to copy from.

## Verification

- Run relevant checks before finalizing changes.
- Prefer `bash scripts/verify.sh` as the repository-level check.
- Summarize changed files, verification results, and known risks in the final response.

