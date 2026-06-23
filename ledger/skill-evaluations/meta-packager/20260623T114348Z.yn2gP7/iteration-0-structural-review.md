# Iteration 0: description/body consistency

## Frontmatter description

Analyze recent Codex work and package repeated patterns as the smallest useful skill, custom subagent, hook, or automation. Use when asked to mine sessions, memories, or recent repeated work for reusable Codex assets.

## Checks

- [x] The description names only use cases covered by the body.
- [x] Trigger wording is specific enough for an agent to know when to use the skill.
- [x] The body contains a minimum complete workflow for each claimed use case.
- [x] Environment constraints and skip conditions are explicit.
- [x] Final reporting expectations are clear.

## Notes

- Finding: The previous body allowed asset creation after a shortlist without requiring explicit approval, omitted hooks from package selection even though this harness treats hooks as reusable assets, and did not define creation locations or privacy constraints tightly enough for session mining.
- Fix before empirical iteration: Updated the workflow to confirm scope, keep evidence collection read-only, require explicit approval before edits, include hooks as a package type, define creation rules for skills/subagents/hooks/automations, and restrict report content to summarized patterns rather than raw private excerpts.
