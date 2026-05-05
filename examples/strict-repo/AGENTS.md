# Strict Repository Guidance

Keep changes minimal, reviewable, and directly tied to the task.

Rules:

- do not perform destructive git operations without explicit approval
- preserve public APIs unless a breaking change is requested
- update docs for behavior, command, configuration, or API changes
- treat hooks and generated code as untrusted until reviewed
- prefer worktrees for risky experiments

Before finalizing:

- run lint, typecheck, tests, and build when available
- record commands that could not be run
- summarize changed files, verification, risks, and migration notes

