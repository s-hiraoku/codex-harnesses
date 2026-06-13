# MCP Tool Allowlist Hook

Example hook that blocks MCP tool calls unless the tool name matches `CODEX_HARNESSES_MCP_ALLOW`.

The allowlist is comma-separated and supports shell-style wildcards:

```sh
export CODEX_HARNESSES_MCP_ALLOW="mcp__github__list_*,mcp__github__get_*,mcp__playwright__*"
```

## Usage

```sh
printf '%s\n' 'mcp__github__create_issue' | python3 hooks/mcp-tool-allowlist/hook.py
```

Use read-only patterns by default. Add write tools only for sessions that intentionally need them.
