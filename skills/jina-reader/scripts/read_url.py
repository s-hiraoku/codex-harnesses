#!/usr/bin/env python3
"""Fetch a public URL through Jina Reader and print Markdown."""

from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("URL is empty")
    if "://" not in url:
        url = "https://" + url
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Unsupported URL: {url}")
    return url


def parse_header(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError("headers must be in 'Name: value' form")
    name, header_value = value.split(":", 1)
    name = name.strip()
    header_value = header_value.strip()
    if not name or not header_value:
        raise argparse.ArgumentTypeError("headers must include a name and value")
    return name, header_value


def build_request(target_url: str, extra_headers: list[tuple[str, str]]) -> urllib.request.Request:
    headers = {
        "User-Agent": "jina-reader-skill/1.0",
    }
    api_key = os.environ.get("JINA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    for name, value in extra_headers:
        headers[name] = value

    # POST handles fragment URLs and very long URLs more reliably than path-prefix GET.
    if "#" in target_url or len(target_url) > 1800:
        body = urllib.parse.urlencode({"url": target_url}).encode("utf-8")
        return urllib.request.Request(
            "https://r.jina.ai/",
            data=body,
            headers=headers,
            method="POST",
        )

    return urllib.request.Request("https://r.jina.ai/" + target_url, headers=headers, method="GET")


def fetch(target_url: str, timeout: float, extra_headers: list[tuple[str, str]]) -> str:
    request = build_request(target_url, extra_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Jina Reader returned HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Jina Reader: {exc.reason}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a public URL through Jina Reader.")
    parser.add_argument("url", help="Public http(s) URL to read")
    parser.add_argument("--output", "-o", help="Write Markdown to this path instead of stdout")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds")
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        type=parse_header,
        help="Additional request header in 'Name: value' form; repeat as needed",
    )
    args = parser.parse_args()

    try:
        target_url = normalize_url(args.url)
        markdown = fetch(target_url, args.timeout, args.header)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as output_file:
            output_file.write(markdown)
        return 0

    print(markdown, end="" if markdown.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
