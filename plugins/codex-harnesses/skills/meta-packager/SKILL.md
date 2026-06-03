---
name: meta-packager
description: Analyze recent Codex work and package repeated patterns as the smallest useful skill, custom subagent, or automation.
---

# Meta Packager

Use this workflow when the user asks Codex to turn repeated recent work into reusable assets, such as skills, custom subagents, or automations.

## Workflow

1. Collect evidence in this order: recent Codex sessions and task summaries, Codex memories under `~/.codex/memories/`, Chronicle-derived memories under `~/.codex/memories_extensions/chronicle/` when present, then existing skills, subagents, hooks, and automations.
2. Inventory existing reusable assets before proposing anything new. Check repository-local assets first, then user-level assets such as `~/.codex/skills`, `~/.agents/skills`, `~/.codex/automations`, and any project `codex/`, `.codex/`, or `.agents/` directories.
3. Group candidate patterns by repeated user intent, not by exact prompt wording. Count only eligible occurrences from the collected evidence.
4. For each candidate, record occurrence count, stable inputs, expected outputs, tools or commands used, failure modes, and overlapping existing assets.
5. Apply all creation gates before packaging: at least two occurrences, stable inputs and outputs, material time or error-reduction benefit, no existing asset already covers most of the workflow, and no repository policy conflict.
6. Choose the smallest package type that fits: skill for repeatable procedural work, custom subagent for read-heavy parallel triage with a summary returned to the parent, automation for hook-driven or scheduled behavior with deterministic triggers.
7. Output a shortlist table before editing files. Mark low-confidence, one-off, or duplicate candidates as deferred instead of creating them.
8. Create only high-confidence items. Prefer extending an existing asset over creating a parallel skill, subagent, or automation.
9. For custom subagents, include an explicit reminder that they require deliberate parallel invocation and do not run automatically.
10. Update README or `docs/` when adding or changing reusable harness concepts, then run relevant verification.

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

Do not inspect credential files or unrelated private application data. If a memory source is unavailable, empty, or blocked by permissions, say so and continue with the remaining evidence.

## Package Rules

- Skill: use for procedures that an agent should follow on demand, especially review loops, release checks, scaffolding, debugging playbooks, or repeated command sequences.
- Custom subagent: use for parallel read-heavy work such as independent security, test-gap, or maintainability scans. Avoid when the work is primarily file editing or conflict-prone.
- Automation: use for deterministic triggers such as stop hooks, CI comment handling, scheduled audits, or notification loops. Avoid when the input is ad-hoc or judgment-heavy.
- Existing asset extension: use when an existing skill, subagent, or automation already covers most of the candidate and needs only a narrow addition.

## Final Report

Include:

- evidence sources inspected and any unavailable sources
- shortlist table with candidate, occurrence count, stable inputs and outputs, tools used, benefit, proposed package type, and decision
- items created or extended, with file paths
- low-confidence or duplicate items intentionally deferred
- verification commands and results
- reminder that custom subagents require explicit parallel invocation when any subagent candidate is created or recommended
