# Briefing output format (canonical)

Referenced from step 5 of `SKILL.md`. This defines the content and section order for both outputs: the HTML briefing (rendered via `briefing-template.html`, whose sections mirror this template one-to-one) and the terminal fallback. Keep the section order and headings stable — a reviewer's tool earns its value by putting the same information in the same place every time.

**This format exists to lower the reviewer's cognitive load.** An earlier layout listed every section (reading order, lens guide, machine-checked, judgment, verify, findings, drafts) at equal weight, which forced the human to triage the briefing before they could triage the PR. This format inverts that: it leads with a **conclusion**, gives the **basis** for trusting it, then the **points** the human must actually decide, and folds the supporting detail (design trade-offs, what-was-verified) into collapsed sections. The reviewer reads top-to-bottom and stops as soon as they have what they need — conclusion, then what to fix/decide, then how to look, with everything else one click away. Do not reorder to a findings-first or all-sections-equal layout; that reintroduces the load this format removes.

Mapping to the older lens vocabulary, so nothing is lost:

| This format | Absorbs |
|---|---|
| **Verdict** | TL;DR (purpose / size / CI / risk feel / time) |
| **Basis** | ✅ Machine-checked — safe to skim (the trust signal, in prose) |
| **Points** | ⚠️ Needs human judgment + ❓ Verify (low-confidence) + 🔴 Findings (high-confidence) — one list, ordered by importance, each tagged by a badge |
| **Trade-offs (collapsed)** | 🧭 Design map + the deliberate design choices that are neither bugs nor blockers + per-spot lenses that belong to no point |
| **Points / Basis** | 🧭 Per-spot lens (as each point's how-to-look line) + spec cross-check (met criteria → basis lines; unmet/ambiguous → `check` points) |
| **What was verified (collapsed)** | The ✅ "perspectives applied vs. not verified" discipline + existing-review dedup note |

## Template

```markdown
# PR #<number> — <verdict headline> (<repo>)
<eyebrow: PR link · repo · N files +A/−D · CI status>

## <Verdict>  ← ok / caution / block
<headline: the one-line conclusion>
<body: what the conclusion rests on, 2–4 lines>
<caveat: the one thing that is true despite the verdict — e.g. "code is fine, but does it meet the goal?">

## Basis — why you can trust the verdict
- ✓ <what holds> — <how it was confirmed, in prose (spec met, nothing breaks, bot fixes are real, …)>
- (repeat per basis line; keep to ~3)

## <Points to decide>  ← ordered by importance
badges (once for the section): blocker = 🔴 high-confidence finding · check = ❓ verify / low-confidence · design = ⚠️ design judgment
- [badge] <headline> (`<path>` / <location>)
  <body: what was chosen / found and why it matters>
  ask: <the decision the human must make — intent? oversight? acceptable?>
  draft: <paste-ready comment, only for points that warrant one>
  <repeat this point block, in importance order, for each point>

## ▸ Trade-offs (collapsed) — what the author chose, and against what
<intro: these are choices, not right/wrong; independent of correctness>
### <trade-off heading>
- <what was chosen and what it was traded against — no evaluation>

## ▸ What this review checked (collapsed)
- Perspectives applied: <list — generic set + any project perspective file sections>
- **Not verified**: <what was NOT checked — runtime behavior, load/perf, untouched areas>. "Not verified" ≠ "no findings".
- Existing review threads: <resolved count / how they were deduped into the basis>
```

## Section guidance

### Verdict (the conclusion, up front)
- Pick the block colour by outcome: **ok** (merge-able / nothing broken), **caution** (confirm-first / conditional), **block** (a real blocker exists). The `class` on `.verdict` and the headline must agree.
- Fold the old TL;DR facts into the eyebrow line (size / CI) and the body (purpose / risk feel). Do not add a separate chips row.
- The **caveat** is the highest-value sentence: state the thing that is true *despite* the verdict (most often "the code is correct, but whether it achieves the goal needs judgment"). Skip it only when there genuinely is none.

### Basis (why the verdict is trustworthy)
- This is the ✅ machine-checked layer in prose. **Distinguish "no findings" from "verified"**: a property no perspective covered is not a basis line.
- Keep it to roughly three lines. Each line names *what holds* and *how it was confirmed* — including, when relevant, that existing bot fixes were re-verified as real rather than taken on trust.

### Points (what the human must decide)
- One merged, importance-ordered list replacing the separate ⚠️/❓/🔴 sections. The **badge** carries the old distinction: `blocker` (high-confidence finding), `check` (low-confidence / verify), `design` (judgment call).
- For each point: state *what was chosen or found*, then a one-line **ask** — the decision the human owns (intended scope-cut? oversight? acceptable trade?). Do not evaluate the choice yourself.
- Attach a **draft** comment only to points where a paste-ready comment helps; default to intent-seeking phrasing ("what was the intent behind …"), assert only high-confidence findings.
- If there are genuinely no points to decide, say so in one line rather than deleting the section — an empty points list is itself a time saver.

### Trade-offs (collapsed)
- The 🧭 design map plus the deliberate choices that are *neither bugs nor blockers*. No evaluations: state *what was chosen* and *what it trades against*.
- Collapsed because it is reference material — the reviewer opens it only if a point sends them there.

### What this review checked (collapsed)
- Always list the perspectives applied, every time, and always state what was **not** verified (runtime behavior, load/perf, untouched areas). "Not verified" ≠ "no findings".
- Note how existing review threads were resolved and deduped, so the reviewer doesn't re-litigate comments already folded into the basis.

### Footer
- End by noting nothing was posted to GitHub and that **whether and how to post the comment drafts is the human's call**.
