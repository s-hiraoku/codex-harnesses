# Usage

This repository is meant to be copied from selectively, not installed as a framework.

Pick the harness pieces that match your project, place them close to the code they govern, and adapt them until they describe real commands and real risk boundaries.

## Copy a Project Harness

Choose a template from `templates/agents/` and copy it into the target repository as `AGENTS.md`.

```sh
cp templates/agents/strict/AGENTS.md /path/to/project/AGENTS.md
cp scripts/verify.sh /path/to/project/scripts/verify.sh
cp -R ledger /path/to/project/ledger
cp policies/default.yaml /path/to/project/policies/codex.yaml
```

Copy only what the target project needs:

- `templates/agents/strict/AGENTS.md` for conservative repositories
- `templates/agents/frontend/AGENTS.md` for UI-heavy projects
- `templates/agents/library/AGENTS.md` for package/library work
- `scripts/verify.sh` when the project needs a shared verification entrypoint
- `ledger/` when work may be long-running or resumed later
- `policies/` when approval, sandboxing, and verification expectations need to be explicit

Then edit the copied files down. Keep only durable project guidance, stable verification commands, and safety expectations. Temporary task instructions belong in an issue, prompt, or task ledger.

For end-to-end adoption steps, see `docs/adoption-checklist.md`.

## Install Skills

Skills are directories that contain `SKILL.md`.

Prefer one of these three installer paths so source metadata and target agent paths are handled consistently.

### APM

Use APM when a team wants project setup declared in a versioned manifest.

```yaml
# apm.yml
name: your-project
version: 1.0.0
dependencies:
  apm:
    - s-hiraoku/codex-harnesses/skills/feature-implementation
    - s-hiraoku/codex-harnesses/skills/bug-fix
    - s-hiraoku/codex-harnesses/skills/review
```

```sh
apm install
```

### GitHub CLI

```sh
gh skill preview s-hiraoku/codex-harnesses feature-implementation
gh skill install s-hiraoku/codex-harnesses feature-implementation --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses bug-fix --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses review --agent codex --scope project
```

Use `--scope user` instead of `--scope project` when the skills should be available across projects.

### Skills CLI

```sh
npx skills add s-hiraoku/codex-harnesses --list
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation
npx skills add s-hiraoku/codex-harnesses --agent codex --skill bug-fix
npx skills add s-hiraoku/codex-harnesses --agent codex --skill review
```

Use `--global` for user-wide installation:

```sh
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation --global
```

If your environment cannot use these installers, copy selected skill directories manually:

```sh
cp -R skills/feature-implementation /path/to/codex-skills/
cp -R skills/goal-manager /path/to/codex-skills/
cp -R skills/bug-fix /path/to/codex-skills/
cp -R skills/review /path/to/codex-skills/
cp -R skills/pr-guardian /path/to/codex-skills/
```

Install or copy only the skills that match repeated workflows. Use `goal-manager` when a task needs explicit objective tracking across implementation, verification, or PR creation. Do not put repository-specific secrets, credentials, or temporary task state in a skill.

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
