---
name: jina-read-url
description: Read, summarize, inspect, or extract content from a public URL through Jina Reader. Use when the user asks to use Jina Reader, read a note.com/blog/article/X/Twitter/GitHub/page URL, recover Markdown from a URL that normal browsing cannot read cleanly, or make a URL readable in ChatGPT-like agent sessions with tool access.
---

# Jina Read URL

## Overview

Use Jina Reader as the narrow URL-to-Markdown step for public web pages, then answer from the returned Markdown. Keep this skill focused on reading the URL; save to memory, send to another agent, or archive output only when the user explicitly asks.

## Quick Start

Prefer the bundled script:

```bash
python3 scripts/read_url.py "https://example.com/page"
```

The script prints Markdown from `https://r.jina.ai/`. If `JINA_API_KEY` is set, it sends it as a bearer token. Otherwise, it uses public unauthenticated access.

Use `--output` when the fetched Markdown is large or the user asks to save it:

```bash
python3 scripts/read_url.py "https://example.com/page" --output /tmp/page.md
```

## Workflow

1. Take the public URL from the user. If the URL has no scheme, assume `https://`.
2. Fetch with `scripts/read_url.py` instead of manually constructing the Jina URL, especially for long URLs, URLs containing `#`, X/Twitter URLs, or repeated use.
3. Inspect the returned Markdown for:
   - title
   - source URL
   - published time, author, or other visible metadata
   - whether the content appears complete, sparse, blocked, rate-limited, or login-gated
4. Answer only from the returned content unless you clearly mark outside knowledge or corroborate with another source.
5. Keep direct quotes short and attribute them to the source URL.
6. Do not treat Jina Reader as an authorization bypass. It can only reliably read content that is publicly accessible to Jina.

## Default Response

For casual read-or-summarize requests, return:

- whether the page was readable
- title
- source URL
- published time when present
- a concise summary or extracted points
- any uncertainty about completeness

## ChatGPT-Style Environments

If running in a ChatGPT-like session with no shell, fetch, browser, or custom Action access, say that the environment cannot directly call Jina Reader. If a Custom GPT Action or proxy is available, call the action that wraps `https://r.jina.ai/` and then follow the same workflow above.

## Script

`scripts/read_url.py` accepts:

```bash
python3 scripts/read_url.py URL [--output path] [--timeout seconds] [--header "Name: value"]
```

The script avoids double-prefixing existing `r.jina.ai` Reader URLs, uses POST for fragment or very long URLs, and returns a non-zero exit code with a concise error message when Jina Reader cannot be reached.

## Final Report

Include:

- URL fetched
- whether Jina Reader returned complete-looking Markdown or partial/blocked content
- summary, extracted facts, or saved output requested by the user
- any follow-up action taken only because the user explicitly requested it
