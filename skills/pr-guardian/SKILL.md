---
name: pr-guardian
description: Monitor or resume GitHub pull requests, fix CI failures and actionable CodeRabbit, Codex, bot, or human review feedback, push focused updates, and stop only when the PR is merge-ready or has a concrete external blocker.
---

# PR Guardian

Use this workflow by default after opening a pull request, and when an existing PR needs follow-up after CI, CodeRabbit, Codex, bot, or human review feedback. The goal is to leave the PR merge-ready or report a specific blocker, not to provide a partial status update.

## Workflow

0. Delegate passive monitoring to a compatible guardian runner.
   - Read `references/guardian-event-contract.md`. Require `kaizen-loop guardian capabilities --json` to advertise schema version 1 and durable completion notification support before monitoring. When the repository is registered with a compatible kaizen-loop, start `kaizen-loop guardian run <pr-number> --project <project-slug> --json` once through an execution path that can deliver its terminal event without asking Codex to inspect repeated process snapshots.
   - Do not repeatedly call a tool to poll the guardian process, GitHub, CI, review bots, or the stabilization window. Sleeps, `gh run watch`, GitHub API polling, head-change detection, review-completion checks, and stabilization are passive runner work and must not consume Codex reasoning cycles.
   - If the execution transport yields before completion, use its non-LLM completion notification or detach the durable job and record its job/event location. End the invocation as `monitoring delegated`; resume only from a terminal event. Do not wake Codex merely to observe that nothing changed.
   - Require one terminal event that passes `scripts/validate_guardian_event.py` for the expected repo, PR, job, sequence, and head, as well as a successful runner exit, before accepting `merge_ready`. Confirm the remote head once when consuming that event. Treat missing, stale, mismatched, malformed, or unsupported event output as `blocked: incompatible guardian runner`, never as success.
   - If no compatible durable runner or completion notification exists, inspect and fix immediately actionable state, but do not reproduce the wait loop with agent tool calls. Report `blocked: passive guardian runner unavailable` with the missing capability and installation or upgrade action.
   - `gh pr checks --watch` is only a CI watcher and never satisfies review/thread monitoring by itself.
   - Treat `success` as a convergence checkpoint, not a permanent terminal state while the PR remains open. The durable runner must re-observe successful jobs and reactivate a same-head PR when late review threads, checks, or merge-gate activity make it non-ready.
   - Run durable jobs in a disposable worktree pinned to the observed head. Before pushing, re-read the remote head SHA; if it changed, stop and reconcile the new head instead of overwriting it.

1. Resolve the GitHub CLI before doing any PR work.
   - Resolve a usable GitHub CLI as `GH_BIN`: try `command -v gh`, the active Nix user profiles (`$HOME/.nix-profile/bin/gh` and `$HOME/.local/state/nix/profiles/profile/bin/gh`), `/run/current-system/sw/bin/gh`, then platform fallbacks such as `/opt/homebrew/bin/gh` and `/usr/local/bin/gh`. Use the resolved absolute path for every command in this workflow; desktop and sandboxed agent shells may intentionally sanitize the user's interactive `PATH`.
2. Resolve the target PRs.
   - Use explicit repo or PR URLs when provided.
   - Otherwise identify the current branch PR, branch, remote, and expected base branch.
   - If the user asks for "each repo" or "all repos", scan the relevant workspace repositories, list open PRs, and process one repo at a time.
   - If the user says a PR is still blocked, still remains, or points at a repository PR list, enumerate the open PRs in the relevant repositories and process every PR that is `BLOCKED`, has unresolved review threads, or has actionable bot/human feedback. Do not stop after fixing only the current checkout's branch.
   - Derive the target host and repository from the resolved PR URL or remote. Run `"$GH_BIN" auth status --active --hostname <host>` and a read-only `"$GH_BIN" api --hostname <host> repos/<owner>/<repo> --jq .full_name`. An authentication failure on an unrelated host or inactive account is not a blocker. A missing executable, failed target-host authentication, or insufficient target-repository access is a concrete blocker; report the exact failed command and stderr.
3. Load local repo context before edits.
   - Read local instructions such as `AGENTS.md`, package scripts, branch status, and PR metadata.
   - Preserve unrelated local changes.
4. Build a complete PR state and feedback inventory.
   - Read `mergeStateStatus`, `mergeable`, `reviewDecision`, `statusCheckRollup`, `reviews`, `latestReviews`, review requests, PR comments, and `gh pr checks`.
   - Always fetch thread-aware review data before claiming success. Flat PR comments are not enough because CodeRabbit, Codex, and human actionable feedback is often in inline review threads.
   - Do not treat an earlier PR Guardian summary comment as current evidence. A bot review can arrive after that comment, so every resume must re-fetch PR state, comments, reviews, latest reviews, and review threads from GitHub.
   - Read `references/pr-feedback-audit.md` and run its executable GraphQL cursor loops and REST `--paginate` commands on every target PR before deciding that no feedback remains. Paginate every connection until `hasNextPage=false` by feeding each `endCursor` into the next request, including nested review comments, and exhaust REST reviews, review comments, issue comments, check runs, and annotations. Summaries and first pages are not complete evidence.
5. Classify every feedback item.
   - `fix`: code, docs, tests, CI, or config change is needed.
   - `respond`: a reviewer asked for clarification and no code change is appropriate.
   - `ignore`: duplicate, outdated, already resolved, or demonstrably wrong.
   - `blocked`: credentials, product decision, external service, or maintainer action is required.
6. Handle CI events.
   - Let the durable runner watch pending CI. Use `gh run view` and failing logs only after the runner reports an actionable CI failure.
   - If CI fails, inspect failing jobs and logs, reproduce locally when practical, and make the smallest fix.
7. Implement all `fix` items.
   - Keep edits scoped to the PR and trace each change back to a feedback or CI cluster.
   - Add or update tests when the feedback identifies behavior risk.
   - Do not rewrite unrelated user changes or broaden the PR scope.
8. Handle every current review thread explicitly.
   - Required conversation resolution is per GitHub review thread, not per PR. The merge gate "all comments must be resolved" is satisfied only when every unresolved `reviewThreads` node has been replied to or intentionally handled and then resolved.
   - For `fix` items, reply in the same review thread or directly to the review comment with the fix made and validation run.
   - For `respond` and `ignore` items, reply in the same review thread or directly to the review comment with the clarification or reason the suggestion is not applicable.
   - Reply before resolving. Use the thread's first review comment `fullDatabaseId` for the REST reply endpoint, then resolve the thread with the GraphQL `reviewThreads.nodes[].id`.
   - Resolve each addressed GitHub review thread, including outdated unresolved threads, when permissions allow. If GitHub does not allow replying or resolving, report the thread URL as `blocked: unresolved required conversation`.
   - Do not rely on an aggregate PR comment as a substitute for per-thread disposition; repositories with required conversation resolution stay blocked until each current thread is resolved.
9. Push fixes and return control to the durable runner.
   - After a push, start or reactivate the runner once and end the reasoning pass. Do not have Codex supervise the runner's wait cycle.
   - The runner must re-fetch review threads after CodeRabbit, Codex, or other review automation updates. While a review bot is `pending` or `in_progress`, unresolved-thread counts are provisional and must not appear in a terminal `merge_ready` event.
   - After every expected review bot reaches a terminal state, the runner must re-fetch thread-aware review data before emitting another actionable event or `merge_ready`. New bot comments can appear after CI is already green.
   - Pin the current PR head SHA at the start of every monitoring cycle. After any push, discard all earlier review-completion and quiet-period evidence. Fetch paginated reviews from the REST `pulls/<pr>/reviews` endpoint; an expected bot review counts as complete only when its terminal review `commit_id` equals the pinned head SHA, or a bot-specific terminal API result explicitly names that SHA. `gh pr view --json reviews` is not commit-SHA evidence, and a review with a missing or older SHA is not completion evidence.
   - After all expected bots have terminal evidence for the pinned head, the runner must start a bounded stabilization window. It waits at least 60 seconds, then fetches the head SHA, checks, merge state, review decision, comments, reviews, and all review threads twice, at least 30 seconds apart. Both snapshots must have the same head SHA and no new review or thread activity. Any new push, check transition, comment, review, or thread resets the runner-side window.
   - A rate limit, timeout, or missing current-head terminal review is `pending external review`, never merge-ready. Do not shorten the stabilization window because GitHub temporarily reports `CLEAN` or zero unresolved threads.
   - Continue while `reviewDecision` is `CHANGES_REQUESTED`, required checks are pending or failing, expected bot reviews are pending, any review thread remains unresolved, any actionable top-level PR comment lacks a clear disposition, or `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`.
10. Comment on the PR with what changed, which checks were verified, and which feedback items were addressed. If a suggestion is not applied, explain why and link to the per-thread reply. If no fixes were needed, claim merge-readiness only after the same final gate below passes; otherwise name the remaining blocker.

## Mergeability gate

When diagnosing an actionable event, inspect current state with commands such as:

```sh
"$GH_BIN" pr view <pr> --json isDraft,mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments,latestReviews,reviewRequests
"$GH_BIN" pr checks <pr>
```

Also re-run the thread-aware GraphQL query and count unresolved review threads:

```sh
"$GH_BIN" api graphql \
  -f owner='<owner>' \
  -f name='<repo>' \
  -F number=<number> \
  -f query='
query($owner:String!, $name:String!, $number:Int!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      reviewThreads(first:100, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          comments(first:20) {
            nodes {
              fullDatabaseId
              url
              author { login }
              body
              outdated
            }
          }
        }
      }
    }
  }
}'
```

If `pageInfo.hasNextPage` is true, paginate before counting unresolved threads. For each unresolved thread that has been handled, reply and resolve:

```sh
"$GH_BIN" api \
  --method POST \
  repos/<owner>/<repo>/pulls/<pr-number>/comments/<top-level-comment-full-database-id>/replies \
  -f body='Fixed in <commit>: <short disposition>. Verified with <command>.'

"$GH_BIN" api graphql \
  -f threadId='<review-thread-id>' \
  -f query='
mutation($threadId:ID!) {
  resolveReviewThread(input:{threadId:$threadId}) {
    thread { id isResolved }
  }
}'
```

Success requires all of these:

- `isDraft` is false. When the user owns the PR and requested merge-readiness, convert a draft with `"$GH_BIN" pr ready <pr-number-or-url> --repo <host/owner/repo>`; otherwise report the permission or author decision as a blocker. Never rely on the current branch to select the target PR.
- `mergeable` is exactly `MERGEABLE`, after retrying transient `UNKNOWN` while GitHub recomputes it.
- `mergeStateStatus` is clean enough for the repository to merge, usually `CLEAN`, `HAS_HOOKS`, or `UNSTABLE` with only non-required failures explicitly documented.
- `reviewDecision` is not `CHANGES_REQUESTED`.
- All required checks in `statusCheckRollup` pass.
- Expected CodeRabbit, Codex, or other bot reviews have completed, and thread-aware review data has been re-fetched after they completed. If checks pass but an expected bot review is still pending, report `pending external review` only after the wait window is exhausted, and make clear that the unresolved-thread count is not final while the bot is still processing.
- Every expected bot has terminal review evidence for the current head SHA, and the post-review stabilization window produced two unchanged, passing snapshots. Older-head reviews, SHA-less reviews, and a single transient `CLEAN` snapshot do not satisfy this gate.
- All actionable human, bot, CodeRabbit, Codex, or agent review comments are fixed, answered, or explicitly explained as not applicable in the relevant review thread or top-level PR conversation.
- Thread-aware review data shows zero unresolved review threads, including outdated threads. If any thread remains unresolved, do not report merge-ready even when `mergeable` is `MERGEABLE`; report `blocked: unresolved required conversations` with the thread URLs unless the only remaining step is a pending external reviewer action.

If `mergeable` is `MERGEABLE` but `mergeStateStatus` remains `BLOCKED`, keep investigating branch protection, unresolved requested changes, required review state, required conversations, or pending checks. Do not report the PR as mergeable until the blocking reason is gone or documented as an external blocker.

## Loop control

- Default to 5 fix-and-push attempts per PR.
- Do not spend a Codex turn between attempts merely to wait. Every push resets runner-side review evidence and reactivates the monitor cycle.
- Configure each runner-owned CI or review wait window with a 30-minute default. On expiry, the runner emits `timeout` with pending check or review names and a final current-head snapshot. It must not emit `merge_ready` from provisional review data.
- If the same CI failure or review comment returns after two fixes, stop broad changes and inspect the underlying assumption before trying again.
- For cross-repo work, finish and report one PR before moving to the next so context loss still leaves useful progress.

## Final Report

Group by repo when multiple PRs are involved. Include:

- PR URL, identifier, and branch
- feedback sources inspected, including CodeRabbit/Codex thread status
- CI runs watched and final status
- guardian terminal event schema version, event, head SHA, reset count, GitHub request counts, cycles, passive wait duration, and Codex action duration
- fixes pushed and commits
- comments or review feedback addressed, including per-thread replies, resolved thread count, and any suggestions intentionally not applied
- PR comment posted or drafted
- unresolved review-thread count, including outdated threads
- final state: merge-ready, pending external review, or blocked with reason
