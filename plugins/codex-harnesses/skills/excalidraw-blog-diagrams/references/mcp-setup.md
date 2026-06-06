# Excalidraw MCP Setup Notes

## Preferred MCP

For AI-generated blog diagrams in this repo, prefer the local stdio MCP:

```bash
codex mcp add excalidraw -- npx -y @scofieldfree/excalidraw-mcp
```

Use it when the agent needs repeatable file creation, local previews, or export to `.excalidraw`, SVG, PNG, or JSON.

## Official Remote MCP

The official remote MCP is useful when the client supports MCP Apps or an interactive remote Excalidraw experience:

```bash
codex mcp add excalidraw --url https://mcp.excalidraw.com
```

Prefer the local MCP if the task is primarily repository asset generation.

## Discovery

After adding an MCP, restart the Codex session if the tool list is not refreshed. Then search for Excalidraw tools before drawing.

Use shell checks to confirm registration:

```bash
codex mcp list
codex mcp get excalidraw
```

## Fallback

If MCP is unavailable, create `.excalidraw` JSON directly only for simple diagrams and export with a known Excalidraw exporter. Do not hand-roll complex Excalidraw element geometry unless the user explicitly accepts rough output.
