# Briefing output format (canonical)

Referenced from step 5 of `SKILL.md`. This defines the content and section order for both outputs: the HTML briefing (rendered via `briefing-template.html`, whose sections mirror this template one-to-one) and the terminal fallback. Keep the section order and headings stable — a reviewer's tool earns its value by putting the same information in the same place every time. Delete sections that don't apply entirely (don't write "none") — **except** ✅ and ⚠️, which are the core of this skill: keep them even when empty, stating explicitly that nothing applies.

## Template

```markdown
# Review Briefing: PR #<number> <title>

## TL;DR
- **Purpose**: <1–2 lines; include the linked issue's gist if any>
- **Size**: <N> files, +<A>/-<D> | **CI**: <passing / failing (what) / pending>
- **Risk feel**: low / medium / high — <one-line reason>
- **Estimated review time**: <X min> (<Y> spots in the ⚠️ section)

## Reading order
1. `<path>` — <why first: the essential change>
2. `<path>` — <consumer / ripple of 1>
3. (skimmable: <mechanical changes, e.g. rename fallout across 12 files>)

## 🧭 Review-lens guide — how to look

### Design map
<responsibilities and dependency direction of the added/changed modules, and the data flow, in 5 lines or fewer — the map to load before reading the diff>

### Per-spot lens
- `<path>` — <how to read it, e.g. re-render impact / authorization boundary / error paths / consistency with the existing X pattern>

### Spec cross-check
- Criterion <n> "<summary>" ↔ `<path>:<line>` — <how to confirm>
- **Ambiguous interpretation to confirm**: `<path>:<line>` <the interpretation the code took> — <what part of the spec is ambiguous; what to check it against (issue comments / design file / spec doc)>

## ✅ Machine-checked — safe to skim
- [spec] <what was verified and the result>
- [risk] <e.g. types, null-safety, a11y floor: no findings>
- [completeness] <only if the perspective ran>
- Perspectives applied: <list them — generic set + any project perspective file sections>

## ⚠️ Needs human judgment — spend your time here
- `<path>:<line>` <what was chosen> — <what it trades against / what to confirm>

## ❓ Verify — low-confidence findings
- [<perspective>/low] `<path>:<line>` <finding> (<why confidence is low>)

## 🔴 Findings (high confidence) — <delete section if none>
- [<severity>][<perspective>] `<path>:<line>` <finding>

## Comment drafts (paste-ready — nothing has been posted)
> `<path>:<line>` <draft. Default to asking intent rather than asserting>
```

## Section guidance

### TL;DR
- "Risk feel" is not just the finding count — weigh the nature of the change (data-model changes, authz, wide ripple).
- Estimated review time is a rough function of ⚠️ spots and size (round to 5 minutes). Its purpose is to seed the human's time budgeting.

### Reading order
- "Essential" is decided by **dependency direction**, not line count (new types/abstractions → their consumers → tests).
- Always quarantine mechanical changes (rename fallout, import shuffles, generated artifacts) as skimmable. Keeping the human from close-reading these is the single biggest time saver.

### 🧭 Review-lens guide
- The **design map** describes *responsibilities and dependency direction*, not file locations — "new type → who consumes it → where it renders" should be graspable in one read.
- Keep the **per-spot lens** to one lens per spot. If you want to list three or more lenses for a file, it belongs in ⚠️ instead — it has outgrown lens-guided reading and needs judgment.
- The **spec cross-check** maps *every* acceptance criterion to its implementing location. A criterion with no matching location is itself important information — escalate it to 🔴 or ❓. For ambiguous interpretations, state the interpretation the code took as a fact and always name what to check it against (issue comments / design file / spec doc).

### ✅ Machine-checked
- **Distinguish "no findings" from "verified"**: list the perspectives applied, every time. A property that no perspective covers (e.g. load behavior) is *not* verified and must not appear here.
- Low-confidence "clean" results don't belong here (nor in ❓ — simply omit them).

### ⚠️ Needs human judgment
- No evaluations. State *what was chosen*, *what it trades against*, and the question to ask — the judgment itself belongs to the human.
- If empty, say "none — mechanical change only": knowing the section is empty is itself a time saver.

### Comment drafts
- Default to intent-seeking phrasing ("what was the intent behind …"); assert only high-confidence findings.
- Make them paste-ready, and end the briefing by noting that **whether and how to post them is the human's call**.
