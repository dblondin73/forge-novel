# tools/ — forge-specific Workflows (Novel layer)

Book-specific orchestration that isn't portable — it encodes forge-novel's Codex,
voice cast, and editorial passes. The **portable** craft tools (the `prose_lint`
linter, the perplexity spot-checker, the `preflight` gate) moved to the
**Standards layer** in `kit/` (G7, 2026-05-31) — see `kit/README.md` and
`kit/LAYERS.md`.

| File | What it is |
|---|---|
| `chronicler_codex.workflow.js` + `.README.md` | Multi-agent Codex chronicler (G2) — proposes Codex entries/updates from a drafted chapter. forge-mcp-specific. |
| `editors_hat_fanout.workflow.js` + `.README.md` | Editorial fan-out (G1) — runs the `/editors-hat` passes across reviewer agents. Calls the kit linter at `kit/prose_lint/prose_lint.py`. |

Both are Workflow scripts (run via the Workflow tool), not standalone CLIs. Each
has its own `.README.md` in this directory with usage detail.

## Where the portable tools went

| Was | Now |
|---|---|
| `tools/prose_lint*.py` | `kit/prose_lint/` |
| `tools/prose_predictability.py` | `kit/perplexity/` |
| `tools/forge_preflight.py` | `kit/preflight/preflight.py` |
| `tools/prose_lint_config.json` | `prose_lint_config.json` (repo root — Book layer) |

These are bound to forge-novel's files via the repo-root `kit.config.json`.
