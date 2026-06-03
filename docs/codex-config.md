# Codex Configuration Boundaries

Codex configuration details can vary by environment. This repository should avoid depending on one registration format unless that format is being tested in the target environment.

Use this document to separate reusable harness files from environment-specific wiring.

## Plugin And Skills

The reusable unit is the `codex-harnesses` plugin exposed by `marketplace.json`.

Recommended options:

- Use `codex plugin marketplace add /path/to/codex-harnesses` for a local checkout.
- Install `codex-harnesses` from the Codex plugin marketplace UI.
- If plugin installation is unavailable, copy selected skill directories from `plugins/codex-harnesses/skills/` into the skills directory supported by your Codex environment.

Avoid putting project secrets, temporary task state, or repository-specific credentials in skills.

## Hooks

The hook scripts in this repository are payload scripts. They read stdin or run repository commands and return deterministic exit codes.

Registration is intentionally not hard-coded here. A target Codex environment should map lifecycle events to these scripts using its supported configuration mechanism.

For production hardening guidance, see `hook-hardening.md`.

Useful payloads:

- `plugins/codex-harnesses/hooks/secret-guard/hook.py`: scan proposed text for likely secrets
- `plugins/codex-harnesses/hooks/dangerous-command-guard/hook.py`: scan proposed shell commands for obvious danger
- `plugins/codex-harnesses/hooks/stop-verify/hook.py`: run `scripts/verify.sh` before stopping

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
