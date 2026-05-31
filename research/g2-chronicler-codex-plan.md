# G2 — Chronicler → Codex Auto-Population: Build Plan

> **Tier-1 graft (P13 + P20 + P29).** After David approves a chapter, a Workflow
> mines it for new canon (entities, relationships, timeline) and for Nate's
> mechanical progression (skills, abilities, ranks, stat reveals), diffs both
> against existing canon, and emits **proposed** Forge MCP Codex updates + a
> `progression-state.json` delta for David to confirm. Source:
> `skill-mining-fantasy-writing.md` grafts G2/P13/P20/P29.

---

## What this is — and isn't

- **Proposes, never writes.** G2 never mutates canon. It emits a proposal
  report: candidate `forge_codex` create/update calls + a `progression-state.json`
  delta. David confirms; an apply step (manual now, scriptable later) executes.
  This is the same catalog-then-approve contract as G1.
- **Solves a 7-book scaling problem.** Manual Codex upkeep across hundreds of
  chapters drifts. The Chronicler keeps the 153-entity Codex current and keeps a
  ground-truth progression ledger the prose can be checked against (a skill used
  in Ch12 that Nate doesn't unlock until Ch15 gets flagged).
- **Code effort, not craft effort.** Per the two-efforts split, this is
  orchestration/tooling — it touches no editorial rule and writes no prose.

---

## The forge-MCP constraint (and why it does not block the build)

The authoritative Codex (153 entities) lives **only in forge-mcp**; the repo's
`REFERENCE.md` is a *prose rebuild* of it (last rebuilt 2026-04-09), not a
structured mirror. Two facts shape the design:

1. **G2's output is proposals, never live writes** — so the forge *write* path is
   never auto-called regardless of whether forge tools are session-live.
2. The only step that wants live forge is **read-for-dedup** (P29
   validate-before-add). That degrades gracefully: the MVP diffs proposed
   entities against `REFERENCE.md` with an explicit **staleness caveat** (the
   prose proxy may lag the live Codex). When forge tools are session-live, a
   future increment swaps in a live Codex read for exact dedup.

Everything else G2 needs is local: the approved draft, `epistemic-states.json`,
`revelation-schedule.json`, `research/skill-system-design.md`.

---

## Inputs

| Input | Role |
|---|---|
| approved chapter draft (`drafts/chNN-*.md`) | the text to mine |
| `REFERENCE.md` | Codex proxy — dedup target (staleness-caveated) |
| `research/skill-system-design.md` | progression ground truth (Domain→Skill→Ability, Conduit Gifts) — drift check |
| `epistemic-states.json` | what the POV character knows when — epistemic-drift check |
| `revelation-schedule.json` | scheduled reveals — don't propose paying a withheld plant early |
| `progression-state.json` *(created by G2; absent today)* | the running LitRPG ledger to extend |

---

## Target architecture — four Workflow phases

```text
Read ─┬─ Extract (parallel) ──────────────┐
      │   • entities  (Codex candidates)   │  BARRIER (dedup needs all
      │   • progression (Nate's ledger)    │  candidates together)
      └────────────────────────────────────┘
                       │
              Validate / Diff  ── dedup vs REFERENCE.md (P29) +
                       │           drift vs skill-system-design + schedule
                       │
                  Synthesis  ── proposal report:
                                 1. Proposed Codex changes (create/update)
                                 2. progression-state.json delta (JSON block)
                                 3. Drift / continuity flags
                                 4. Copy-ready proposed forge_codex calls
```

**Why a barrier here (not a pipeline):** the dedup/validate step is the textbook
case for a barrier — it needs *all* extracted entities at once to resolve
aliases and cross-check duplicates against each other and against canon. (G1, by
contrast, pipelines because each finding verifies independently.)

---

## MVP scope (this build) vs increments

**MVP — two extractors (the two ★ patterns), proposal-only:**

- **Entities** [P13] — new/updated Codex candidates: characters, creatures,
  items, locations, factions, mechanics. Each tagged NEW vs UPDATE-to-existing
  (with the `REFERENCE.md` Codex # when it can be matched).
- **Progression** [P20] — Nate's (and companions') mechanical changes: skills,
  abilities, ranks, stat reveals, class/loadout developments → the
  `progression-state.json` delta.
- **Validate/diff** — dedup candidates vs `REFERENCE.md` (P29); flag mechanical
  drift vs `skill-system-design.md` and epistemic/reveal drift vs the schedule.
- **Synthesis** — one proposal report + the copy-ready artifacts.

**Increments (after MVP validates), mirroring G1's step rhythm:**

1. ~~**Relationships + timeline extractors** [P13] — bonds/allegiances/conflicts and
   world-state events as their own lenses.~~ **BUILT 2026-05-31** — the Workflow
   now runs four parallel extractors (entities + relationships + timeline +
   progression); validate collapses symmetric edges and adds relationship/timeline
   drift types; synthesis emits relationship-edge proposals + a `timeline-state.json`
   delta alongside the progression ledger.
2. **Live-forge dedup** [P29] — swap the `REFERENCE.md` proxy for a live
   `forge_codex` read when the tools are session-live (exact dedup, real Codex #s).
3. **Epistemic delta proposals** — propose `learned_this_chapter` +
   revelation-status advances (coordinated with `/forge-write`, which owns that
   file today — G2 only *proposes*).
4. **Apply step** — a small confirm-then-write path (forge_codex calls +
   progression-state.json merge) gated on David's explicit OK.
5. **Adjacent-chapter dedup** — *(surfaced by the Ch03 increment run)* dedup
   currently reads `REFERENCE.md` only, so an entity established in an earlier
   chapter's prose but never given a Codex entry reads as "new" (the two Ch03
   runs disagreed on Congressman the steer for exactly this reason). Feed the
   validator the prior chapters' accepted-entity set (or a running entity index)
   so create-vs-confirm accounts for prose canon, not just the Codex proxy.

---

## Contract guarantees

- **Never auto-writes** canon, the ledger, or the schedule. Returns a report.
- **Reuses line cites as evidence** for every proposed change (auditable).
- **Conservative dedup**: when unsure whether a candidate is new or an existing
  entity, propose UPDATE and flag the ambiguity rather than minting a duplicate.
- **Honors withheld reveals**: the Codex holds full author-truth, so adding
  Flint's true nature to the Codex is fine — but G2 must NOT propose advancing a
  reveal's *in-world* status before its scheduled chapter.

---

## Deliverables

| File | Role |
|---|---|
| `tools/chronicler_codex.workflow.js` | the G2 Workflow (MVP) |
| `tools/chronicler_codex.README.md` | usage + the forge-MCP caveat |
| `progression-state.json` | **created on first confirmed run** (not by the Workflow itself) |
| `reports/chNN-chronicler-<date>.md` | per-run proposal report (David's confirm queue) |

## Status

**G2 MVP BUILT + VALIDATED 2026-05-31** (committed `16c09bd`). Entities +
progression extractors, REFERENCE.md dedup, drift flags, proposal synthesis.
Dry-run on Ch03 surfaced 11 Codex actions + 13 progression events + a real major
drift flag (HUD green→blue, Codex lags prose), rejected false mints, held the
Narnia Principle. Report: `reports/ch03-chronicler-2026-05-31.md`.

**Increment #1 BUILT 2026-05-31** (relationships + timeline lenses — now a
6-agent Workflow). Re-run on Ch03 to validate the two new lenses is pending.
Increments #2-4 (live-forge dedup, epistemic deltas, apply step) unstarted —
live-forge dedup and the apply write-half are blocked on forge_codex tools being
session-live.
