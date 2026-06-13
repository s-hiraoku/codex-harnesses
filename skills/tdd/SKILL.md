---
name: tdd
description: Drive implementation through red-green-refactor with isolated test design, minimal implementation, and behavior-preserving cleanup.
---

# Test-Driven Development

Use this workflow when the user wants new behavior developed under TDD discipline, or when a risky behavior change benefits from a failing test before implementation.

## Workflow

1. Specify the behavior in one or two concrete sentences and identify the test framework.
2. Red: write one focused test that captures the requested behavior. Prefer existing test patterns and fixtures. Run it and confirm it fails for the expected reason.
3. Green: implement the smallest code change that makes the failing test pass. Avoid speculative options, broad rewrites, or unrelated cleanup.
4. Run the focused test. If it still fails, fix the implementation rather than weakening the test unless the test contradicts the stated behavior.
5. Refactor: clean only the code introduced or directly touched by the change. Preserve public APIs, return values, side effects, and data formats.
6. Run the focused test again, then related tests for the touched area.
7. Repeat the loop for each distinct behavior instead of writing a broad test batch up front.

When subagents are available, keep phases isolated: pass the behavior only to a test-writing subagent, pass the failing test only to an implementation subagent, and pass the green code only to a refactoring subagent.

## Final Report

Include:

- behavior implemented
- red test added or updated
- implementation files changed
- refactor changes applied
- tests run and result
- remaining risks or follow-up tests
