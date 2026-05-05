# Strict Repository Guidance

Use this template for important repositories where safety and review matter.

## Expectations

- Keep changes minimal and directly tied to the task.
- Inspect existing patterns before editing.
- Do not perform destructive git operations without explicit approval.
- Do not bypass tests, hooks, or policy checks.
- Treat generated or example code as untrusted until reviewed.
- Update docs when behavior, commands, configuration, or public APIs change.

## Verification

- Run lint, typecheck, tests, and build when available.
- Record commands that were run and any commands that could not be run.
- Do not claim verification passed unless the command completed successfully.

## Final Response

Summarize changed files, verification results, remaining risks, and follow-up work.

