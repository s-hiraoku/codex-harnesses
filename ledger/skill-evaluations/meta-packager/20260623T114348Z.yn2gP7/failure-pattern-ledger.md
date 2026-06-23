# Failure pattern ledger

- **Unapproved asset creation**
  - Example: A packaging workflow emits a shortlist, then immediately creates a new skill because the candidate is high confidence.
  - General Fix Rule: Put explicit user approval before any file edits unless the current request already approves a named candidate.
  - Seen in: iteration 0 structural review
- **Package type collapse**
  - Example: Deterministic lifecycle enforcement is described as automation even though the repository treats hooks as separate reusable assets.
  - General Fix Rule: Keep skill, custom subagent, hook, and automation as separate package choices with clear boundaries.
  - Seen in: iteration 0 structural review
- **Raw private evidence leakage**
  - Example: Final reports quote session excerpts while justifying repeated patterns.
  - General Fix Rule: Report source categories, counts, and paraphrased patterns; do not quote secrets, personal content, or long session text.
  - Seen in: iteration 0 structural review
