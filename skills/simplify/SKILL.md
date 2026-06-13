---
name: simplify
description: Remove avoidable complexity from changed code while preserving behavior exactly.
---

# Simplify

Use this workflow after a feature or bug fix works, but before review or release, to reduce unnecessary complexity introduced during the change.

## Workflow

1. Identify the changed files and public behavior that must remain unchanged.
2. For each non-trivial changed file, check whether the change added:
   - helpers used only once
   - abstractions without a second caller
   - validation for impossible states
   - unused imports, variables, branches, flags, or configuration
   - comments that restate code instead of explaining intent
   - duplicated logic that an existing local helper already handles
3. Search before introducing or keeping a helper; prefer established project patterns.
4. Apply minimal cleanup only when behavior is clearly unchanged.
5. Leave risky cleanup as a proposal instead of applying it.
6. Re-run targeted tests for each touched area.

## Final Report

Include:

- files simplified
- specific complexity removed
- behavior-preservation checks run
- cleanup proposals intentionally left unapplied
- residual risks
