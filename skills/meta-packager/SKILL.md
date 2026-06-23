---
name: meta-packager
description: Analyze recent Codex work and package repeated patterns as the smallest useful skill, custom subagent, hook, or automation. Use when asked to mine sessions, memories, or recent repeated work for reusable Codex assets.
---

# Meta Packager

Use this workflow when the user asks Codex to turn repeated recent work into reusable assets, such as skills, custom subagents, hooks, or automations.

## Workflow

1. Confirm the packaging scope: target repository assets by default, user-global assets only when the user asks for them, and no live service changes unless explicitly requested.
2. Collect evidence in this order: recent Codex sessions and task summaries, Codex memories under `~/.codex/memories/`, Chronicle-derived memories under `~/.codex/memories_extensions/chronicle/` when present, then existing skills, subagents, hooks, and automations. Keep collection read-only.
3. Inventory existing reusable assets before proposing anything new. Check repository-local assets first, then user-level assets such as `~/.codex/skills`, `~/.agents/skills`, `~/.codex/automations`, `~/.codex/hooks`, and any project `codex/`, `.codex/`, or `.agents/` directories.
4. Group candidate patterns by repeated user intent, not by exact prompt wording. Count only eligible occurrences from the collected evidence.
5. For each candidate, record occurrence count, stable inputs, expected outputs, tools or commands used, failure modes, and overlapping existing assets.
6. Apply all creation gates before packaging: at least two occurrences, stable inputs and outputs, material time or error-reduction benefit, no existing asset already covers most of the workflow, and no repository policy conflict.
7. Choose the smallest package type that fits: skill for repeatable procedural work, custom subagent for read-heavy parallel triage with a summary returned to the parent, hook for deterministic lifecycle enforcement, automation for scheduled or event-driven behavior with clear triggers.
8. Output a shortlist table and stop for explicit user approval before editing files. If the user has already approved a specific candidate in the current request, proceed only with that candidate.
9. Create or extend only approved high-confidence items. Prefer extending an existing asset over creating a parallel skill, subagent, hook, or automation.
10. For custom subagents, include an explicit reminder that they require deliberate parallel invocation and do not run automatically.
11. Update README or `docs/` when adding or changing reusable harness concepts, then run relevant verification.

## Evidence Hints

Recent session data is usually available through Codex state files, history files, or session JSONL files. Useful local checks include:

```sh
tail -80 ~/.codex/history.jsonl
tail -80 ~/.codex/session_index.jsonl
find ~/.codex/sessions -type f | tail -80
find ~/.codex/memories -maxdepth 3 -type f
find ~/.codex/memories_extensions/chronicle -maxdepth 3 -type f
```

If Codex state is stored in SQLite, inspect schemas before querying and keep queries read-only:

```sh
sqlite3 ~/.codex/state_5.sqlite .tables
sqlite3 ~/.codex/state_5.sqlite 'PRAGMA table_info(threads);'
```

Do not inspect credential files or unrelated private application data. Do not quote secrets, personal content, or long session excerpts in reports; summarize only the pattern, source category, and evidence count. If a memory source is unavailable, empty, or blocked by permissions, say so and continue with the remaining evidence.

## Package Rules

- Skill: use for procedures that an agent should follow on demand, especially review loops, release checks, scaffolding, debugging playbooks, or repeated command sequences.
- Custom subagent: use for parallel read-heavy work such as independent security, test-gap, or maintainability scans. Avoid when the work is primarily file editing or conflict-prone.
- Hook: use for deterministic lifecycle enforcement such as command guards, verification gates, context injection, or secret scanning. Hooks are payloads until explicitly wired into a target environment.
- Automation: use for scheduled audits, follow-ups, notifications, CI comment handling, or other event-driven behavior with clear triggers. Avoid when the input is ad-hoc or judgment-heavy.
- Existing asset extension: use when an existing skill, subagent, hook, or automation already covers most of the candidate and needs only a narrow addition.

## Creation Rules

- Write new assets into the target repository by default. Use user-global locations only when the user explicitly asks for global installation.
- For new skills, create the smallest valid skill folder with `SKILL.md`; add `agents/openai.yaml`, scripts, references, or assets only when they materially improve reuse.
- For custom subagents, use the target repository's established format when one exists. If no format is discoverable, recommend the subagent contract instead of inventing a storage convention.
- For hooks, create deterministic payload scripts and tests or usage examples when practical. Document that registration is a separate integration step.
- For automations, use the available automation tooling when present. If no automation tool or project convention is available, write a proposed trigger/action spec and stop before pretending it is installed.

## Final Report

Include:

- evidence sources inspected and any unavailable sources
- shortlist table with candidate, occurrence count, stable inputs and outputs, tools used, benefit, proposed package type, and decision
- items created or extended, with file paths
- low-confidence or duplicate items intentionally deferred
- verification commands and results
- reminder that custom subagents require explicit parallel invocation when any subagent candidate is created or recommended
- note that hooks and automations are not active unless they were explicitly wired into the target environment
