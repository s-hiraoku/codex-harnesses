# Before / after examples

Calibration set for `SKILL.md` — read once per session when the skill activates. Each pair shows the cut line: what goes, what must survive. Every "after" uses only facts already present in its "before." If the source is vague, keep the uncertainty or flag the missing evidence; never invent specifics to make prose denser.

## 1. Investigation report opening

**Before (slop):**
> In this report, I will summarize the results of my investigation into the login timeout issue. This was a very interesting problem that required looking at several different parts of the codebase. After a thorough analysis, I believe the root cause is that `SessionStore.refresh()` re-acquires the DB lock it already holds at `session/store.py:142`, so under load the second acquisition waits out the 30 s timeout. It should also be noted that token expiry was ruled out because the logs show valid tokens at failure time, and the LB health check was ruled out because the failure is identical with the LB bypassed. These are important findings.

**After:**
> The login timeout is caused by `SessionStore.refresh()` re-acquiring the DB lock it already holds (`session/store.py:142`); under load the second acquisition waits out the 30 s timeout. Two other suspects were ruled out: token expiry (logs show valid tokens at failure time) and the LB health check (fails identically with LB bypassed).

Why: the before buries the cause and eliminated alternatives under announcement, hedging, and self-praise. The after preserves every finding and makes the causal chain direct.

## 2. PR description

**Before (slop):**
> This PR makes some improvements to the validation logic. Several issues were found and fixed: empty-string emails passed `validateEmail` at `validators.ts:18`, phone numbers over 15 digits were silently truncated at line 34, and `null` addresses threw instead of returning a field error at line 51. The code now handles these edge cases appropriately and is more robust. A regression test was added for each fix, and `pnpm test validators` passes all 41 tests. Please review when you have a chance!

**After:**
> Fixes three validation gaps: empty-string emails passed `validateEmail` (`validators.ts:18`), phone numbers over 15 digits were silently truncated (`:34`), and `null` addresses threw instead of returning a field error (`:51`). Each fix has a regression test; `pnpm test validators` passes (41 tests).

Why: "some improvements", "appropriately", and "more robust" add nothing. The after keeps the three fixes, their locations, and the exact test result while removing the vague wrapper.

## 3. Recommendation with caveat (preservation test)

**Before (slop):**
> Based on my analysis, I would generally recommend migrating to the new API, as it removes the per-request auth round-trip, which we measured at 80–120 ms per call. It could potentially be worth considering that clients on SDK versions below 2.3 cannot parse the new pagination cursor and will therefore need to be pinned or upgraded before cutover, but this should not affect newer clients.

**After:**
> Recommend migrating to the new API: it removes the per-request auth round-trip (measured 80–120 ms per call). One compatibility caveat: clients on SDK < 2.3 cannot parse the new pagination cursor and will need pinning or upgrading before the cutover.

Why: the hedge-stack hid a real caveat. Deleting it would be omission; the after keeps the affected SDK versions, failure mode, and required mitigation.

## 4. Structure over substance

**Before (slop):**
> ## Summary
> - The function was refactored
>
> ## Details
> - **What changed**: The 120-line `processData` function, which had cyclomatic complexity 14, was split into `parse`, `validate`, and `persist`
> - **Why**: The function was hard to read
> - **Impact**: Behavior is unchanged, the existing 12 tests still pass, and the code is now easier to read
>
> ## Conclusion
> In conclusion, this refactoring improves the readability of the code.

**After:**
> To improve readability, split `processData` (was 120 lines, cyclomatic complexity 14) into `parse`, `validate`, and `persist`; behavior unchanged, covered by the existing 12 tests.

Why: four headings, three bullets, and a conclusion obscure facts that fit in one sentence. The after preserves the rationale, size, complexity, split, behavior, and test coverage without the scaffold.
