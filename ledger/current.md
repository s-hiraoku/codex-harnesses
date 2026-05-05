# Current Task Ledger

Use this file to keep long-running work resumable.

## Current Goal

- Goal: Clarify hook expectations, CI verification guidance, and ledger operating rules; dogfood the repository harness.
- Owner: Codex
- Started: 2026-05-05 11:53 JST
- Status: PR review feedback addressed and verified

## Context

- Repository: codex-harnesses
- Branch: codex/clarify-harness-safety-ci
- Related issue or PR: https://github.com/s-hiraoku/codex-harnesses/pull/1
- Important files: README.md, AGENTS.md, docs/usage.md, docs/adoption-checklist.md, docs/task-ledger-patterns.md, docs/release-readiness.md, ledger/verification.md

## Plan

- [x] Inspect current state
- [x] Implement changes
- [x] Update tests or docs
- [x] Run verification
- [ ] Summarize outcome

## Progress

Record dated progress notes here.

- 2026-05-05 11:53 JST: Confirmed this repository already contains the core harness pieces: root `AGENTS.md`, `policies/strict.yaml`, `ledger/`, `scripts/verify.sh`, and GitHub Actions verification.
- 2026-05-05 11:53 JST: Clarified that hooks are payload scripts, CI should run the same strict verification script, and ledger updates are required for large, risky, security-sensitive, or interrupted work.
- 2026-05-05 11:53 JST: Updated root `AGENTS.md` so the repository explicitly dogfoods its strict harness.
- 2026-05-05 11:56 JST: Ran strict repository verification successfully with repo-local venv tools.
- 2026-05-05 12:01 JST: Addressed PR feedback by adding Python setup and dependency installation steps before strict verification in the CI example.
- 2026-05-05 12:01 JST: Re-ran strict repository verification successfully after review feedback changes.

## Blockers

- None recorded.

## Next Step

- Commit and push the PR feedback update.

## Checkpoints

`scripts/checkpoint.sh` appends entries here.
