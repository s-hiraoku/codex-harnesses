# Codex Configuration Boundaries

Codex configuration details can vary by environment. This repository should avoid depending on one registration format unless that format is being tested in the target environment.

Use this document to separate reusable harness files from environment-specific wiring.

## Skills

The reusable unit is a directory containing `SKILL.md`.

Recommended options:

- If your environment supports a global skills directory, copy selected skill directories there.
- If your environment supports project-local skills, keep selected skills inside the project and reference them from `AGENTS.md`.
- If neither is available, keep the skill text as a reusable workflow document and ask Codex to follow it explicitly.

Avoid putting project secrets, temporary task state, or repository-specific credentials in skills.

## Hooks

The hook scripts in this repository are payload scripts. They read stdin or run repository commands and return deterministic exit codes.

Registration is intentionally not hard-coded here. A target Codex environment should map lifecycle events to these scripts using its supported configuration mechanism.

Useful payloads:

- `hooks/secret-guard/hook.py`: scan proposed text for likely secrets
- `hooks/dangerous-command-guard/hook.py`: scan proposed shell commands for obvious danger
- `hooks/stop-verify/hook.py`: run `scripts/verify.sh` before stopping

## Policies

Policy files are examples of approval, sandboxing, guards, verification, and git expectations. They are useful as:

- human-readable repository policy
- editor-validated YAML using `schemas/policy.schema.json`
- input to future automation

Do not assume a policy file is enforced unless a target environment or hook explicitly reads and applies it.

## Task Ledger

The task ledger is repository-local task memory. Keep it near the project being changed, not in a global Codex configuration directory.

For long-running work, update the ledger before pausing and after decisions, risky edits, and verification runs.

## Verification

`scripts/verify.sh` is intended to be copied into a target project and adapted. In this repository, CI runs it in strict mode so missing verification tooling does not look like a passing test run.

