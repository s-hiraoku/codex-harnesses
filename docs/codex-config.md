# Codex Configuration Boundaries

Codex configuration details can vary by environment. This repository should avoid depending on one registration format unless that format is being tested in the target environment.

Use this document to separate reusable harness files from environment-specific wiring.

## Skills

The reusable unit is a directory containing `SKILL.md`.

Recommended options:

- Use APM with `s-hiraoku/codex-harnesses/skills/<skill>` entries in `apm.yml` when project setup should be reproducible for a team.
- Use `gh skill install s-hiraoku/codex-harnesses <skill> --agent codex --scope project` for project-local Codex skills.
- Use `gh skill install s-hiraoku/codex-harnesses <skill> --agent codex --scope user` for user-wide Codex skills.
- Use `npx skills add s-hiraoku/codex-harnesses --agent codex --skill <skill>` as the npm-based installer path.
- If none of these installers are available, copy selected skill directories manually into the skills directory supported by your Codex environment.

Avoid putting project secrets, temporary task state, or repository-specific credentials in skills.

## Hooks

The hook scripts in this repository are payload scripts. They read stdin or run repository commands and return deterministic exit codes.

Registration is intentionally not hard-coded here. A target Codex environment should map lifecycle events to these scripts using its supported configuration mechanism.

For production hardening guidance, see `hook-hardening.md`.

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
