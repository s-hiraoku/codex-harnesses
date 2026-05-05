#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f package.json ]]; then
  echo "package.json not found"
  exit 1
fi

npm run lint
npm run typecheck
npm test
npm run build

