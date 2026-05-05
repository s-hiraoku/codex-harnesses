#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f package.json ]]; then
  echo "package.json not found"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node not found"
  exit 1
fi

if [[ -f package-lock.json ]]; then
  package_manager="npm"
elif [[ -f pnpm-lock.yaml ]]; then
  package_manager="pnpm"
elif [[ -f yarn.lock ]]; then
  package_manager="yarn"
else
  package_manager="npm"
fi

if ! command -v "${package_manager}" >/dev/null 2>&1; then
  echo "${package_manager} not found"
  exit 1
fi

run_script_if_present() {
  local script_name="$1"

  if ! node -e "process.exit(require('./package.json').scripts?.['${script_name}'] ? 0 : 1)"; then
    echo "No script '${script_name}' detected"
    return
  fi

  echo "Running ${script_name}"
  "${package_manager}" run "${script_name}"
}

run_script_if_present lint
run_script_if_present typecheck
run_script_if_present test
run_script_if_present build
