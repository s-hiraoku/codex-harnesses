# Philosophy

LLMs are probabilistic. Harnesses should make important parts deterministic.

Codex can reason, inspect, edit, and verify, but long-running development needs more than reasoning. It needs durable guidance, stable workflows, explicit memory, safety boundaries, and repeatable checks.

Harnesses reduce the amount of important behavior that depends on the model remembering instructions from chat history. They turn common expectations into files that can be reviewed, versioned, reused, and executed.

Good harnesses are:

- small enough to be read
- specific enough to guide behavior
- deterministic where safety or verification matters
- easy to adapt per repository
- explicit about their limits

The goal is not to remove judgment. The goal is to reserve judgment for the work that needs it, while scripts, policies, and ledgers handle the parts that should not drift.

