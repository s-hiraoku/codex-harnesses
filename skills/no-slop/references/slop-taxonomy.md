# Slop taxonomy (canonical, growable)

Recognition patterns for prose slop, referenced from `SKILL.md` rule 1. Each entry: the pattern, why it is slop, and the fix. Add new patterns here as they are noticed — the skill body does not need to change.

## A. Ritual framing

| Pattern | Why it is slop | Fix |
|---|---|---|
| "In this report/section, I will explain…" | Announces content instead of delivering it | Delete; start with the content |
| "I hope this helps / Let me know if…" | Social filler carrying no task information | Delete |
| "Great question!" / "That's an interesting point" | Flattery, no information | Delete |
| Restating the user's question before answering | The reader asked it; they know it | Delete; answer directly |
| "As mentioned earlier…" followed by the full repeat | Repetition disguised as reference | Reference without repeating, or delete |

## B. Contentless emphasis and hedging

| Pattern | Why it is slop | Fix |
|---|---|---|
| "This is very important / crucial / critical" with no reason | Emphasis without grounds is noise | State *why* it matters, or delete the emphasis |
| "It could potentially be possible that…" | Stacked hedges; one hedge suffices | One hedge, or a confidence statement with grounds |
| "generally / basically / essentially / in most cases" as reflex | Softens claims without adding conditions | Delete, or state the actual condition |
| "It should be noted that X" | X alone says the same | Write X |

## C. Redundancy

| Pattern | Why it is slop | Fix |
|---|---|---|
| Same point in different words across adjacent sentences | Padding | Keep the sharper sentence |
| A conclusion section that re-summarizes the body | The body just said it | Conclusion states only what is *new*: the decision, the next step. Otherwise delete |
| Both a table and prose saying identical things | Duplication | One carrier per fact; prose adds only what the table cannot hold |
| Defining a term the audience obviously knows | Audience mismatch | Delete for expert readers; keep for newcomers (that is information) |

## D. Structure over substance

| Pattern | Why it is slop | Fix |
|---|---|---|
| Bullet lists of full sentences that flow as a paragraph | Bullets imply enumerable items; these aren't | Merge into prose |
| A heading per two lines | Navigation for content that has none | Collapse sections |
| Bold/emoji sprinkled for energy rather than signal | Decoration | Reserve bold for the few load-bearing terms |
| Numbered steps for things that are not sequential | False structure | Prose or plain bullets |

## E. Thinness (the other half of slop)

| Pattern | Why it is slop | Fix |
|---|---|---|
| "several issues were found" | Unverifiable vagueness | Name and count them |
| "handle errors appropriately" | Abstract verb hides the actual behavior | Say what happens and when |
| "significant improvement" | No baseline, no number | Give the number or the observable change |
| A recommendation with no reason | Reader cannot evaluate it | Attach the reason or drop the recommendation |
| "X is a powerful/robust/flexible tool" | Marketing adjectives | State the capability that matters here |

## Non-slop look-alikes (do NOT cut)

- A caveat that repeats across sections *because each section is read independently* (e.g. safety warnings in runbooks)
- Explanation sized for a newcomer audience
- A hedge that encodes real uncertainty ("unverified — the diff does not show the caller")
- Transitional sentences that carry logical connection ("this fails only because of the earlier cast" is content, not filler)
- Examples: an example is information when the rule alone is ambiguous
