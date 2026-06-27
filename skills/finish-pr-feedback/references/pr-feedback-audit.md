# PR Feedback Audit

Use these commands when a PR may have unresolved CodeRabbit, Codex, human review, or CI feedback. Prefer explicit PR URLs; otherwise run from the repo checkout.

## Resolve PRs

Current branch PR:

```sh
gh pr view --json number,url,headRefName,baseRefName,isDraft,author
```

Open PRs in the current repo:

```sh
gh pr list --state open --json number,url,headRefName,baseRefName,isDraft,author,updatedAt,title
```

Workspace scan from an org folder:

```sh
find . -maxdepth 2 -type d -name .git -print | sed 's#/.git$##' | sort
```

For each repo path, `cd` into it and run the open PR command. Prioritize PRs whose head branch is checked out locally, authored by the user, recently updated, or explicitly named by the user.

## Read PR State

```sh
gh pr view <pr> --json number,url,title,headRefName,baseRefName,isDraft,mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments,latestReviews,reviewRequests
gh pr checks <pr>
```

Inspect failing logs:

```sh
gh run list --branch <head-branch> --limit 10
gh run view <run-id> --log-failed
```

## Fetch Thread-Aware Review Data

Flat PR comments are not enough for CodeRabbit or Codex because actionable feedback is often in inline review threads. Use GraphQL:

```sh
gh api graphql \
  -f owner='<owner>' \
  -f name='<repo>' \
  -F number=<number> \
  -f query='
query($owner:String!, $name:String!, $number:Int!) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      url
      reviewDecision
      mergeStateStatus
      reviewThreads(first:100) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          isResolved
          isOutdated
          path
          line
          startLine
          comments(first:20) {
            nodes {
              id
              url
              author { login }
              body
              createdAt
              outdated
              diffHunk
            }
          }
        }
      }
    }
  }
}'
```

If there are more than 100 threads, paginate with `pageInfo { hasNextPage endCursor }` and `after`.

## Identify Agent Feedback

Search both thread comments and top-level comments for authors or markers like:

- `coderabbitai`, `coderabbitai[bot]`, `CodeRabbit`
- `codex`, `codex[bot]`, `openai`, `OpenAI`
- `github-actions`, `Copilot`, or repo-specific review bots
- phrases such as `Actionable comments posted`, `requested changes`, `nitpick`, `issue`, `bug`, `failing`, `blocking`

Treat outdated threads as non-actionable only after checking whether the same point reappears in a current thread or latest bot summary.

## Completion Gate

Before reporting success, run:

```sh
gh pr view <pr> --json mergeStateStatus,mergeable,reviewDecision,statusCheckRollup,reviews,comments,latestReviews
gh pr checks <pr> --watch
```

Then re-run the GraphQL thread query and count unresolved actionable current threads. The PR is not merge-ready if:

- `reviewDecision` is `CHANGES_REQUESTED`
- any required check is pending, skipped unexpectedly, cancelled, or failing
- `mergeStateStatus` is `BLOCKED`, `DIRTY`, `UNKNOWN`, or `BEHIND`
- CodeRabbit/Codex says actionable comments remain
- unresolved current review threads contain actionable feedback
- the PR is draft and the user wanted ready-for-review

Allowed final states:

- `merge-ready`: all gates pass
- `pending external review`: local fixes and required checks pass, but a bot or maintainer review has not completed
- `blocked`: a specific external blocker prevents completion
