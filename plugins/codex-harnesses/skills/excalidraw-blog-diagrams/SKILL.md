---
name: excalidraw-blog-diagrams
description: Use when creating, revising, exporting, or reviewing Excalidraw diagrams for technical blog posts, Zenn articles, markdown content, architecture diagrams, workflow diagrams, concept maps, comparison diagrams, or article illustrations using Excalidraw MCP, .excalidraw files, SVG, PNG, Mermaid-to-Excalidraw, or diagram image assets.
---

# Excalidraw Blog Diagrams

## Overview

Use Excalidraw as the editable source of truth for blog diagrams, and export article-ready SVG or PNG assets. Optimize for a reader skimming a technical article, not for a whiteboard session.

## Tool Selection

Prefer Excalidraw MCP when available. Search for MCP tools named or described as `excalidraw`, `diagram`, `canvas`, `export`, `svg`, `png`, or `mermaid`.

If no Excalidraw MCP tool is connected, tell the user and suggest one of these setup commands:

```bash
codex mcp add excalidraw -- npx -y @scofieldfree/excalidraw-mcp
codex mcp add excalidraw --url https://mcp.excalidraw.com
```

Use local MCP first for repeatable file export in this repo. Use the official remote MCP when the user wants an interactive MCP App experience.

For detailed setup notes, read [references/mcp-setup.md](references/mcp-setup.md) only when MCP configuration or installation is part of the task.

## Workflow

1. Identify the diagram's job in one sentence: explanation, comparison, architecture, timeline, workflow, or mental model.
2. Choose one diagram type. Do not combine multiple types into one dense figure.
3. Draft the structure before drawing: nodes, edges, groups, and labels.
4. Create or update the `.excalidraw` source with MCP.
5. Export article assets as SVG by default; use PNG when the article platform or visual style needs raster output.
6. Inspect the exported asset. Check that text is readable, arrows are unambiguous, no labels overlap, and the file format matches its extension.
7. Report the source path and exported asset path.

## Repo Paths

Use these paths unless the article has an established image directory:

```text
diagrams/<slug>.excalidraw
assets/images/<slug>.svg
assets/images/<slug>.png
```

For article-specific image folders, mirror the article slug:

```text
images/<article-slug>/<figure-slug>.svg
images/<article-slug>/<figure-slug>.png
```

Never leave the only editable source under a tool cache such as `~/.gemini`, `/tmp`, or an MCP workspace. Copy the final `.excalidraw` source into the repo.

## Readability Rules

- Keep one figure to 3-7 major objects.
- Use short labels: 1-4 words for nodes, one line when possible.
- Prefer left-to-right flow for processes and top-to-bottom flow for layered systems.
- Use thick enough strokes and high contrast for screenshots and mobile readers.
- Use 16:9 or 4:3 for article hero/inline diagrams; use tall layouts only for step-by-step flows.
- Use color sparingly: one accent color for the main path, gray for context, red/orange only for risk or failure.
- Put explanatory detail in the blog prose, not inside tiny diagram text.
- Avoid decorative icons unless they clarify the domain.
- Avoid crossing arrows. If crossings are unavoidable, split the diagram.

## Blog-Specific Patterns

Architecture:

```text
User -> Client -> API -> Queue -> Worker -> Database
```

Show ownership boundaries with lightly tinted containers. Label data movement arrows with verbs, not nouns.

Workflow:

```text
Trigger -> Decision -> Action -> Verification -> Outcome
```

Use diamonds only for real branching decisions. If there is no branch, use rectangles.

Comparison:

```text
Before | After
```

Keep the same layout on both sides so the visual difference is meaningful.

Mental model:

```text
Outer context -> Inner mechanism -> Result
```

Use nested frames only when containment is the core idea.

## Export Checks

After export, verify with shell tools:

```bash
file assets/images/<name>.png
file assets/images/<name>.svg
```

If a file has a mismatched extension, fix it before finishing. For example, a JPEG saved as `.png` must be converted or renamed.

When possible, open or inspect the rendered image before finalizing. The figure must still be legible at roughly 700 px wide.

## Final Report

Include the diagram purpose, `.excalidraw` source path, exported asset path, file type verification, and any limitations such as missing MCP access or skipped visual inspection.

## Common Mistakes

- Creating a diagram that restates the article title instead of explaining one specific idea.
- Putting full sentences into boxes.
- Using too many colors, arrows, or nested groups.
- Exporting only PNG and losing the editable `.excalidraw` source.
- Trusting a tool's reported format without checking the actual file type.
