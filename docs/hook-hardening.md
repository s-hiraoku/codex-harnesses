# Hook Hardening

The hooks in this repository are examples. They show where deterministic enforcement can live, but they are not production-ready security controls by default.

Use this guide when adapting an example hook for an important repository.

## Payload vs Registration

This repository provides payload scripts:

- read stdin or repository state
- decide allow or block
- print a clear reason
- return a deterministic exit code

Your Codex environment provides registration:

- which lifecycle event calls the hook
- what input the hook receives
- whether a block is advisory or enforced
- how hook failures are surfaced

Keep those responsibilities separate. Test the payload script before wiring it into a lifecycle event.

## Secret Guard Hardening

The example `secret-guard` detects a small set of likely secrets. Before relying on it:

- add patterns for the providers used by the project
- include known private key and certificate formats
- add allowlists for test fixtures and documented dummy values
- avoid printing matched secret values in error output
- test both true positives and false positives

For high-risk repositories, use a maintained secret scanner in addition to this hook.

## Dangerous Command Guard Hardening

The example `dangerous-command-guard` is not a shell parser. Before relying on it:

- define which commands are blocked, allowed, or approval-only
- account for aliases, shell wrappers, and command substitutions
- block secret-reading commands for project-specific credential files
- test destructive command variants, not just exact examples
- fail closed when the hook cannot parse required input

Use sandboxing and approval policy alongside command guards. A command hook should not be the only protection against destructive edits.

## Stop Verify Hardening

The example `stop-verify` runs `scripts/verify.sh`. Before relying on it:

- make sure `scripts/verify.sh` runs real project checks
- run CI with strict verification
- keep verification output visible
- decide whether missing tools should block stopping
- document any checks that are intentionally skipped

Verification hooks should fail loudly. Do not convert failed checks into warnings unless the repository policy explicitly allows it.

## Test Requirements

A hardened hook should have tests for:

- allowed input
- blocked input
- malformed input
- missing required tools or files
- clear stderr messages
- expected exit codes

Keep the test cases close to the hook. When a hook protects a project-specific rule, add project-specific tests in that repository.

## Operational Rules

- Do not log secrets, even in failure output.
- Prefer explicit blocked reasons over generic failure messages.
- Keep hooks small and deterministic.
- Version hook changes with the repository they protect.
- Review hook changes like security-sensitive code.

