#!/usr/bin/env bash
set -euo pipefail

if [[ -f package-lock.json ]]; then
  runner="npm run"
elif [[ -f pnpm-lock.yaml ]]; then
  runner="pnpm"
elif [[ -f yarn.lock ]]; then
  runner="yarn"
else
  runner="npm run"
fi

if [[ ! -f package.json ]]; then
  echo "package.json not found"
  exit 1
fi

run_script_if_present() {
  local script_name="$1"

  if ! node -e "process.exit(require('./package.json').scripts?.['${script_name}'] ? 0 : 1)"; then
    echo "No script '${script_name}' detected"
    return
  fi

  echo "Running ${script_name}"
  ${runner} "${script_name}"
}

run_script_if_present lint
run_script_if_present typecheck
run_script_if_present test
run_script_if_present build
