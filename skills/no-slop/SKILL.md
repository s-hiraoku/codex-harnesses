---
name: no-slop
description: Strip AI slop from prose output and raise its information density — filler openings/closings, restated questions, contentless emphasis, stacked hedges, repeated points, structure that outweighs substance — while preserving every fact, number, caveat, and reason (compression, never omission). This is a MODIFIER skill; it changes how output is written, not what work is done. Invoke it alongside any other skill or task ("write the report, no-slop", "PR 本文を no-slop で"), on its own to rewrite existing text ("deslop this paragraph"), or as a standing session rule ("no-slop for this whole session"). Use whenever the user asks for concise, dense, non-AI-sounding writing, complains that output is verbose/thin/padded, or invokes any writing-heavy task where quality matters. For removing slop from CODE (comments, defensive try/except), use the deslop skill instead — this one is for prose.
---

# no-slop — dense prose, nothing lost

AI prose fails in two directions at once: it is verbose (filler, restatement, decoration) and thin (claims without specifics). This skill fixes both. The output contract: **every sentence carries new information, and no information is lost.**

This is a **modifier**, not a workflow. Once invoked, its rules apply to all user-facing prose you produce for the current task — reports, summaries, PR bodies, README sections, briefings, explanations. It does not change what work you do; it changes how you write the result.

## Invocation modes

| How it was invoked | What to do |
|---|---|
| Alongside another skill or task ("write X, no-slop") | Do the task per its own skill/instructions; apply these rules to every prose deliverable it produces |
| Standalone with existing text ("deslop this") | Rewrite the given text under these rules; show the result (and, if asked, what was cut and why) |
| Standing ("no-slop for this session") | Apply to all subsequent prose until the user turns it off. Re-read this file if you notice drift in long sessions |

## The three rules

### 1. Delete slop (cut without loss)

Cut anything that a reader could delete without losing information. The recognition patterns live in [`references/slop-taxonomy.md`](references/slop-taxonomy.md) — the canonical, growable list. The headline categories:

- Ritual openings and closings ("In this report, I will…", "I hope this helps")
- Restating the question or the task before answering it
- Contentless emphasis ("this is very important" with no *why*)
- Stacked hedges ("it could potentially be possible that")
- Saying the same thing twice in different words; conclusions that re-summarize the body
- Structure that outweighs substance: bullet sprawl, heading-per-sentence, bold/emoji decoration
- Explaining the obvious to the audience at hand

### 2. Densify (thin content is also slop)

Deleting filler is not enough — the remaining sentences must carry weight:

- Every claim gets its ground: a fact, number, path, example, or reason. A claim you cannot ground gets cut or marked as an open question — not padded.
- Replace vague quantities with the actual items ("several issues" → name the three).
- Replace abstract verbs with the concrete action ("handle it properly" → what happens, when).
- Prefer one precise sentence over three approximate ones.

### 3. Preserve (compression is not omission)

**Compression removes redundancy. Omission removes information. Only compression is allowed.** Never cut:

- Facts, numbers, file paths, names
- Caveats, limitations, failure conditions
- Reasons behind judgments and decisions
- Steps the reader must perform

When unsure whether something is redundancy or information, keep it. A dense text that silently dropped a caveat is worse than a verbose one that kept it — the reader can skim verbosity but cannot recover a missing warning.

## Self-verification (must-fire, two passes)

After drafting any deliverable prose, before presenting it:

1. **Density pass** — read each sentence and ask "what new information does this carry?" Cut or merge any sentence with no answer.
2. **Preservation pass** — list the facts, numbers, caveats, and reasons in your pre-cut draft (or source text, in rewrite mode); confirm each one survives in the final text. Anything missing goes back in.

Do not skip pass 2 to save time — over-cutting is this skill's primary failure mode, and it is invisible without the check.

## Calibration

- Dense ≠ terse. Write complete sentences; drop fragments and arrow chains ("A → B → fails") that force the reader to reconstruct your meaning. Readability outranks brevity.
- Match the reader: an expert needs less scaffolding, a newcomer needs more explanation — explanation for a reader who needs it is information, not slop.
- Structure (headings, tables, bullets) is allowed when it carries organization the prose can't; it is slop when it decorates content that one paragraph would state better.
- Worked before/after examples: [`references/examples.md`](references/examples.md). Read them once per session when this skill activates — they calibrate the cut line better than the rules alone.
