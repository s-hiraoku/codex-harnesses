---
name: review-briefing
description: Prepare a human reviewer to review a pull request in the least time with the best judgment. Given a PR number or URL, produce an HTML briefing opened in the browser (terminal fallback available) with a reading-order guide, the areas AI has already machine-checked (safe to skim), the design decisions and trade-offs that genuinely need human judgment, low-confidence findings to verify, and ready-to-paste comment drafts. Strictly read-only — never posts to GitHub. Use when the user says things like "help me review this PR", "prep PR 123 for review", "where should I start reading this diff", "review briefing", or whenever the user has been assigned as a reviewer on someone else's PR. For fully automated review (AI produces the findings and finishes), use a code-review skill instead — this skill assumes the human stays in the loop.
argument-hint: "PR number or URL (e.g. 4228)"
---

# review-briefing — a copilot for the human reviewer

Put the human reviewer in the best position to review quickly and well. The skill does not replace review; it splits the work the way it should be split: perspectives that have been verbalized get applied by AI with mechanical consistency, and the human spends their limited attention on judgment — design choices, trade-offs, and product intent that no checklist covers.

## When to use / not use

| Goal | Use |
|---|---|
| **Prepare a human to review someone else's PR** | **this skill** |
| Have AI produce a complete review by itself | a code-review skill (e.g. `review`) |
| Respond to review comments you received | your PR-feedback skill |

## Principles (must-fire)

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

Then the main agent builds a **spec cross-check table** from the step-1 acceptance criteria and the step-3 spec findings: acceptance criterion ↔ implementing location (`file:line`), plus **spec interpretations that are ambiguous and need human confirmation** (include the spec perspective's low-confidence items). Item 2 tells the human *where* to look; item 3 and the cross-check table tell them *how*.

### 5. Output the briefing (HTML in the browser + terminal summary)

Compose the briefing content per [`references/briefing-format.md`](references/briefing-format.md) — its section order and rules are canonical. Then:

1. **Render it as HTML** using [`references/briefing-template.html`](references/briefing-template.html): copy the template, replace every `{{PLACEHOLDER}}`, duplicate list items as needed, and follow the template's comments (risk/CI chip classes, deleting the 🔴 section when empty). Do not add external resources — the file must stay self-contained. **HTML-escape every value that originates from the PR or the repo before inserting it** — PR title, body, branch/author names, issue text, file paths, finding text, and comment drafts can all contain `<`, `>`, `&`, or `"`; a malicious PR could otherwise inject markup/script into the local file (local XSS when you open it). Escape those four characters (`&`→`&amp;` first, then `<`→`&lt;`, `>`→`&gt;`, `"`→`&quot;`) in the text you substitute; the template's own literal markup is already safe.
2. **Write it to a local file outside the repo working tree** (never commit it): `"${TMPDIR:-/tmp}/review-briefing-pr<N>.html"`.
3. **Open it in the browser**: `open <file>` on macOS, `xdg-open <file>` on Linux.
4. **Print a terminal summary**: the TL;DR block, any 🔴 high-confidence findings, and the HTML file path.

If no browser can be opened (headless/SSH session) or the user asks for terminal output, print the full markdown briefing to the terminal instead — same sections, same order.

Skeleton (both outputs):

1. **TL;DR** — purpose / size / CI status / overall risk feel / estimated review time
2. **Reading-order guide** — essential changes first; quarantine mechanical changes (renames, generated files) as "skimmable"
3. **🧭 Review-lens guide** — the step-4 artifacts: design map / per-spot review lens (how to read each spot) / spec cross-check table (acceptance criteria ↔ implementing locations, ambiguous interpretations to confirm)
4. **✅ Machine-checked — safe to skim** — perspectives that came back clean at high confidence. **Always list which perspectives were applied** (what wasn't checked isn't verified)
5. **⚠️ Needs human judgment** — the step-4 map. This is where the reviewer should spend time
6. **❓ Verify — low-confidence findings** — the human decides true/false
7. **🔴 Findings (high confidence) — ...** — if any, by severity
8. **Comment drafts** — paste-ready, explicitly marked as **not posted**

## After the review (must-fire, once)

When the user signals they finished reviewing ("done", "approved", "left comments"), ask **once**:

> Did you catch anything the machine-check layer missed? If so, it's worth verbalizing it into your project's accumulated review perspectives — next time it lands in the ✅ section instead of costing you time.

This closes the loop the skill is built on: the human's new job is discovering and verbalizing the next perspective. Offer once; don't push.

## Prerequisites

- `gh` CLI authenticated with read access to the target PR
- A subagent mechanism for the parallel reviewers. Without one, run the perspectives selected in step 3 sequentially in the main agent with the same clean-brief and confidence contract (slower, still valid)
