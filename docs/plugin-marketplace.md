# Plugin Marketplace

`codex-harnesses` is packaged as a Codex plugin and exposed through the repository marketplace manifest.

## Layout

- `marketplace.json`: marketplace manifest.
- `plugins/codex-harnesses/.codex-plugin/plugin.json`: plugin manifest.
- `plugins/codex-harnesses/skills/`: reusable Codex workflows.
- `plugins/codex-harnesses/hooks/`: hook payload examples.

The plugin manifest exposes the skills directory to Codex. Hooks, policies, ledgers, examples, and scripts remain harness examples; review and wire them explicitly before relying on them.

## Install From A Local Checkout

Add the repository as a marketplace root:

```sh
codex plugin marketplace add /path/to/codex-harnesses
```

Then install `codex-harnesses` from the Codex plugin marketplace UI.

## Development Notes

Keep `marketplace.json` and `plugins/codex-harnesses/.codex-plugin/plugin.json` in sync when the plugin name, category, or install policy changes.

Run plugin validation after manifest changes:

```sh
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/codex-harnesses
```

Run repository verification before finalizing:

```sh
bash scripts/verify.sh
```
