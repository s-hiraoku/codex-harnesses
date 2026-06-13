# Cost Ceiling Guard Hook

Example hook that counts tool invocations in a rolling 24-hour window and blocks once a configurable ceiling is exceeded.

Environment variables:

- `CODEX_HARNESSES_COST_CEILING`: maximum calls per 24 hours, default `5000`
- `CODEX_HARNESSES_COST_PATH`: override ledger path, default `~/.codex-harnesses/cost-ledger.json`

## Usage

```sh
CODEX_HARNESSES_COST_CEILING=10 python3 hooks/cost-ceiling-guard/hook.py
```

Use this only as a coarse runaway-loop guard. It is not a billing system.
