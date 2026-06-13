---
name: fix-ci
description: Diagnose and repair failing CI checks on the current branch or pull request with focused, reproducible fixes.
---

# Fix CI

Use this workflow when CI is failing for a branch or pull request and the goal is to get checks green or identify a real blocker.

## Workflow

1. Identify the branch, pull request, and failing checks. Use local tools, GitHub tooling, or the available GitHub connector.
2. Fetch the failing job output. For GitHub Actions, prefer `gh pr checks`, `gh run list --branch <branch> --limit 5`, and `gh run view <run-id> --log-failed` when available.
3. Cluster failures by type:
   - build or type errors
   - lint or format errors
   - test failures
   - dependency or lockfile drift
   - environment, runner, or network failures
4. Reproduce locally when practical with the narrowest matching command.
5. Apply the smallest fix for one cluster at a time. Do not bundle unrelated cleanup.
6. Never disable, delete, or skip a test as the fix unless the user explicitly authorizes it.
7. Re-run the local failing command, then broader verification when practical.
8. Push focused updates if working on a PR and re-check CI. Stop when failures repeat without changing mode, or when the blocker is outside the repository.

## Final Report

Include:

- failing checks at start
- failure clusters identified
- fixes applied
- local verification run
- final CI status when checked
- remaining failures classified as real, flaky, or environmental
