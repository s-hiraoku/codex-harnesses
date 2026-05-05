# Contributing

This repository is a harness collection for Codex-driven software development. Contributions should keep the repository practical, copyable, and easy to verify.

## What Fits

Good contributions include:

- concise `AGENTS.md` templates
- focused skills with valid `SKILL.md` frontmatter
- hook examples with clear limits and tests
- policy examples that validate against `schemas/policy.schema.json`
- ledger templates and operating patterns
- verification scripts and tests that prevent template drift
- docs that clarify how to adopt or safely adapt the harnesses

Avoid adding a multi-agent router, production hook runtime, or broad framework unless the repository scope changes explicitly.

## Change Guidelines

- Keep examples small enough to copy.
- Keep docs concise and developer-facing.
- Prefer deterministic checks over prose-only expectations.
- Make limits explicit, especially for safety and security examples.
- Update README or docs when adding a new harness type or adoption path.
- Add or update tests when changing hooks, policies, examples, skills, scripts, or docs links.

## Verification

Before proposing a change, run:

```sh
CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh
```

For local development, install dev dependencies first:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Then run:

```sh
.venv/bin/ruff check .
.venv/bin/pytest
```

Do not claim verification passed unless the command completed successfully.

## Skill Changes

Each skill must live in `skills/<name>/SKILL.md` and include frontmatter with:

```yaml
---
name: <name>
description: <when to use this skill>
---
```

Keep skill bodies focused on workflow, verification, and final reporting.

## Hook Changes

Hooks in this repository are examples. When adding or changing a hook:

- document what it blocks and what it does not block
- avoid printing secret values
- return deterministic exit codes
- add tests for allowed and blocked cases
- update `docs/hook-hardening.md` if the hardening guidance changes

## Policy Changes

Policy examples must validate against `schemas/policy.schema.json`. If the policy shape changes, update the schema and tests in the same change.

