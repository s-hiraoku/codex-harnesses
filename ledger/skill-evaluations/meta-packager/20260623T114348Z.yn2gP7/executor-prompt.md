# Executor prompt template

You are an executor reading meta-packager with a blank slate.

## Target prompt

Read the full target skill at:

`/Volumes/SSD/ghq/github.com/s-hiraoku/codex-harnesses/skills/meta-packager/SKILL.md`

## Scenario

Paste one scenario from `scenarios.md`.

## Requirements checklist

Paste that scenario's checklist. Do not add or remove [critical] tags.

## Task

1. Follow the target prompt to execute the scenario and produce the deliverable.
2. On completion, respond with the report structure below.

## Report structure

- Deliverable: <artifact or execution summary>
- Requirement achievement: ○ / × / partial, with reason for each item
- Trace:
  - Use `Trace: all OK` only when Understanding, Planning, Execution, and Formatting are all OK.
  - Otherwise list each phase with OK / stuck / skipped and a one-line reason.
- Unclear points (structured): for each issue, include Issue / Cause / General Fix Rule.
- Discretionary fill-ins: places not fixed by the instruction and filled by judgment.
- Retries: number of times the same decision was redone and why.
