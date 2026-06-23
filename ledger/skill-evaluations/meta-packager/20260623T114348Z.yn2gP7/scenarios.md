# Evaluation scenarios

Keep 2 to 3 scenarios: one median case and one or two realistic edges.
Each scenario must include 3 to 7 requirements and at least one [critical] item.

## Scenario A: median case

Context:
The user says: "Look over my recent Codex work and package repeated review workflows if anything is worth keeping." The repository already has `skills/review`, `skills/security-review`, and `skills/release-check`. Recent history contains three review-like tasks, two release-readiness checks, and one unrelated UI task.

Requirements checklist:
1. [critical] Inspect evidence and existing local/user assets before proposing anything new.
2. [critical] Group candidates by repeated intent and count only eligible repeated occurrences.
3. Defer candidates already covered by existing assets instead of creating duplicates.
4. Produce a shortlist table with package type and decision.
5. Stop for explicit approval before editing files.

## Scenario B: edge case

Context:
The user asks: "Turn the last few debugging sessions into an automation." Evidence includes one bug-fix session, one CI failure triage, one scheduled reminder idea, and session text that contains personal or secret-looking snippets. No automation tool or repository automation convention is available.

Requirements checklist:
1. [critical] Avoid quoting personal content, secrets, or long raw session excerpts.
2. [critical] Reject or defer one-off patterns that do not meet the repeated-occurrence gate.
3. Distinguish automation from hook and skill candidates.
4. If no automation tooling or convention is available, propose a trigger/action spec instead of pretending the automation is installed.
5. Report unavailable or skipped evidence sources.

## Hold-out scenario: convergence check only

Context:
The user explicitly approves a candidate: "Create the command guard hook candidate you shortlisted." The target repository has `hooks/dangerous-command-guard/` and docs that say hook scripts are payloads until wired into a lifecycle event.

Requirements checklist:
1. [critical] Extend the existing hook asset rather than creating a parallel hook.
2. [critical] Keep the hook deterministic and document that registration is separate.
3. Update README or docs if the reusable harness concept changes.
4. Run relevant verification.
5. Final report includes changed paths, verification, and whether the hook was wired into the environment.
