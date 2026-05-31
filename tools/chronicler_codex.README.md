# chronicler-codex — G2 Chronicler → Codex auto-population (Workflow)

After David **approves** a chapter, this Workflow mines it for new canon and for
Nate's mechanical progression, then emits **proposals** for David to confirm. It
**never writes canon, the ledgers, or the schedule** — it returns a report.

- **P13 (Chronicler):** new/updated Codex **entities** (characters, creatures,
  items, locations, factions, mechanics, abilities), **relationships** (bonds,
  alliances, conflicts, loyalty shifts — the Codex is a relationship graph), and
  **timeline** events (world-state changes in story order).
- **P20 (Progression ledger):** Nate's (and companions') skills, abilities,
  ranks, stat reveals, class/loadout changes → a `progression-state.json` delta.
- **P29 (validate-before-add):** dedup candidates against the Codex; flag
  mechanical / epistemic / reveal / continuity / relationship / timeline drift.

Design rationale and the increment roadmap: `research/g2-chronicler-codex-plan.md`.

## Run it

The Workflow needs the harness **"workflow" opt-in** (it spawns 6 subagents:
4 extractors + validate + synthesis).

```jsonc
Workflow({
  scriptPath: 'tools/chronicler_codex.workflow.js',
  args: { chapter: 'ch03', file: 'drafts/ch03-first-boot-draft01.md' }
})
```

`args.file` is optional — given only `chapter`, the first agent globs
`drafts/chNN-*-draft01.md`. Output is a structured report object; save it under
`reports/chNN-chronicler-<date>.md`.

## What it reads (all local)

| Source | Role |
|---|---|
| the approved draft | the text to mine |
| `REFERENCE.md` | Codex proxy — dedup target |
| `research/skill-system-design.md` | progression ground truth — mechanical-drift check |
| `epistemic-states.json` | what the POV character knows when — epistemic-drift check |
| `revelation-schedule.json` | scheduled reveals — reveal-timing check |
| `progression-state.json` | the running progression ledger (created on first confirmed run) |
| `timeline-state.json` | the running world-event ledger (created on first confirmed run) |

## Phases

`Extract` (parallel: **entities + relationships + timeline + progression**) →
**barrier** → `Validate` (dedup + drift) → `Synthesis` (proposal report). The
barrier is deliberate: the validator needs **all** candidates at once to resolve
aliases, collapse symmetric relationship edges, and dedup against each other and
canon.

Model routing: the four extractors on Sonnet; validate + synthesis on Opus
(dedup and drift detection are the correctness-critical steps).

## The forge-MCP caveat (read this)

The authoritative 153-entity Codex lives **only in forge-mcp**. This MVP dedups
against `REFERENCE.md` — a **prose rebuild** of the Codex (last rebuilt
2026-04-09), not a structured mirror. So:

- Dedup is **best-effort** and may lag the live Codex. Each proposal's
  `dedup_note` flags how it was matched and the residual staleness risk.
- **Sanity-check create-vs-update against the live Codex** before applying.
- When `forge_codex` tools are session-live, the planned increment swaps the
  proxy for a live Codex read (exact dedup, real Codex numbers).

## Applying the proposals (manual, gated on David's OK)

1. **Codex entities:** `proposed_codex_calls[]` maps 1:1 to `forge_codex`
   create/update calls — run them when the forge tools are available in-session.
2. **Relationships:** `proposed_relationship_edges[]` are the new/changed Codex
   graph edges (pure "confirm" edges are omitted — they need no write).
3. **Ledgers:** `progression_state_json` merges into `progression-state.json`;
   `timeline_state_json` merges into `timeline-state.json` (both files created on
   the first confirmed run).
4. **Drift flags** are for David to adjudicate — some are real canon bugs, some
   are deliberate (a withheld reveal the Codex already knows in full).

Nothing applies automatically. The Workflow proposes; David confirms; apply is a
separate, explicit step.
