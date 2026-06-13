# MCP Recipes

MCP servers add external tool and knowledge access. Treat them as opt-in dependencies: review the source, required credentials, and write surface before enabling a server in a project.

This repository ships a disabled-by-default recipe at `mcp/recipes/curated.mcp.json`. Copy the recipe into the target project's MCP configuration, then move only the servers you need from `_disabled` into `mcpServers`.

## Why Disabled by Default

MCP servers can start extra processes, make network calls, and expose credentials or write tools. A harness should not silently expand a repository's tool surface. Enable servers one at a time and document why each one is needed.

## GitHub

- Source: `@modelcontextprotocol/server-github`
- Auth: `GITHUB_PERSONAL_ACCESS_TOKEN`
- Recommended use: issues, pull requests, repository metadata, code search, and CI context.
- Permission note: prefer a fine-grained token scoped to the repositories under active work. Add write-capable tools only for sessions that intentionally update GitHub state.

## Playwright

- Source: `@playwright/mcp`
- Auth: none by default.
- Recommended use: browser automation, UI regression checks, screenshots, accessibility snapshots, and end-to-end flow reproduction.
- Permission note: browser state and downloads can persist outside the repository. Keep test sessions isolated when possible.

## Context7

- Source: `@upstash/context7-mcp`
- Auth: optional API key for higher limits.
- Recommended use: current version-specific framework and SDK documentation.
- Permission note: prefer official upstream docs through the server and cite version-sensitive claims in final reports.

## Serena

- Source: `oraios/serena`
- Auth: none by default.
- Recommended use: semantic code navigation and symbol-aware refactoring in larger repositories.
- Permission note: start with read/navigation tools. Enable edit tools only when the project has verification coverage for refactors.

## Sequential Thinking

- Source: `@modelcontextprotocol/server-sequential-thinking`
- Auth: none by default.
- Recommended use: structured reasoning for architecture decisions, root-cause analysis, and ambiguous multi-step debugging.
- Permission note: treat output as scaffolding. It should slow down decisions, not replace tests or review.

## Sentry

- Source: `@sentry/mcp-server`
- Auth: `SENTRY_AUTH_TOKEN`
- Recommended use: production error triage, stack traces, issue frequency, and release health context.
- Permission note: use read-only scopes such as event, project, and organization read access unless an operational task explicitly requires writes.

## Filesystem MCP

Do not add a filesystem MCP server by default. Codex already has repository file tools with permission integration, and an additional filesystem server expands attack surface without adding much value.
