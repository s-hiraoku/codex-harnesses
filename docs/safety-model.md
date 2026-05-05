# Safety Model

Safety should be layered. No single prompt, hook, policy, or review step is enough.

## Prompt Guidance

`AGENTS.md` and skills describe expected behavior. They are useful for shaping work, but they are not enforcement.

## Policy

Policy files make approval, sandboxing, verification, and git-risk expectations explicit. They should be conservative for important repositories.

## Hooks

Hooks are deterministic scripts that can block likely secrets, dangerous commands, or unverified stop events. The examples here are starting points, not hardened production systems.

## Sandboxing

Sandboxing limits the blast radius of mistakes. Prefer restricted write access and explicit approval for network, destructive, or credential-sensitive operations.

## Review

Human and automated review should check behavior, security, migrations, and documentation. Review is especially important for changes that touch authentication, permissions, data deletion, billing, or deployment.

## Git Isolation

Use branches and worktrees to isolate changes. Avoid force pushes and hard resets unless there is an explicit, reviewed reason.

