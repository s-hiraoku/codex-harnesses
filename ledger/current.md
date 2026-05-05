# Current Task Ledger

Use this file to keep long-running work resumable.

## Current Goal

- Goal: Clarify hook expectations, CI verification guidance, and ledger operating rules; dogfood the repository harness.
- Owner: Codex
- Started: 2026-05-05 11:53 JST
- Status: Verified; ready for commit and PR

## Context

- Repository: codex-harnesses
- Branch: codex/clarify-harness-safety-ci
- Related issue or PR: PR to be opened after verification
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

## Blockers

- None recorded.

## Next Step

- Commit these changes, push `codex/clarify-harness-safety-ci`, and open a PR.

## Checkpoints

`scripts/checkpoint.sh` appends entries here.
