#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET="."
AGENTS_TEMPLATE="strict"
INSTALL_VERIFY=1
INSTALL_LEDGER=0
POLICY=""
SKILLS=""
HOOKS=""
DRY_RUN=0
FORCE=0

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [options]

Deploy selected codex-harnesses files into a project.

Options:
  --target DIR              Target project directory. Defaults to current directory.
  --agents NAME             AGENTS.md template: strict, frontend, or library. Defaults to strict.
  --no-agents               Do not install AGENTS.md.
  --verify                  Install scripts/verify.sh. Enabled by default.
  --no-verify               Do not install scripts/verify.sh.
  --ledger                  Install ledger templates.
  --policy NAME             Install policies/NAME.yaml as policies/codex.yaml.
  --skills LIST             Install comma-separated skills, or "all".
  --hooks LIST              Install comma-separated hook directories, or "all".
  --force                   Overwrite existing target files.
  --dry-run                 Print planned changes without writing files.
  -h, --help                Show this help.

Examples:
  scripts/install.sh --target /path/to/project --agents strict --skills feature-implementation,bug-fix,review --ledger --policy default
  scripts/install.sh --target . --agents frontend --skills all --hooks secret-guard,stop-verify
USAGE
}

fail() {
  echo "error: $*" >&2
  exit 1
}

log() {
  echo "$*"
}

canonical_existing_path() {
  local path="$1"
  local dir

  [[ -e "${path}" ]] || return 1
  dir="$(cd "$(dirname "${path}")" && pwd -P)"
  printf '%s/%s\n' "${dir}" "$(basename "${path}")"
}

same_existing_path() {
  local left="$1"
  local right="$2"

  [[ -e "${left}" && -e "${right}" ]] || return 1
  [[ "$(canonical_existing_path "${left}")" == "$(canonical_existing_path "${right}")" ]]
}

ensure_known_name() {
  local kind="$1"
  local name="$2"
  local path="$3"

  [[ -e "${path}" ]] || fail "unknown ${kind}: ${name}"
}

LIST_ITEMS=()

split_list() {
  local value="$1"
  local dir="$2"

  LIST_ITEMS=()
  if [[ "${value}" == "all" ]]; then
    local path
    while IFS= read -r path; do
      LIST_ITEMS+=("$(basename "${path}")")
    done < <(find "${dir}" -mindepth 1 -maxdepth 1 -type d | sort)
    return
  fi

  local item
  IFS=',' read -ra LIST_ITEMS <<<"${value}"
  for item in "${LIST_ITEMS[@]}"; do
    [[ -n "${item}" ]] || fail "empty item in list: ${value}"
  done
}

copy_file() {
  local src="$1"
  local dest="$2"

  if same_existing_path "${src}" "${dest}"; then
    log "skip same path ${dest}"
    return
  fi

  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    log "skip existing ${dest}"
    return
  fi

  log "install ${dest}"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    return
  fi

  mkdir -p "$(dirname "${dest}")"
  cp "${src}" "${dest}"
}

copy_dir() {
  local src="$1"
  local dest="$2"

  if same_existing_path "${src}" "${dest}"; then
    log "skip same path ${dest}"
    return
  fi

  if [[ -e "${dest}" && "${FORCE}" -ne 1 ]]; then
    log "skip existing ${dest}"
    return
  fi

  log "install ${dest}/"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    return
  fi

  rm -rf "${dest}"
  mkdir -p "$(dirname "${dest}")"
  cp -R "${src}" "${dest}"
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      [[ -n "${TARGET}" ]] || fail "--target requires a directory"
      shift 2
      ;;
    --agents)
      AGENTS_TEMPLATE="${2:-}"
      [[ -n "${AGENTS_TEMPLATE}" ]] || fail "--agents requires a template name"
      shift 2
      ;;
    --no-agents)
      AGENTS_TEMPLATE=""
      shift
      ;;
    --verify)
      INSTALL_VERIFY=1
      shift
      ;;
    --no-verify)
      INSTALL_VERIFY=0
      shift
      ;;
    --ledger)
      INSTALL_LEDGER=1
      shift
      ;;
    --policy)
      POLICY="${2:-}"
      [[ -n "${POLICY}" ]] || fail "--policy requires a policy name"
      shift 2
      ;;
    --skills)
      SKILLS="${2:-}"
      [[ -n "${SKILLS}" ]] || fail "--skills requires a comma-separated list or all"
      shift 2
      ;;
    --hooks)
      HOOKS="${2:-}"
      [[ -n "${HOOKS}" ]] || fail "--hooks requires a comma-separated list or all"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

[[ -d "${TARGET}" ]] || fail "target directory does not exist: ${TARGET}"
TARGET="$(cd "${TARGET}" && pwd)"

if [[ -n "${AGENTS_TEMPLATE}" ]]; then
  agents_src="${ROOT}/templates/agents/${AGENTS_TEMPLATE}/AGENTS.md"
  ensure_known_name "AGENTS.md template" "${AGENTS_TEMPLATE}" "${agents_src}"
  copy_file "${agents_src}" "${TARGET}/AGENTS.md"
fi

if [[ "${INSTALL_VERIFY}" -eq 1 ]]; then
  copy_file "${ROOT}/scripts/verify.sh" "${TARGET}/scripts/verify.sh"
fi

if [[ "${INSTALL_LEDGER}" -eq 1 ]]; then
  copy_dir "${ROOT}/ledger" "${TARGET}/ledger"
fi

if [[ -n "${POLICY}" ]]; then
  policy_src="${ROOT}/policies/${POLICY}.yaml"
  ensure_known_name "policy" "${POLICY}" "${policy_src}"
  copy_file "${policy_src}" "${TARGET}/policies/codex.yaml"
fi

if [[ -n "${SKILLS}" ]]; then
  split_list "${SKILLS}" "${ROOT}/skills"
  skill_names=("${LIST_ITEMS[@]}")
  for skill in "${skill_names[@]}"; do
    ensure_known_name "skill" "${skill}" "${ROOT}/skills/${skill}/SKILL.md"
    copy_dir "${ROOT}/skills/${skill}" "${TARGET}/skills/${skill}"
  done
fi

if [[ -n "${HOOKS}" ]]; then
  split_list "${HOOKS}" "${ROOT}/hooks"
  hook_names=("${LIST_ITEMS[@]}")
  for hook in "${hook_names[@]}"; do
    ensure_known_name "hook" "${hook}" "${ROOT}/hooks/${hook}"
    copy_dir "${ROOT}/hooks/${hook}" "${TARGET}/hooks/${hook}"
  done
fi

log "codex harness deployment complete"
