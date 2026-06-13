---
name: deslop
description: Remove common AI-generated boilerplate and readability noise from changed code without changing behavior.
---

# Deslop

Use this workflow when code on the current branch contains visibly generated boilerplate that makes maintenance harder but does not represent real behavior.

## Workflow

1. List changed files and read the diff before editing.
2. Look for common slop signatures:
   - comments that restate the next line
   - broad `except Exception` wrappers that add no handling
   - private docstrings longer than the code they describe
   - "helper" functions used exactly once
   - defensive checks for states the type system or caller contract rules out
   - conversation-bound comments such as "added for this issue"
   - verbose variable names that obscure simple logic
3. Preserve genuine boundary handling for HTTP, subprocesses, file IO, parsing, and user input.
4. Remove only noise whose behavior impact is clearly zero.
5. Run targeted tests or checks for the touched files.
6. If a removal might change observability or error behavior, leave it as a proposal.

## Final Report

Include:

- files cleaned
- slop categories removed
- tests or checks run
- proposals not applied
- residual risks
