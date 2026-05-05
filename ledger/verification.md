# Verification Log

Use this file to record meaningful verification runs.

## Template

### YYYY-MM-DD HH:MM

- Command:
- Scope:
- Result:
- Notes:

## Runs

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
