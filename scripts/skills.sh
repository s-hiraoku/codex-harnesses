#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET="${CODEX_SKILLS_DIR:-}"
SKILLS="all"
FORCE=0

usage() {
  cat <<'USAGE'
Usage: scripts/skills.sh [options] [skill ...]

Install codex-harnesses skills into a skills directory.

Options:
  --target DIR       Destination skills directory. Defaults to CODEX_SKILLS_DIR, then ./.codex/skills.
  --force            Overwrite existing skills.
  -h, --help         Show this help.

Examples:
  scripts/skills.sh --target ~/.codex/skills feature-implementation bug-fix review
  CODEX_SKILLS_DIR=.codex/skills scripts/skills.sh all
USAGE
}

fail() {
  echo "error: $*" >&2
  exit 1
}

skill_args=()
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      [[ -n "${TARGET}" ]] || fail "--target requires a directory"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      skill_args+=("$1")
      shift
      ;;
  esac
done

if [[ "${#skill_args[@]}" -gt 0 ]]; then
  SKILLS="$(IFS=','; echo "${skill_args[*]}")"
fi

if [[ -z "${TARGET}" ]]; then
  TARGET=".codex/skills"
fi

mkdir -p "${TARGET}"

skill_names=()
if [[ "${SKILLS}" == "all" ]]; then
  while IFS= read -r path; do
    skill_names+=("$(basename "${path}")")
  done < <(find "${ROOT}/skills" -mindepth 1 -maxdepth 1 -type d | sort)
else
  IFS=',' read -ra skill_names <<<"${SKILLS}"
fi

for skill in "${skill_names[@]}"; do
  [[ -n "${skill}" ]] || fail "empty skill name"
  src="${ROOT}/skills/${skill}"
  dest="${TARGET}/${skill}"
  [[ -f "${src}/SKILL.md" ]] || fail "unknown skill: ${skill}"

  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    echo "skip existing ${dest}"
    continue
  fi

  echo "install ${dest}/"
  rm -rf "${dest}"
  cp -R "${src}" "${dest}"
done

echo "skill installation complete"
