---
name: security-review
description: Review a diff for concrete security risks across injection, authn/authz, secrets, supply chain, infrastructure, and business logic.
---

# Security Review

Use this workflow before merging or releasing changes that touch authentication, authorization, data handling, network surfaces, infrastructure, dependencies, or LLM-facing inputs.

## Workflow

1. Establish the review scope with the user request, current branch, pull request, commit range, or changed files.
2. Inspect the diff first, then read the smallest amount of surrounding code needed to validate each candidate issue.
3. Review by concern:
   - Injection: SQL, NoSQL, shell, template, deserialization, path traversal, prompt injection.
   - Authn/Authz: session handling, tokens, RBAC, object-level authorization, privilege boundaries.
   - Secrets: committed credentials, unsafe logging, insufficient redaction, private key material.
   - Supply chain: new dependencies, unpinned executables, lockfile drift, install scripts.
   - Infrastructure: public exposure, missing encryption, weak defaults, overly broad permissions.
   - Business logic: state bypasses, replay, race conditions, idempotency, rollback gaps.
4. Confirm reachability before reporting a finding. Do not report pattern matches that cannot execute.
5. Redact any secret values. Cite only enough structure to identify the issue safely.
6. Rank findings by severity and provide concrete fix directions.
7. If no issues are found, say so clearly and note the remaining verification gaps.

## Final Report

Lead with a verdict: `Ready to Merge`, `Needs Attention`, or `Needs Work`.

For each finding, include:

- severity
- file and line when available
- reachable path or trigger
- what can fail
- why it matters
- concrete fix direction

End with reviewed scope, verification consulted, and residual risks.
