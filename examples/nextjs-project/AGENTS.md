# Next.js Project Guidance

Follow existing routing, rendering, data-fetching, styling, and component patterns.

## Expectations

- Preserve server/client component boundaries.
- Keep route handlers, server actions, and API calls explicit about authorization and validation.
- Avoid broad rewrites of routing, layout, or shared state.
- Update docs or examples when user-facing behavior, environment variables, or commands change.
- Treat generated UI as unfinished until it has been checked in a browser.

## Verification

Before finalizing meaningful changes:

- run `bash scripts/verify.sh`
- check changed routes in a browser when UI behavior changed
- summarize verification, browser coverage, and remaining risks

## Safety

- Do not print `.env` files or secrets.
- Do not change production deployment settings without explicit review.
- Do not force push or hard reset without explicit approval.

