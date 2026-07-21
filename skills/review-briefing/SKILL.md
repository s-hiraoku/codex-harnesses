---
name: review-briefing
description: Prepare a human reviewer to review a pull request in the least time with the best judgment. Given a PR number or URL, produce a verdict-first HTML briefing opened in the browser (terminal fallback available): the conclusion up front, the basis for trusting it, an importance-ordered list of points the human must decide (with ready-to-paste comment drafts), and collapsed trade-off / what-was-verified detail. Strictly read-only — never posts to GitHub. Use when the user says things like "help me review this PR", "prep PR 123 for review", "where should I start reading this diff", "review briefing", or whenever the user has been assigned as a reviewer on someone else's PR. For fully automated review (AI produces the findings and finishes), use a code-review skill instead — this skill assumes the human stays in the loop.
argument-hint: "PR number or URL (e.g. 4228)"
---

# review-briefing — a copilot for the human reviewer

Put the human reviewer in the best position to review quickly and well. The skill does not replace review; it splits the work the way it should be split: perspectives that have been verbalized get applied by AI with mechanical consistency, and the human spends their limited attention on judgment — design choices, trade-offs, and product intent that no checklist covers.

**The briefing's job is to lower cognitive load, not add to it.** A briefing that dumps every section at equal weight makes the human do the triage the skill was supposed to do for them. So the output leads with the answer and defers the detail: **conclusion first → what to fix / decide → what to look at and how → supporting detail folded away.** The reviewer should be able to read the top and stop as soon as they have what they need; everything below that is there when they want it, not in their face by default. Every design choice in the output format serves this — the up-front verdict, the short basis, the importance-ordered points, and the collapsed trade-off/verification sections.

## When to use / not use

| Goal | Use |
|---|---|
| **Prepare a human to review someone else's PR** | **this skill** |
| Have AI produce a complete review by itself | a code-review skill (e.g. `review`) |
| Respond to review comments you received | your PR-feedback skill |

## Principles (must-fire)

- **Lead with the conclusion; defer the detail.** The output exists to *reduce* the reviewer's cognitive load. Order it so the answer comes first (verdict), then what they must act on (points to fix/decide), then how to look (lens), with reference material (trade-offs, what-was-verified) collapsed. Never present all sections at equal weight — that hands the triage back to the human. If a section would make the reviewer work harder to find the point, it is in the wrong place or too prominent.
- **Strictly read-only**: never write to GitHub (no comments, reviews, labels). Comment drafts live only in the local briefing (HTML file / terminal). The human's judgment is never pre-empted.
- **Review subagents get a clean brief**: pass only the diff, the acceptance criteria (from the linked issue, if any), and the perspective to check. Do not pass existing review comments into the reviewers — that creates confirmation bias. Deduplication against existing comments happens afterwards, in the main agent.
- **Route reviewers to a stronger model tier or higher reasoning effort** per your runtime's escalation policy (e.g. the routing table used by the `adviser` skill); disclose a downgrade if one occurs. Consistent judgment quality is the point of the machine-check layer.
- **If your project maintains a verbalized perspective file** (accumulated review checklists, "missed-finding" perspectives), pass it to the reviewers as the canonical perspective set instead of inventing one — and never fork a second copy of it.

## Workflow (5 steps)

### 1. Fetch PR context (main agent, `gh`)

```bash
gh pr view <PR> --json number,title,body,url,author,baseRefName,files,additions,deletions,statusCheckRollup
gh pr view <PR> --json comments,reviews          # existing findings (for dedup)
gh api repos/<owner>/<repo>/pulls/<PR>/comments  # inline comments
gh pr diff <PR>
```

Read the linked issue (from `closes …`) for acceptance criteria and background. If CI is failing, say so at the top of the briefing — the human should know before they start reading.

### 2. Background research (parallel read-only subagents, conclusions only)

Collect what the human needs to judge "does this follow the codebase's existing conventions":

- Agent A: existing patterns, similar implementations, naming conventions in the touched area
- Agent B: the specs/conventions that govern the touched feature (project docs, CLAUDE.md / AGENTS.md sections)

**Tier**: skip this step for small PRs (roughly under ~100 changed lines).

### 3. Machine-check layer (parallel review-only subagents)

Spawn independent review-only subagents, one per perspective, each with a clean brief (diff + acceptance criteria + that perspective only — separate lenses catch what a single merged reviewer misses):

- **spec**: does the change satisfy the acceptance criteria / stated intent; does it follow existing patterns
- **risk**: bugs, type mismatches, runtime errors, security, accessibility, performance
- **completeness** (only when the PR adds/changes a user-facing feature): facets the issue never spelled out but the product obviously needs (empty states, error states, loading, i18n, analytics)

Output contract for every reviewer — this drives the briefing's triage:

> Tag every finding with **confidence: high / low** ("provable from the diff and the perspective" = high; "depends on runtime conditions, unclear reproduction, or spec interpretation" = low).

### 4. Judgment-area and review-lens extraction (one subagent, orthogonal to step 3)

This is *not* another bug hunt. Ask a separate read-only subagent for three things:

> 1. **Design map**: the responsibilities and dependency direction of the modules/components this diff adds or changes, and the data flow — in 5 lines or fewer. This is the mental map the reviewer loads before reading the diff.
> 2. **Judgment areas**: list the places where a **design decision, trade-off, or spec interpretation** was made. Do not look for bugs or violations — look for *places where the author chose something*: a new abstraction, a deliberate deviation from an existing pattern, an error-handling behavior, a performance/readability trade, a data-model shape. For each, one line on *what was chosen* and *what it was traded against*. Do NOT evaluate whether the choice is good — that is the human's job.
> 3. **Per-spot review lens**: for each major changed file and judgment area, one line on *how to read it* (e.g. "read for re-render impact", "trace the authorization boundary", "walk the error paths only", "compare against the existing X pattern").

Then the main agent cross-checks the step-1 acceptance criteria against the step-3 spec findings and routes everything into the output sections: **criteria that hold become basis lines** ("spec met — confirmed at `file:line`"), **criteria that are unmet or ambiguously interpreted become points** (badge `check`, with the ambiguity as the *ask*), the **design map goes into the collapsed Trade-offs section**, and each **per-spot lens becomes the how-to-look line inside the point it belongs to** (lenses for spots with no point go into Trade-offs). Nothing from this step gets its own section — it feeds the verdict-first layout.

### 5. Output the briefing (HTML in the browser + terminal summary)

Compose the briefing content per [`references/briefing-format.md`](references/briefing-format.md) — its section order and rules are canonical. Then:

1. **Render it as HTML** using [`references/briefing-template.html`](references/briefing-template.html): copy the template verbatim and replace every `{{PLACEHOLDER}}` — **do not redesign it**. The template is the canonical format; do not invent your own layout, CSS classes, or section structure. Replace **all** placeholders — including the easy-to-miss head ones (`{{LANG}}`, `{{VERDICT_TITLE}}`) and the choice placeholders `{{VERDICT_CLASS}}` (`ok`/`caution`/`block`, must agree with the headline) and `{{BADGE_CLASS}}` (`blocker`/`check`/`design`) — then follow the template's comments: duplicate `<li>`/`.point`/`h4`+`ul` blocks as needed, and drop the `.draft` block on points that have no comment draft. Before writing the file, grep it for `{{` — any leftover placeholder means you are not done. Do not add external resources — the file must stay self-contained. **HTML-escape every value that originates from the PR or the repo before inserting it** — PR title, body, branch/author names, issue text, file paths, finding text, and comment drafts can all contain `<`, `>`, `&`, or `"`; a malicious PR could otherwise inject markup/script into the local file (local XSS when you open it). Escape those four characters (`&`→`&amp;` first, then `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`) in the text you substitute; the template's own literal markup is already safe.
2. **Write it to a local file outside the repo working tree** (never commit it): `"${TMPDIR:-/tmp}/review-briefing-pr<N>.html"`.
3. **Open it in the browser**: `open <file>` on macOS, `xdg-open <file>` on Linux.
4. **Print a terminal summary**: the verdict headline + caveat, any `blocker`-badged points, and the HTML file path.

If no browser can be opened (headless/SSH session) or the user asks for terminal output, print the full markdown briefing to the terminal instead — same sections, same order.

Skeleton (both outputs — mirrors `briefing-template.html` one-to-one):

1. **Verdict** — the one-line conclusion (ok / caution / block), what it rests on, and the caveat that is true despite it (absorbs the old TL;DR: purpose / size / CI / risk feel / time)
2. **Basis** — ~3 prose lines on why the verdict is trustworthy (the ✅ machine-checked layer; **always name the perspectives that back it** — what wasn't checked isn't verified)
3. **Points to decide** — one importance-ordered list of ⚠️ judgment calls, ❓ low-confidence items, and 🔴 high-confidence findings, each with a badge (`design`/`check`/`blocker`); attach a paste-ready **draft** only where one helps
4. **Trade-offs (collapsed)** — the step-4 design map plus the deliberate choices that are neither bugs nor blockers; no evaluations
5. **What this review checked (collapsed)** — perspectives applied vs. explicitly **not verified**, and how existing review threads were deduped into the basis

## After the review (must-fire, once)

When the user signals they finished reviewing ("done", "approved", "left comments"), ask **once**:

> Did you catch anything the machine-check layer missed? If so, it's worth verbalizing it into your project's accumulated review perspectives — next time it lands in the ✅ section instead of costing you time.

This closes the loop the skill is built on: the human's new job is discovering and verbalizing the next perspective. Offer once; don't push.

## Prerequisites

- `gh` CLI authenticated with read access to the target PR
- A subagent mechanism for the parallel reviewers. Without one, run the perspectives selected in step 3 sequentially in the main agent with the same clean-brief and confidence contract (slower, still valid)
