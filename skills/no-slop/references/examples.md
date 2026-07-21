# Before / after examples

Calibration set for `SKILL.md` — read once per session when the skill activates. Each pair shows the cut line: what goes, what must survive. Note in every example: the "after" is *shorter and carries more*, and no fact/caveat from the "before" is missing.

## 1. Investigation report opening

**Before (slop):**
> In this report, I will summarize the results of my investigation into the login timeout issue. This was a very interesting problem that required looking at several different parts of the codebase. After a thorough analysis, I was able to identify what I believe could potentially be the root cause of the issue. It should be noted that this is an important finding.

**After:**
> The login timeout is caused by `SessionStore.refresh()` re-acquiring the DB lock it already holds (`session/store.py:142`); under load the second acquisition waits out the 30 s timeout. Two other suspects were ruled out: token expiry (logs show valid tokens at failure time) and the LB health check (fails identically with LB bypassed).

Why: the before announces, hedges, and self-praises without one fact. The after carries the cause, the location, the mechanism, and the eliminated alternatives — which the before never got to.

## 2. PR description

**Before (slop):**
> This PR makes some improvements to the validation logic. Several issues were found and fixed. The code now handles edge cases appropriately and is more robust. Tests have been updated accordingly. Please review when you have a chance!

**After:**
> Fixes three validation gaps: empty-string emails passed `validateEmail` (`validators.ts:18`), phone numbers over 15 digits were silently truncated (`:34`), and `null` addresses threw instead of returning a field error (`:51`). Each fix has a regression test; `pnpm test validators` passes (41 tests).

Why: "some improvements", "several issues", "appropriately", "more robust" are unverifiable. The after names all three fixes with locations — same length, all content.

## 3. Recommendation with caveat (preservation test)

**Before (slop):**
> Based on my analysis, I would generally recommend migrating to the new API, as it is basically a more modern and powerful solution. It could potentially be worth considering that there may be some compatibility concerns with older clients in certain edge cases, but in most cases this should not be a major issue.

**After:**
> Recommend migrating to the new API: it removes the per-request auth round-trip (measured 80–120 ms per call). One compatibility caveat: clients on SDK < 2.3 cannot parse the new pagination cursor and will need pinning or upgrading before the cutover.

Why: the hedge-stack hid a real caveat. Deleting the whole caveat would be omission — the fix is to sharpen it into a concrete condition (which SDK, what breaks, what to do). This is the compression-vs-omission line.

## 4. Structure over substance

**Before (slop):**
> ## Summary
> - The function was refactored
>
> ## Details
> - **What changed**: The `processData` function was refactored to improve readability
> - **Why**: The function was hard to read
> - **Impact**: The code is now easier to read
>
> ## Conclusion
> In conclusion, this refactoring improves the readability of the code.

**After:**
> Split `processData` (was 120 lines, cyclomatic complexity 14) into `parse`, `validate`, and `persist`; behavior unchanged, covered by the existing 12 tests.

Why: four headings, three bullets, and a conclusion carried one sentence of content — and still omitted the substance (what the split actually was). One dense sentence beats the scaffold.
