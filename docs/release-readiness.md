# Release Readiness

Use this checklist before announcing, tagging, or broadly sharing this repository.

## Repository Metadata

- [ ] Repository description explains the harness collection in one sentence.
- [ ] Repository homepage points to the GitHub Pages guide.
- [ ] Topics make the repository discoverable.
- [ ] README has current CI and Pages badges.

## Documentation

- [ ] README explains what the repository is and is not.
- [ ] Quick Start points users to examples and adoption docs.
- [ ] User guide builds with `mkdocs build --strict`.
- [ ] Hook examples clearly state they are not production-ready security controls.
- [ ] Ledger docs explain how to resume long-running work.
- [ ] Contribution guidelines match the repository scope.

## Harness Assets

- [ ] Each skill has valid `SKILL.md` frontmatter.
- [ ] Each example has `README.md` and `AGENTS.md`.
- [ ] Policies validate against `schemas/policy.schema.json`.
- [ ] Hook scripts have allowed and blocked test cases.
- [ ] Root scripts are executable and pass bash syntax checks.

## Verification

- [ ] `CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh` passes locally.
- [ ] GitHub Actions `Verify` passes on `main`.
- [ ] GitHub Actions `Publish GitHub Pages` passes on `main`.
- [ ] GitHub Pages renders the user guide correctly.

## Risk Review

- [ ] No docs imply example hooks are complete security products.
- [ ] No secrets or local paths are committed.
- [ ] Generated artifacts such as `site/`, `.venv/`, and caches are ignored.
- [ ] Known limitations are documented rather than hidden.

## Announcement Notes

When introducing the repository, describe it as:

> A copyable, tested harness collection for helping Codex run long tasks safely, with durable guidance, reusable skills, deterministic hooks, task ledgers, policies, examples, and verification loops.

Avoid positioning it as a multi-agent router or a replacement for project-specific tests, review, sandboxing, or security tooling.

