# Usage

This repository is meant to be copied from, not installed as a framework.

Pick the harness pieces that match your project, place them close to the code they govern, and adapt them until they describe real commands and real risk boundaries.

## Copy an AGENTS.md Template

Choose a template from `templates/agents/` and copy it into the target repository as `AGENTS.md`.

```sh
cp templates/agents/strict/AGENTS.md /path/to/project/AGENTS.md
```

Then edit it down. Keep only durable project guidance, stable verification commands, and safety expectations. Temporary task instructions belong in an issue, prompt, or task ledger.

For end-to-end adoption steps, see `docs/adoption-checklist.md`.

## Install Skills

Skills are directories that contain `SKILL.md`.

Codex environments may load skills differently. If your environment supports a global skills directory, copy selected skills there. If not, keep them project-local and reference them from your project guidance.

```sh
cp -R skills/feature-implementation /path/to/codex-skills/
cp -R skills/bug-fix /path/to/codex-skills/
cp -R skills/review /path/to/codex-skills/
```

Use skills for repeated workflows. Do not put repository-specific secrets, credentials, or temporary task state in a skill.

## Configure Hooks

Hooks in this repository are examples. They do not auto-register with Codex when copied into a project. Wire them into your Codex lifecycle only after reviewing and adapting them.

Typical use:

```sh
printf '%s\n' "$TEXT_TO_SCAN" | python3 hooks/secret-guard/hook.py
printf '%s\n' "$COMMAND_TO_SCAN" | python3 hooks/dangerous-command-guard/hook.py
python3 hooks/stop-verify/hook.py
```

Hook registration depends on your Codex environment. Treat these scripts as the deterministic payload that a lifecycle hook can call.

For the boundary between payload scripts and environment-specific registration, see `docs/codex-config.md`.

## Use Policies

Policy files in `policies/` are human-readable examples for approval, sandboxing, guards, verification, and git behavior.

Copy one into the target project and adapt it:

```sh
cp policies/default.yaml /path/to/project/policies/codex.yaml
```

The policy schema in `schemas/policy.schema.json` can be used by editors or validation tooling.

## Use the Task Ledger

Copy the `ledger/` templates into the target project when a task may run for a long time or be resumed later.

```sh
cp -R ledger /path/to/project/ledger
```

Update `ledger/current.md` before pausing, after major decisions, and before risky edits. Record meaningful check results in `ledger/verification.md` when future sessions or reviewers should trust them. Use `scripts/checkpoint.sh` to append branch, status, and commit context.

## Run Verification

Copy `scripts/verify.sh` into the target project, then adapt it to the project commands.

```sh
bash scripts/verify.sh
```

For stricter failure behavior, set:

```sh
CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh
```

Strict mode fails when project files are detected but no supported verification commands are available.

Run the same script from CI so local and pull request verification stay aligned. A minimal GitHub Actions job looks like:

```yaml
name: Verify

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh
```

## Recommended Workflow for a New Task

1. Copy or update `AGENTS.md`.
2. Pick a matching skill.
3. Record the goal and next step in `ledger/current.md`.
4. Work in small steps.
5. Run targeted checks after meaningful edits.
6. Update docs and ledger entries when behavior changes.
7. Run `bash scripts/verify.sh` before finalizing.
8. Report changed files, checks, risks, and next steps.
