---
name: finish-pr-feedback
description: Resume and finish stalled GitHub pull requests by inspecting each relevant repo PR, fixing all actionable CodeRabbit, Codex, human review, and CI feedback, pushing focused fixes, and stopping only when the PR is merge-ready or has a concrete external blocker. Use when PR work was left midway, when a user asks to fix reviewer or bot comments across repos, or when CodeRabbit/Codex comments must be handled after PR creation.
---

# Finish PR Feedback

Use this workflow when a PR already exists and the goal is to recover from incomplete follow-up. The output must be a merge-ready PR or a clear blocker, not a partial status report.

## Workflow

1. Resolve target PRs.
   - Use explicit repo/PR URLs when provided.
   - If the user says "each repo" or "all repos", scan the current workspace's git repositories and list open PRs for the current branch and for recent branches owned by the user.
   - If multiple PRs are found, process them one repo at a time and keep the final report grouped by repo.
2. Load local repo instructions before edits.
   - Read `AGENTS.md`, `CLAUDE.md`, package scripts, branch status, and PR metadata for the active repo.
   - Preserve unrelated local changes.
3. Build a complete feedback inventory.
   - Read PR state, checks, comments, reviews, and thread-aware review data.
   - For CodeRabbit, Codex, and other agents, treat top-level "actionable comments posted" summaries as pointers, not proof that all inline comments were fetched.
   - Read `references/pr-feedback-audit.md` for the concrete `gh` and GraphQL commands when thread state, bot comments, or cross-repo scanning matters.
4. Classify every item.
   - `fix`: code, docs, tests, CI, or config change is needed.
   - `respond`: reviewer asked for clarification and no code change is appropriate.
   - `ignore`: duplicate, outdated, already resolved, or demonstrably wrong.
   - `blocked`: needs credentials, product decision, external service, or maintainer action.
5. Implement all `fix` items.
   - Keep edits scoped to the PR and trace each change back to a feedback cluster.
   - Add or update tests when the feedback identifies behavior risk.
   - Commit and push in focused batches. Do not rewrite unrelated user changes.
6. Handle `respond` and `ignore` items explicitly.
   - Leave a concise PR comment or review reply when a suggestion is not applied.
   - Do not resolve GitHub review threads unless the user explicitly allows write actions beyond commits and comments.
7. Re-check after every push.
   - Watch CI or poll checks until required checks pass, fail, or hit the retry cap.
   - Re-fetch review threads after CodeRabbit/Codex has had time to update.
   - Continue while `reviewDecision` is `CHANGES_REQUESTED`, required checks are pending/failing, or unresolved actionable review threads remain.
8. Apply the final merge-ready gate.
   - Success requires passing required checks, no requested changes, no unresolved actionable CodeRabbit/Codex/human threads, and a clean enough `mergeStateStatus`.
   - If any bot review is still pending, report "checks passed, bot review pending" instead of merge-ready.
   - If a real blocker remains, include the exact repo, PR, blocking status, evidence, and next human action.

## Loop Limits

- Default to 5 fix-and-push attempts per PR.
- If the same failure or review comment returns after two fixes, stop broad changes and inspect the underlying assumption before trying again.
- For cross-repo work, finish and report one PR before moving to the next so context loss still leaves useful progress.

## Final Report

Group by repo and include:

- PR URL and branch
- feedback sources inspected, including CodeRabbit/Codex thread status
- fixes pushed and commits
- local verification and CI status
- unresolved actionable thread count
- final state: merge-ready, pending external review, or blocked with reason
