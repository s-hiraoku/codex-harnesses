#!/usr/bin/env bash
set -euo pipefail

run_if_script_exists() {
  local script_name="$1"

  if ! command -v npm >/dev/null 2>&1; then
    echo "npm not found; skipping package.json script checks"
    return
  fi

  if npm run | grep -E "^[[:space:]]+${script_name}$|^[[:space:]]+${script_name}:" >/dev/null 2>&1; then
    echo "Running npm run ${script_name}"
    npm run "${script_name}"
  else
    echo "No npm script '${script_name}' detected"
  fi
}

run_python_checks() {
  local ran_check=0

  if command -v ruff >/dev/null 2>&1; then
    echo "Running ruff check ."
    ruff check .
    ran_check=1
  fi

  if command -v mypy >/dev/null 2>&1; then
    echo "Running mypy ."
    mypy .
    ran_check=1
  fi

  if command -v pytest >/dev/null 2>&1 && compgen -G "tests/test*.py" >/dev/null; then
    echo "Running pytest"
    pytest
    ran_check=1
  fi

  if [[ "${ran_check}" -eq 0 ]]; then
    echo "pyproject.toml detected, but no supported Python checks were available"
  fi
}

main() {
  local detected=0

  if [[ -f package.json ]]; then
    detected=1
    run_if_script_exists lint
    run_if_script_exists typecheck
    run_if_script_exists test
    run_if_script_exists build
  fi

  if [[ -f pyproject.toml ]]; then
    detected=1
    run_python_checks
  fi

  if [[ "${detected}" -eq 0 ]]; then
    echo "No project-specific verification detected"
  fi

  echo "Verification script completed"
}

main "$@"

