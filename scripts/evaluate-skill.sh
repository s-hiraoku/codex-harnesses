#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_ROOT="${CODEX_SKILL_EVAL_DIR:-${ROOT}/ledger/skill-evaluations}"

usage() {
  cat <<'USAGE'
Usage: scripts/evaluate-skill.sh [options] SKILL_DIR

Create an empirical-prompt-tuning evaluation pack for a skill.

Options:
  --output DIR       Destination directory for evaluation runs.
                     Defaults to ledger/skill-evaluations.
  -h, --help         Show this help.

Examples:
  scripts/evaluate-skill.sh skills/feature-implementation
  scripts/evaluate-skill.sh --output /tmp/skill-evals skills/my-skill
USAGE
}

fail() {
  echo "error: $*" >&2
  exit 1
}

extract_frontmatter_value() {
  local key="$1"
  local file="$2"

  awk -v key="${key}" '
    NR == 1 && $0 != "---" { exit 1 }
    NR > 1 && $0 == "---" { exit 0 }
    NR > 1 {
      split($0, parts, ":")
      if (parts[1] == key) {
        sub("^[^:]*:[[:space:]]*", "", $0)
        print $0
        exit 0
      }
    }
  ' "${file}"
}

require_section() {
  local section="$1"
  local file="$2"

  grep -Fqx "## ${section}" "${file}" || fail "${file} must contain '## ${section}'"
}

skill_dir=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --output)
      OUTPUT_ROOT="${2:-}"
      [[ -n "${OUTPUT_ROOT}" ]] || fail "--output requires a directory"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      [[ -z "${skill_dir}" ]] || fail "only one SKILL_DIR may be provided"
      skill_dir="$1"
      shift
      ;;
  esac
done

[[ -n "${skill_dir}" ]] || fail "SKILL_DIR is required"

if [[ "${skill_dir}" != /* ]]; then
  skill_dir="${ROOT}/${skill_dir}"
fi

skill_file="${skill_dir}/SKILL.md"
[[ -f "${skill_file}" ]] || fail "missing ${skill_file}"

skill_name="$(basename "${skill_dir}")"
frontmatter_name="$(extract_frontmatter_value name "${skill_file}")"
description="$(extract_frontmatter_value description "${skill_file}")"

[[ "${frontmatter_name}" == "${skill_name}" ]] || fail "frontmatter name must be ${skill_name}"
[[ -n "${description}" ]] || fail "frontmatter description is required"
require_section "Workflow" "${skill_file}"

timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
run_parent="${OUTPUT_ROOT}/${skill_name}"
mkdir -p "${run_parent}"
run_dir="$(mktemp -d "${run_parent}/${timestamp}.XXXXXX")"

cat >"${run_dir}/README.md" <<EOF
# ${skill_name} empirical prompt tuning

Target skill: \`${skill_file}\`
Generated: ${timestamp}

Use \`empirical-prompt-tuning\` to run this pack. Do not change the scenario
requirements after the first executor run; record changes as a new run instead.

## Run order

1. Complete \`iteration-0-structural-review.md\`.
2. Fill in two or three concrete scenarios in \`scenarios.md\`.
3. Dispatch a fresh executor per baseline scenario with \`executor-prompt.md\`.
4. Record results in \`results.md\`.
5. Apply one theme of fixes to the target skill and start a new run.
6. Use the hold-out scenario only when checking convergence.
EOF

cat >"${run_dir}/iteration-0-structural-review.md" <<EOF
# Iteration 0: description/body consistency

## Frontmatter description

${description}

## Checks

- [ ] The description names only use cases covered by the body.
- [ ] Trigger wording is specific enough for an agent to know when to use the skill.
- [ ] The body contains a minimum complete workflow for each claimed use case.
- [ ] Environment constraints and skip conditions are explicit.
- [ ] Final reporting expectations are clear.

## Notes

- Finding:
- Fix before empirical iteration:
EOF

cat >"${run_dir}/scenarios.md" <<'EOF'
# Evaluation scenarios

Keep 2 to 3 scenarios: one median case and one or two realistic edges.
Each scenario must include 3 to 7 requirements and at least one [critical] item.

## Scenario A: median case

Context:

Requirements checklist:
1. [critical]
2.
3.

## Scenario B: edge case

Context:

Requirements checklist:
1. [critical]
2.
3.

## Hold-out scenario: convergence check only

Context:

Requirements checklist:
1. [critical]
2.
3.
EOF

cat >"${run_dir}/executor-prompt.md" <<EOF
# Executor prompt template

You are an executor reading ${skill_name} with a blank slate.

## Target prompt

Read the full target skill at:

\`${skill_file}\`

## Scenario

Paste one scenario from \`scenarios.md\`.

## Requirements checklist

Paste that scenario's checklist. Do not add or remove [critical] tags.

## Task

1. Follow the target prompt to execute the scenario and produce the deliverable.
2. On completion, respond with the report structure below.

## Report structure

- Deliverable: <artifact or execution summary>
- Requirement achievement: ○ / × / partial, with reason for each item
- Trace:
  - Use \`Trace: all OK\` only when Understanding, Planning, Execution, and Formatting are all OK.
  - Otherwise list each phase with OK / stuck / skipped and a one-line reason.
- Unclear points (structured): for each issue, include Issue / Cause / General Fix Rule.
- Discretionary fill-ins: places not fixed by the instruction and filled by judgment.
- Retries: number of times the same decision was redone and why.
EOF

cat >"${run_dir}/results.md" <<'EOF'
# Results

## Iteration 1

### Execution results

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---:|---:|---:|---:|---|
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

### Structured reflection

- Scenario A:
- Scenario B:

### Discretionary fill-ins

- Scenario A:
- Scenario B:

### Fix proposal

- Judgment wording satisfied:
- Minimum fix:

### Convergence check

- Consecutive clear rounds:
- Hold-out scenario run:
- Hold-out result:
EOF

cat >"${run_dir}/failure-pattern-ledger.md" <<'EOF'
# Failure pattern ledger

- **Pattern name**:
  - Example:
  - General Fix Rule:
  - Seen in:
EOF

printf 'created %s\n' "${run_dir}"
