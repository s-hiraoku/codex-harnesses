# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

### 2026-05-31 16:32 JST

- Command: `PATH=/private/tmp/codex-harnesses-verify-venv/bin:$PATH bash scripts/verify.sh`
- Scope: repository-level verification after rebasing `codex/frontend-design-harness` onto `origin/main` and resolving `docs/usage.md`
- Result: passed
- Notes: `ruff check .`, 20 pytest tests, and `mkdocs build --strict` passed.

### 2026-05-31 12:41 JST

- Command: `PATH=/private/tmp/codex-harnesses-verify-venv/bin:$PATH bash scripts/verify.sh`
- Scope: repository-level ruff, pytest, and MkDocs strict build after adding the `frontend-design` skill
- Result: passed
- Notes: Created a temporary venv under `/private/tmp` and installed `requirements-dev.txt` because the user-level `pytest` used an incompatible `rpds` wheel. `ruff check .`, 20 pytest tests, and `mkdocs build --strict` passed.

### 2026-05-05 11:54 JST

- Command: `CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level ruff, pytest, and MkDocs strict build
- Result: failed
- Notes: `pytest` collected with the system Python environment and failed importing `rpds` because the installed wheel was `x86_64` while the interpreter needed `arm64e` or `arm64`.

### 2026-05-05 11:56 JST

- Command: `PATH=.venv/bin:$PATH CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level ruff, pytest, and MkDocs strict build
- Result: passed
- Notes: Created a repo-local venv and installed `requirements-dev.txt` so verification used architecture-compatible tools. `ruff check .`, 16 pytest tests, and `mkdocs build --strict` all passed.

### 2026-05-05 12:01 JST

- Command: `PATH=.venv/bin:$PATH CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: PR review feedback update for CI documentation example
- Result: passed
- Notes: `ruff check .`, 16 pytest tests, and `mkdocs build --strict` all passed after adding setup and dependency installation steps to the CI example.

### 2026-05-09 08:23 JST

- Command: `pytest tests/test_skills.py tests/test_scripts.py`
- Scope: empirical-prompt-tuning skill registration and skill evaluation pack script
- Result: passed
- Notes: 10 targeted tests passed.

### 2026-05-09 08:24 JST

- Command: `bash scripts/verify.sh`
- Scope: repository-level verification with system Python
- Result: failed
- Notes: `ruff check .` passed, but pytest collection failed importing `rpds` through `jsonschema` because the installed wheel was `x86_64` while the interpreter needed `arm64e` or `arm64`.

### 2026-05-09 08:25 JST

- Command: `PATH=.venv/bin:$PATH CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level ruff, pytest, and MkDocs strict build
- Result: passed
- Notes: `ruff check .`, 21 pytest tests, and `mkdocs build --strict` all passed with the repo-local venv.

### 2026-05-26 12:08:00 JST

- Command: `bash scripts/verify.sh`
- Scope: repository-level verification for `meta-packager` skill and docs updates
- Result: failed
- Notes: `ruff check .` passed, then `pytest` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`).

### 2026-05-26 12:08:30 JST

- Command: `PATH=.venv/bin:$PATH bash scripts/verify.sh`
- Scope: repository-level verification for `meta-packager` skill and docs updates
- Result: passed
- Notes: `ruff check .`, 18 pytest tests, and `mkdocs build --strict` all passed using the repo-local virtualenv. Re-ran after recording this ledger entry; the same command passed on the final tree.

### 2026-05-31 00:44 JST

- Command: `PATH=.venv/bin:$PATH bash scripts/verify.sh`
- Scope: PR #7 review feedback fixes
- Result: passed
- Notes: `ruff check .`, 18 pytest tests, and `mkdocs build --strict` all passed after clarifying verification-log timestamps.

### 2026-05-31 07:46 JST

- Command: `PATH=.venv/bin:$PATH pytest tests/test_scripts.py tests/test_skills.py`
- Scope: PR #6 conflict resolution and `evaluate-skill.sh` unique run-directory fix
- Result: passed
- Notes: 9 targeted tests passed after preserving the `meta-packager` and `empirical-prompt-tuning` skill registrations.

### 2026-05-31 07:47 JST

- Command: `PATH=.venv/bin:$PATH CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level verification after PR #6 conflict resolution
- Result: failed
- Notes: `.venv` did not exist in this worktree yet, so the command fell back to system Python and failed importing the incompatible `rpds` wheel.

### 2026-05-31 07:48 JST

- Command: `PATH=.venv/bin:$PATH CODEX_HARNESSES_STRICT=1 bash scripts/verify.sh`
- Scope: repository-level verification after PR #6 conflict resolution
- Result: passed
- Notes: Created `.venv`, installed `requirements-dev.txt`, then `ruff check .`, 20 pytest tests, and `mkdocs build --strict` all passed.

### 2026-06-10 10:34 JST

- Command: `bash scripts/verify.sh`
- Scope: repository-level verification for `jina-read-url` skill addition
- Result: failed
- Notes: `ruff check .` passed, then `pytest` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`).

### 2026-06-10 10:34 JST

- Command: `PATH=.venv/bin:$PATH bash scripts/verify.sh`
- Scope: repository-level verification for `jina-read-url` skill addition
- Result: passed
- Notes: `ruff check .`, 20 pytest tests, and `mkdocs build --strict` all passed using the repo-local virtualenv.

### 2026-06-13 09:51 JST

- Command: `bash scripts/verify.sh`
- Scope: repository-level verification after PR #12 conflict resolution
- Result: failed
- Notes: `ruff check .` passed, then `pytest` failed during collection because the system Python loaded an incompatible `rpds` wheel (`x86_64` instead of `arm64e` or `arm64`).

### 2026-06-13 09:51 JST

- Command: `PATH=.venv/bin:$PATH bash scripts/verify.sh`
- Scope: repository-level verification after PR #12 conflict resolution
- Result: passed
- Notes: `ruff check .`, 20 pytest tests, and `mkdocs build --strict` all passed using the repo-local virtualenv.
