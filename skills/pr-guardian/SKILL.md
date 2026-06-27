---
name: pr-guardian
description: Monitor or resume GitHub pull requests, fix CI failures and actionable CodeRabbit, Codex, bot, or human review feedback, push focused updates, and stop only when the PR is merge-ready or has a concrete external blocker.
---

# PR Guardian

Use this workflow by default after opening a pull request, and when an existing PR needs follow-up after CI, CodeRabbit, Codex, bot, or human review feedback. The goal is to leave the PR merge-ready or report a specific blocker, not to provide a partial status update.

## Workflow

1. Resolve the target PRs.
   - Use explicit repo or PR URLs when provided.
   - Otherwise identify the current branch PR, branch, remote, and expected base branch.
   - If the user asks for "each repo" or "all repos", scan the relevant workspace repositories, list open PRs, and process one repo at a time.
2. Load local repo context before edits.
   - Read local instructions such as `AGENTS.md`, package scripts, branch status, and PR metadata.
   - Preserve unrelated local changes.
3. Build a complete PR state and feedback inventory.
   - Read `mergeStateStatus`, `mergeable`, `reviewDecision`, `statusCheckRollup`, `reviews`, `latestReviews`, review requests, PR comments, and `gh pr checks`.
   - Fetch thread-aware review data when review automation, CodeRabbit, Codex, requested changes, or "Actionable comments posted" summaries appear.
   - Use `references/pr-feedback-audit.md` for concrete `gh` and GraphQL commands when thread state, bot comments, CI logs, or cross-repo scanning matter.
4. Classify every feedback item.
   - `fix`: code, docs, tests, CI, or config change is needed.
   - `respond`: a reviewer asked for clarification and no code change is appropriate.
   - `ignore`: duplicate, outdated, already resolved, or demonstrably wrong.
   - `blocked`: credentials, product decision, external service, or maintainer action is required.
5. Start or continue CI monitoring.
   - Use `gh run watch` for the relevant workflow run when practical.
   - If CI fails, inspect failing jobs and logs, reproduce locally when practical, and make the smallest fix.
6. Implement all `fix` items.
   - Keep edits scoped to the PR and trace each change back to a feedback or CI cluster.
   - Add or update tests when the feedback identifies behavior risk.
   - Do not rewrite unrelated user changes or broaden the PR scope.
7. Handle `respond` and `ignore` items explicitly.
   - Leave a concise PR comment or review reply when a suggestion is not applied.
   - Do not resolve GitHub review threads unless the user explicitly allows write actions beyond commits and comments.
8. Push fixes and repeat the PR state, CI, and feedback checks.
   - Re-fetch review threads after CodeRabbit, Codex, or other review automation has had time to update.
   - Continue while `reviewDecision` is `CHANGES_REQUESTED`, required checks are pending or failing, expected bot reviews are pending, unresolved actionable review threads remain, or `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`.
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
- Expected CodeRabbit, Codex, or other bot reviews have completed. If checks pass but an expected bot review is still pending, report `pending external review` instead of merge-ready.
- All actionable human, bot, CodeRabbit, Codex, or agent review comments are fixed, resolved, or explicitly explained as not applicable in the PR comment.
- Thread-aware review data shows no unresolved current actionable review threads.

If `mergeable` is `MERGEABLE` but `mergeStateStatus` remains `BLOCKED`, keep investigating branch protection, unresolved requested changes, required review state, required conversations, or pending checks. Do not report the PR as mergeable until the blocking reason is gone or documented as an external blocker.

## Loop control

- Default to 5 fix-and-push attempts per PR.
- Cap each CI or review wait window at 30 minutes, or 30 polling checks at 60-second intervals. If checks are still pending after that, report `pending external review` instead of waiting indefinitely.
- If the same CI failure or review comment returns after two fixes, stop broad changes and inspect the underlying assumption before trying again.
- For cross-repo work, finish and report one PR before moving to the next so context loss still leaves useful progress.

## Final Report

Group by repo when multiple PRs are involved. Include:

- PR URL, identifier, and branch
- feedback sources inspected, including CodeRabbit/Codex thread status
- CI runs watched and final status
- fixes pushed and commits
- comments or review feedback addressed, including any suggestions intentionally not applied
- PR comment posted or drafted
- unresolved actionable thread count
- final state: merge-ready, pending external review, or blocked with reason
