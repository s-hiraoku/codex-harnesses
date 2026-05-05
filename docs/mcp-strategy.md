# MCP Strategy

MCP is the layer for external tools and knowledge access. It should not replace project guidance, task workflows, hooks, policies, or verification scripts.

This repository does not implement an MCP server yet. It documents useful MCP categories for Codex harnesses.

## Suggested Categories

## GitHub

Repository metadata, issues, pull requests, review comments, CI status, release notes, and deployment history.

## Docs and Knowledge Base

Official documentation, internal runbooks, API references, architecture decisions, and product requirements.

## Browser and Playwright

Browser automation, UI inspection, screenshots, accessibility checks, and end-to-end flow verification.

## Local Repo Tools

Search, build tools, test runners, linters, typecheckers, dependency analyzers, and code generation commands.

## Memory and Task Ledger

Long-running task state, decisions, risks, verification history, and handoff summaries.

## Boundary

MCP should provide access. It should not silently enforce policy. Enforcement belongs in hooks, sandboxing, review, and deterministic verification.

