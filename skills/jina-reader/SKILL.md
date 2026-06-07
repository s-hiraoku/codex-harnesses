---
name: jina-reader
description: Fetch public web pages with Jina AI Reader API and convert them into LLM-friendly Markdown. Use when an agent needs to read, summarize, quote briefly, extract facts from, or inspect a public URL that normal browsing, scraping, search snippets, or direct fetch tools cannot read cleanly, including JavaScript-heavy pages, reader-hostile pages, X/Twitter posts and threads, articles, GitHub pages, and PDFs. Trigger when the user asks to use Jina, use r.jina.ai, read an otherwise unreadable site, recover readable text from a URL, read an X/Twitter post by URL, or turn a webpage into Markdown.
---

# Jina Reader

## Quick Start

Use the bundled script when a public URL is hard to read through normal tools:

```bash
python3 scripts/read_url.py "https://x.com/user/status/1234567890"
```

The script prints Markdown from `https://r.jina.ai/`. If `JINA_API_KEY` is set, it sends it as a bearer token; otherwise it uses public unauthenticated access.

For a one-off fetch without the script:

```bash
curl "https://r.jina.ai/https://example.com/page"
```

## Workflow

1. Try ordinary browsing, web search, or direct fetch first when those tools are already suitable.
2. Use `scripts/read_url.py` when the page is public but normal tools return a blank page, script shell, paywall/login-like wrapper, poor snippets, blocked parsing, or incomplete text.
3. Also prefer the script for X/Twitter, long URLs, URLs containing `#`, or repeated use.
4. Summarize or extract only the relevant content requested by the user.
5. Mention uncertainty when Reader returns sparse output, a login wall, deleted content, rate-limit text, or an obviously incomplete page.
6. Do not treat Jina Reader as authorization bypass. It can only reliably read content that is publicly accessible to Jina.

## X/Twitter Notes

- Use the canonical post URL when possible: `https://x.com/<handle>/status/<id>`.
- `twitter.com` URLs are acceptable; the script leaves the original URL intact.
- Reader may fail on deleted, protected, age-gated, region-blocked, or login-only posts.
- For threads, fetch the thread URL first. If the returned Markdown only includes the first post, ask for or locate the individual post URLs before claiming full thread coverage.

## Output Handling

- Keep direct quotations short and attribute them to the fetched URL.
- For news, legal, financial, medical, or other high-stakes/current claims, corroborate with additional reliable sources before presenting conclusions.
- If the task is to archive or preserve a post, save the Markdown to a user-facing file only when the user asks.

## Script

`scripts/read_url.py` accepts:

```bash
python3 scripts/read_url.py URL [--output path] [--timeout seconds] [--header "Name: value"]
```

Use `--output` when the fetched Markdown is large or the user asked for a saved artifact.

## Final Report

Include:

- URL fetched
- whether Jina Reader returned complete-looking Markdown or partial/blocked content
- summary, extracted facts, or saved output requested by the user
- corroboration used for current or high-stakes claims
