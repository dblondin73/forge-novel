# G5 — Outline-is-Law Pre-Flight Gate: Build Plan

> **Tier-2 graft (P2 + P3).** Before `/forge-write` generates a single line of
> prose, it derives the minimal context set the requested beats need (P3),
> verifies every required input is actually present (P2 — outline is law), and
> **halts into specific questions** if anything is missing or a stub — instead of
> inventing structure to paper the gap. Source:
> `skill-mining-fantasy-writing.md` grafts G5/P2/P3.

---

## What this is — and isn't

- **A front-end gate, not a craft rule.** G5 touches no voice, prose, or
  theology rule. It hardens the *mechanics* of the Context Loading Protocol — an
  orchestration change, the "script/code" effort kind, never the craft kind.
- **The complement to the existing post-write catch.** `check-proper-nouns.py`
  already flags *unflagged inventions after* a draft is written. G5 is the
  mirror on the front: don't start drafting *into a gap* in the first place.
- **Not a Workflow.** G1/G2 fan out many agents; G5 is a gate inside the *single*
  drafting agent's decision procedure. It is a SKILL.md protocol step plus a
  small deterministic helper — no subagents.
- **Halts, never fills.** When a required input is missing, G5 emits a specific
  question and stops. David answers; G5 never invents the beat, the sheet, or
  the entity itself.

---

## The forge-MCP constraint (and how the gate splits around it)

The chapter **outline/beats live only in forge-mcp** (`forge_outline_beats`),
not in a repo file. So the gate splits into two halves:

1. **Repo-local checks — deterministic, zero-token** (`tools/forge_preflight.py`):
   - prior-chapter epistemic entry present (`after_ch{NN-1}` in
     `epistemic-states.json`);
   - this chapter's scheduled revelations enumerated (any revelation whose
     `plant_chapter` / `hint_chapters` / `full_reveal_chapter` includes NN — the
     gate reminds the agent it MUST advance them);
   - character sheets present in `characters/` for named characters;
   - named entities resolve against `.forge-known-entities.json` (the same cache
     `check-proper-nouns.py` already uses).
2. **Forge-side check — agent-side** (`forge_outline_beats`, or the SSH fallback
   already documented in the skill): the requested beats exist and are unwritten,
   and the beat's linked Codex entities aren't stubs. Degrades gracefully when
   forge isn't session-live — the deterministic half still runs and the agent
   notes the outline check ran in fallback mode.

Everything the deterministic half needs is local and already in the repo.

---

## Inputs

| Input | Role |
|---|---|
| target chapter + optional beat range (`$ARGUMENTS`) | what to pre-flight |
| `forge_outline_beats` (forge / SSH fallback) | beats exist + unwritten — outline-is-law |
| `epistemic-states.json` | prior-chapter `after_ch{NN-1}` entry must exist |
| `revelation-schedule.json` | reveals scheduled for NN → must-advance reminder |
| `characters/*.md` | named characters need a sheet (or explicit Codex-only note) |
| `.forge-known-entities.json` | named entities resolve to the Codex cache |

---

## Target architecture — a new Step 0

```text
Step 0 — PRE-FLIGHT GATE  (new; runs before everything)
  1. Derive the required-context set FROM the request (P3):
       beats + their named entities/characters
       + prior epistemic entry + HUD phase + scheduled reveals.
     This set is ALSO the load set — never bulk-load the Codex or prior chapters.
  2. Run tools/forge_preflight.py --chapter NN [--beats ...]   → repo-local PASS/HALT
  3. Run the forge-side beats check (forge_outline_beats / SSH) → outline PASS/HALT
  4. If ANY required input is missing or a stub:
       emit ⛔ PRE-FLIGHT HALT — each gap as a specific question — and STOP.
       Do NOT draft. Do NOT invent.
  5. All-clear only → proceed to Steps 1-9, loading exactly the derived set.
```

**Why a hard STOP and not a soft warning:** the skill already *says* "don't
infer missing context" (Operating Contract, Pre-Draft Questions, Error
Handling), but that is prose the model can rationalize past in the pull to be
helpful. G5 converts the instruction into a discrete gate with a required report
artifact: the agent must emit the PASS/HALT block before any prose exists, which
is what actually makes "outline is law" bite.

---

## MVP scope (this build) vs increments

**MVP:**

- **Step 0 gate** added to the head of the Context Loading Protocol in
  `forge-write/SKILL.md`, with the `⛔ PRE-FLIGHT HALT` format and the
  derive-then-load (P3) instruction.
- **`tools/forge_preflight.py`** — deterministic, zero-token, covering the four
  repo-local checks. Emits a human-readable PASS/HALT report; exit 0 on pass,
  non-zero on halt. Reuses `.forge-known-entities.json`.
- Tighten the existing **Pre-Draft Questions** section so a HALT routes through
  it (the gate feeds the question list rather than duplicating it).

**Increments (after MVP validates):**

1. **Forge-live beat checks** — wire beat-status + stub detection into the script
   when `forge_outline_beats` is session-live (exact, no SSH round-trip).
2. **Beat→entity link map** — scope the entity-presence check to the entities a
   *specific beat* references (from the outline link data), not the whole chapter.
3. **`--json` mode** — structured output the skill consumes directly, so the
   agent reasons over a parsed report instead of free text.

---

## Contract guarantees

- **Never invents** a beat, sheet, or entity to fill a gap. Halts with a question.
- **Minimal-context (P3):** the derived required set defines the load set; no
  bulk Codex or prior-chapter loads.
- **Specific halts:** names the missing beat / sheet / entity (and the chapter's
  must-advance reveals), never a generic "context missing."
- **Degrades, never blocks the build:** when forge isn't session-live the
  deterministic half still runs; the outline half notes fallback mode.

---

## Deliverables

| File | Role |
|---|---|
| `tools/forge_preflight.py` | the deterministic repo-local pre-flight checker |
| `forge-write/SKILL.md` (Step 0 edit) | the gate + HALT format + P3 derive-then-load |
| `tools/README.md` (note) | usage + the forge-side/repo-local split |
| `research/g5-outline-preflight-plan.md` | this plan |

## Status

**G5 MVP BUILT + VALIDATED 2026-05-31.** Scope: gate + deterministic helper
(David's call). Deliverables landed:

- `tools/forge_preflight.py` — stdlib-only, zero-token; the four repo-local
  checks + `--fail-on {halt,warn,never}` exit policy mirroring `prose_lint`.
- `forge-write/SKILL.md` — the standalone "Load Outline Beats" step expanded into
  **Step 4 — Pre-Flight Gate** (4a load+verify beats / 4b derive minimal set /
  4c run the checker / 4d HALT-or-proceed + the `⛔ PRE-FLIGHT HALT` format).
  Operating Contract + Pre-Draft Questions wired to the gate. No renumbering, so
  the external "Step 7b" reference in `voice/exemplars.md` still resolves.
- `tools/README.md` — usage, the repo-local/forge-side split, exit-code policy.

Validated against live repo data: Ch09 PASS with correct WARNs (Marcus
Codex-only, "Meat Grinder" uncached) and correct per-chapter reveal enumeration
(stag-purpose hint / sonja-witness-gift plant / integration-global-scope full);
Ch01 prior-epistemic special case clean; an injected unknown character ("Gandalf")
fired a [HALT] with exit 3; `--fail-on warn` correctly escalated a WARN to exit 3.

Increments #1-3 (forge-live beat checks, beat→entity link map, `--json` mode)
unstarted — the live-beat half is blocked on `forge_outline_beats` being
session-live, exactly as the gate's repo-local/forge-side split anticipates.
