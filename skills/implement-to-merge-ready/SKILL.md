---
name: implement-to-merge-ready
description: Run an end-to-end implementation delivery workflow from user request to merge-ready pull request. Use when the user asks Codex to implement a change and expects planning, goal tracking, UI design where relevant, code edits, tests, self-review, regular ready-for-review PR creation, CI/review follow-up, and bringing the PR as close to mergeable as possible.
---

# Implement To Merge Ready

## Overview

Use this as an orchestration workflow for implementation tasks that should not stop at local code changes. Drive the task from intake through PR stabilization, using narrower skills and tools when their trigger conditions apply.

## Workflow

1. Confirm scope and repository state.
   - Read local instructions such as `AGENTS.md` before editing.
   - Inspect `git status`, branch, remotes, package scripts, tests, and relevant source structure.
   - Ask only when ambiguity would cause risky or irreversible work.
   - Preserve unrelated user changes.

2. Set a goal for substantial work.
   - Use goal tracking when the task includes implementation plus verification or PR work.
   - Write the objective in outcome terms: behavior to deliver, verification to run, PR to open, and merge-readiness follow-up.
   - Check the goal again after resumes, direction changes, and before the final report.

3. Plan the implementation.
   - State a concise plan once enough context is known.
   - Choose the narrowest applicable implementation mode: feature, bug fix, refactor, docs, frontend, backend, or CI repair.
   - Keep the plan reviewable and update it when discoveries change the work.

4. Design UI work before coding when relevant.
   - Use `ui-imagegen-director` for UI visual direction when the UI design quality or visual target matters.
   - For HTML/CSS/client-side UI work, use current frontend guidance before implementation.
   - Match existing product patterns and design systems.
   - Build the actual usable screen or flow, not a marketing placeholder, unless the request is specifically for marketing.
   - Verify responsive layouts and important visual states in a real browser after significant UI edits.

5. Implement in focused steps.
   - Prefer existing project patterns, APIs, and tests.
   - Keep commits and code changes scoped to the request.
   - Update docs when commands, configuration, APIs, workflows, or user-visible behavior changes.
   - Do not rewrite unrelated code for style or broad cleanup.

6. Verify locally.
   - Run targeted tests first, then broader lint/type/build/test commands when practical.
   - For UI changes, run the app if needed and inspect the changed flow with browser screenshots or interaction checks.
   - If a check cannot run, capture the exact blocker and any partial verification completed.

7. Review before PR.
   - Inspect `git diff` and review for bugs, regressions, missing tests, data loss, security issues, and edge cases.
   - Fix actionable issues found during self-review before committing.
   - Confirm the final diff does not include unrelated files or generated noise.

8. Commit, push, and open a PR.
   - Create a clear commit history appropriate to the repo.
   - Push the branch to the expected remote.
   - Open a regular ready-for-review pull request by default.
   - Do not create a draft PR and do not pass `--draft` unless the user explicitly asks for a draft.
   - Include a PR body with summary, tests, screenshots when useful, and known risks.

9. Bring the PR toward merge-ready.
   - Check PR status, required checks, CI runs, review requests, bot comments, and unresolved review threads.
   - Watch CI when practical. On failure, inspect logs, reproduce locally when possible, make the smallest fix, push, and re-check.
   - Collect actionable human, bot, and agent feedback from every available source before deciding the PR is done: unresolved review threads, PR comments, bot review summaries, agent handoff notes, CI annotations, and follow-up messages in the Codex thread.
   - Use `pr-guardian` when CodeRabbit, Codex, or review automation posts "Actionable comments posted", requested changes, or inline comments after the PR is opened.
   - Treat each actionable agent finding as a tracked fix item. Implement all such items, re-run the relevant local verification, push the fixes, and re-check the PR.
   - Repeat the feedback pass until no actionable human, bot, or agent feedback remains. A single pass is not enough when new comments can appear after pushing fixes.
   - If feedback conflicts, is incorrect, or cannot be fixed without changing scope, explain that specific item and mark the PR blocked or waiting for user input instead of calling it complete.
   - Do not treat the PR as merge-ready while any required check, bot review, or review status is still pending. Wait and re-check after checks/reviews appear; if a bot such as CodeRabbit remains pending after a reasonable watch window, report the PR as "CI passed, bot review pending" rather than complete or merge-ready.
   - Before finalizing, perform a thread-aware review check when available and report the count of unresolved current review threads and unresolved actionable agent findings. If either count is nonzero, continue addressing the items or report the exact blocker.
   - Leave the PR in a state where required checks pass and no known actionable human, bot, or agent feedback remains, or report the exact blocker.
   - Do not merge unless the user explicitly asks and the repo policy permits it.

## Skill Composition

Use narrower skills when available and relevant:

- `goal-manager` for objective and completion tracking.
- `feature-implementation`, `bug-fix`, `refactor-safely`, or `docs-updater` for the local code-change phase.
- `ui-imagegen-director` for UI design direction and image-generated mockups when visual quality matters.
- `modern-web-guidance`, Browser, and Playwright for frontend implementation and verification.
- `review` for bug-first self-review before publishing.
- GitHub PR and CI skills or tools for PR creation, check inspection, and review-thread follow-up.
- `pr-guardian` after the PR is open when the user expects continued monitoring and fixes.

## Progress Updates

Keep the user informed at phase boundaries:

- after repository/context inspection
- before edits
- after local verification
- after PR creation
- after CI or review follow-up

## Final Report

Include:

- goal status, when goal tracking was used
- changed behavior and key files
- local checks run and results
- PR URL, branch, and CI/review status
- fixes made after PR creation
- unresolved current review-thread count
- unresolved actionable agent-finding count
- remaining blockers, risks, or pending checks

If any check or bot review is pending, say so explicitly and do not call the PR merge-ready.
If any actionable agent finding remains unresolved, say so explicitly and do not call the task complete or merge-ready.
