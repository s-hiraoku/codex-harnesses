# Usage

This repository is meant to be deployed from selectively, not installed as a framework.

Pick the harness pieces that match your project, place them close to the code they govern, and adapt them until they describe real commands and real risk boundaries.

## Deploy a Project Harness

Use `scripts/install.sh` from a local checkout of this repository:

```sh
scripts/install.sh --target /path/to/project --agents strict --skills feature-implementation,bug-fix,review --ledger --policy default
```

With GitHub CLI:

```sh
gh repo clone s-hiraoku/codex-harnesses /tmp/codex-harnesses
/tmp/codex-harnesses/scripts/install.sh --target /path/to/project --agents strict --skills feature-implementation,bug-fix,review --ledger --policy default
```

The installer is intentionally small. It copies selected files into the target project, skips existing files by default, and supports `--dry-run` and `--force`.

Common options:

```sh
scripts/install.sh --target . --agents frontend --skills all --ledger --policy default
scripts/install.sh --target . --agents library --no-verify --skills release-check,docs-updater
scripts/install.sh --target . --hooks secret-guard,dangerous-command-guard
```

Then edit the deployed files down. Keep only durable project guidance, stable verification commands, and safety expectations. Temporary task instructions belong in an issue, prompt, or task ledger.

For end-to-end adoption steps, see `docs/adoption-checklist.md`.

## Install Skills

Skills are directories that contain `SKILL.md`.

Codex environments may load skills differently. If your environment supports a global skills directory, install selected skills there. If not, keep them project-local and reference them from your project guidance.

```sh
<<<<<<< codex/deployable-harness-installer
scripts/skills.sh --target /path/to/codex-skills feature-implementation bug-fix review
=======
cp -R skills/feature-implementation /path/to/codex-skills/
cp -R skills/goal-manager /path/to/codex-skills/
cp -R skills/bug-fix /path/to/codex-skills/
cp -R skills/review /path/to/codex-skills/
cp -R skills/pr-guardian /path/to/codex-skills/
>>>>>>> main
```

Use skills for repeated workflows. Use `goal-manager` when a task needs explicit objective tracking across implementation, verification, or PR creation. Do not put repository-specific secrets, credentials, or temporary task state in a skill.

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

Install one into the target project and adapt it:

```sh
scripts/install.sh --target /path/to/project --no-agents --no-verify --policy default
```

The policy schema in `schemas/policy.schema.json` can be used by editors or validation tooling.

## Use the Task Ledger

Install the `ledger/` templates into the target project when a task may run for a long time or be resumed later.

```sh
scripts/install.sh --target /path/to/project --no-agents --no-verify --ledger
```

Update `ledger/current.md` before pausing, after major decisions, and before risky edits. Record meaningful check results in `ledger/verification.md` when future sessions or reviewers should trust them. Use `scripts/checkpoint.sh` to append branch, status, and commit context.

## Run Verification

Deploy `scripts/verify.sh` into the target project, then adapt it to the project commands.

```sh
bash scripts/verify.sh
```

For stricter failure behavior, set:

```sh
CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh
```

Strict mode fails when project files are detected but no supported verification commands are available.

Run the same script from CI so local and pull request verification stay aligned. Install the tools that `scripts/verify.sh` expects before running strict mode. A minimal Python-based GitHub Actions job looks like:

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
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install verification dependencies
        run: python -m pip install -r requirements-dev.txt

      - name: Run repository verification
        run: CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh
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
