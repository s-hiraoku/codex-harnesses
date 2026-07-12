# Usage

This repository is meant to be copied from selectively, not installed as a framework.

Pick the harness pieces that match your project, place them close to the code they govern, and adapt them until they describe real commands and real risk boundaries.

## Copy a Project Harness

Choose a template from `templates/agents/` and copy it into the target repository as `AGENTS.md`.

```sh
mkdir -p /path/to/project/scripts /path/to/project/policies
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
gh skill install s-hiraoku/codex-harnesses frontend-design --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses implement-to-merge-ready --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses kaizen-loop --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses ui-imagegen-director --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses bug-fix --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses review --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses jina-reader --agent codex --scope project
gh skill install s-hiraoku/codex-harnesses jina-read-url --agent codex --scope project
```

Use `--scope user` instead of `--scope project` when the skills should be available across projects.

### Skills CLI

```sh
npx skills add s-hiraoku/codex-harnesses --list
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation
npx skills add s-hiraoku/codex-harnesses --agent codex --skill frontend-design
npx skills add s-hiraoku/codex-harnesses --agent codex --skill implement-to-merge-ready
npx skills add s-hiraoku/codex-harnesses --agent codex --skill kaizen-loop
npx skills add s-hiraoku/codex-harnesses --agent codex --skill ui-imagegen-director
npx skills add s-hiraoku/codex-harnesses --agent codex --skill bug-fix
npx skills add s-hiraoku/codex-harnesses --agent codex --skill review
npx skills add s-hiraoku/codex-harnesses --agent codex --skill jina-reader
npx skills add s-hiraoku/codex-harnesses --agent codex --skill jina-read-url
```

Use `--global` for user-wide installation:

```sh
npx skills add s-hiraoku/codex-harnesses --agent codex --skill feature-implementation --global
```

### Enable automatic Adviser timing

Skill installation alone does not guarantee that Codex will invoke `adviser` on tasks that never mention it. Add this standing instruction to the user-global `~/.codex/AGENTS.md` after installing the skill:

```md
## Adviser

For consequential work that takes more than a few steps, consider the globally installed `$adviser` skill at important decision points. Typical high-value checkpoints are after orientation but before committing to an approach, and after the deliverable is durable and verified but before declaring completion. These are defaults, not a fixed call quota.

Also consult Adviser when material ambiguity blocks a decision, failures recur, the approach stops converging, or a materially different direction is under consideration. Skip ritual consultations for short reactive work whose next action is already dictated by fresh tool output.

Keep the main agent responsible for execution and weigh Adviser output against repository evidence, primary sources, and empirical verification. Do not assume the fallback reviewer received a complete transcript or uses a stronger model; report those capabilities only when verified.
```

This reproduces the native Advisor timing pattern more closely while keeping timing model-driven and short mechanical tasks free of unnecessary consultations. The skill emulates the workflow, not native server-side transcript delivery, billing, caching, or UI.

### Companion Skills for Vercel Frontends

For React, Next.js, and Vercel-hosted frontend work, install Vercel's official skills alongside the local harness skills:

```sh
npx skills add vercel-labs/agent-skills --global --agent codex --skill vercel-react-best-practices vercel-composition-patterns vercel-react-view-transitions web-design-guidelines
npx skills add vercel-labs/next-skills --global --agent codex --skill next-best-practices
```

Use `vercel-react-best-practices` for React and Next.js performance patterns, `vercel-composition-patterns` for component APIs, `vercel-react-view-transitions` for React view transition work, and `web-design-guidelines` for UI, accessibility, and UX review. Add `next-cache-components` or `next-upgrade` from `vercel-labs/next-skills` only for projects that need those specific Next.js workflows.

If your environment cannot use these installers, copy selected skill directories manually:

```sh
cp -R skills/feature-implementation /path/to/codex-skills/
cp -R skills/frontend-design /path/to/codex-skills/
cp -R skills/implement-to-merge-ready /path/to/codex-skills/
cp -R skills/kaizen-loop /path/to/codex-skills/
cp -R skills/ui-imagegen-director /path/to/codex-skills/
cp -R skills/goal-manager /path/to/codex-skills/
cp -R skills/bug-fix /path/to/codex-skills/
cp -R skills/review /path/to/codex-skills/
cp -R skills/jina-reader /path/to/codex-skills/
cp -R skills/jina-read-url /path/to/codex-skills/
cp -R skills/pr-guardian /path/to/codex-skills/
cp -R skills/meta-packager /path/to/codex-skills/
```

Install or copy only the skills that match repeated workflows. Use `implement-to-merge-ready` when an implementation request should run from plan and goal setup through tests, review, PR creation, and merge-readiness follow-up. Use `kaizen-loop` when Codex should evaluate a product, propose prioritized improvements, wait for user approval, then implement approved changes through merge-ready PRs. Use `frontend-design` for substantial UI layout, typography, color, usability, or responsive work, and `ui-imagegen-director` when image-generated UI direction should guide frontend implementation. Use `jina-reader` when public URLs need Jina Reader to recover LLM-friendly Markdown from pages normal tools cannot parse cleanly, and `jina-read-url` when the repeated task is simply to turn one public URL into readable Markdown and a concise summary in a ChatGPT-like workflow. Use `goal-manager` when a task needs explicit objective tracking across implementation, verification, or PR creation. Use `meta-packager` to mine recent Codex work, propose the smallest useful reusable asset, and package only explicitly approved high-confidence repeated patterns as skills, subagents, hooks, or automations. Do not put repository-specific secrets, credentials, or temporary task state in a skill.

### Evaluate a Skill

Use `empirical-prompt-tuning` when a skill is new, substantially revised, or important enough that subjective review is not enough. Start by generating an evaluation pack:

```sh
scripts/evaluate-skill.sh skills/feature-implementation
```

The generated files live under `ledger/skill-evaluations/<skill>/<timestamp>/` by default:

- `iteration-0-structural-review.md`: description/body consistency checks.
- `scenarios.md`: baseline scenarios plus a hold-out convergence scenario with `[critical]` requirements.
- `executor-prompt.md`: prompt template for fresh executors.
- `results.md`: iteration metrics and fix proposals.
- `failure-pattern-ledger.md`: recurring ambiguity patterns.

Keep the scenario requirements fixed after the first executor run, and reserve the hold-out scenario for convergence checking. Apply one theme of fixes, generate or start a new run, and repeat until the empirical-prompt-tuning stopping criteria are met.

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
