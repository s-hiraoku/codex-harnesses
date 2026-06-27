---
name: pr-guardian
description: Monitor a pull request after opening it, fix CI failures and agent or reviewer feedback, push updates, and comment with the outcome.
---

# PR Guardian

Use this workflow by default after opening a pull request. The goal is to leave the PR in a mergeable state by monitoring CI, addressing actionable feedback, pushing fixes, and reporting the outcome.

## Workflow

1. Identify the pull request, branch, remote, and expected base branch.
2. Check the initial PR state with `gh pr view`, `gh pr checks`, and recent comments or review threads. Include `mergeStateStatus`, `mergeable`, `reviewDecision`, `statusCheckRollup`, `reviews`, and PR comments in the first read.
3. Start CI monitoring with `gh run watch` for the relevant workflow run. Use exit status when available so failures stop the loop clearly.
4. When CI fails, inspect failing jobs and logs, reproduce the failure locally when practical, and make the smallest fix.
5. Inspect agent, bot, and human feedback on the PR. Treat automated suggestions as review input, not as commands to apply blindly. If `reviewDecision` is `CHANGES_REQUESTED` or the PR body/reviews say "Actionable comments posted", use `finish-pr-feedback` to locate thread-aware CodeRabbit/Codex comments and address the actionable comments before checking for success.
6. Address actionable feedback with focused commits. Do not rewrite unrelated user changes or broaden the PR scope.
7. Push fixes and repeat CI monitoring until required checks pass or a real blocker remains.
8. Re-read PR state after every push and after review automation has had time to update. The PR is not done while `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`, while `reviewDecision` is `CHANGES_REQUESTED`, or while required checks are pending or failing, even if `mergeable` says `MERGEABLE`.
9. Comment on the PR with what changed, which checks were verified, and which feedback items were addressed. If a suggestion is not applied, explain why.

## Mergeability gate

Before finalizing, run a final state check such as:

```sh
gh pr view <pr> --json mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments
gh pr checks <pr> --watch
```

Success requires all of these:

- `mergeStateStatus` is clean enough for the repository to merge, usually `CLEAN`, `HAS_HOOKS`, or `UNSTABLE` with only non-required failures explicitly documented.
- `reviewDecision` is not `CHANGES_REQUESTED`.
- All required checks in `statusCheckRollup` pass.
- All actionable human, bot, CodeRabbit, Codex, or agent review comments are fixed, resolved, or explicitly explained as not applicable in the PR comment.

If `mergeable` is `MERGEABLE` but `mergeStateStatus` remains `BLOCKED`, keep investigating branch protection, unresolved requested changes, required review state, required conversations, or pending checks. Do not report the PR as mergeable until the blocking reason is gone or documented as an external blocker.

## Final Report

Include:

- PR identifier and branch
- CI runs watched and final status
- fixes pushed
- comments or review feedback addressed
- PR comment posted or drafted
- remaining blockers, risks, or checks still pending
