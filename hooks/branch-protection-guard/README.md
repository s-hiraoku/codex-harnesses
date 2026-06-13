# Branch Protection Guard Hook

Example hook that scans stdin and blocks direct `git push` to protected branches. It also blocks `git commit` when the current branch is protected or cannot be determined.

Protected branches are `main`, `master`, `production`, and `release`.

Set `CODEX_HARNESSES_ALLOW_PROTECTED_BRANCH=1` to bypass the example guard for one session after an intentional human decision.

## Usage

```sh
printf '%s\n' "git push origin main" | python3 hooks/branch-protection-guard/hook.py
```

This is a conservative example. Adapt branch names, bypass policy, and lifecycle registration before relying on it.
