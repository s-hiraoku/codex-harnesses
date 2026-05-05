# Library Repository Guidance

Use this template for packages, SDKs, and reusable libraries.

## Expectations

- Preserve public APIs unless a breaking change is explicitly requested.
- Add or update tests for changed behavior.
- Keep examples and reference docs aligned with the implementation.
- Avoid broad rewrites when a focused change will solve the problem.
- Document migrations for breaking changes.

## Verification

- Run tests for changed behavior.
- Run typecheck, lint, and build commands when available.
- Check package metadata and release notes for release-facing changes.

## Final Response

Summarize API impact, changed files, verification, and migration notes if needed.

