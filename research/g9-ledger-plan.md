# G9 — Promise/Payoff Ledger + Character-Sim + Recap: Build Plan

> **Tier-3 graft (P8 + P15 + ledger-idea #3).** Three related deliverables under
> one graft: a **promise/payoff ledger** (the "Mercy Engine") that generalizes
> revelation tracking into every kind of planted promise; a **character-sim
> discovery mode** that interrogates a character in-voice before drafting a hard
> beat; and a **recap source-pack aggregator** for "Previously On" beats. Sources:
> Crucible Mercy Engine (P8), `creative-writing-skills` Character-sim (P15),
> story-narrative-summary / RPG-session-summarizer (idea #3). Patterns only — no
> source text reproduced.

---

## What it is

Three pieces, one theme — *track the threads the story owes the reader*:

| Piece | Layer | What |
|---|---|---|
| **`kit/ledger/ledger.py`** | Standards | Promise/payoff engine: validate, overdue sweep, surface planted-but-unpaid threads. |
| **`promises.json`** | Book | This volume's ledger; seeded from the revelation schedule. |
| **Character-sim mode** | Novel (`forge-write`) | Pre-draft in-voice interrogation of a Codex character. Discovery, never prose. |
| **`kit/recap/recap.py`** | Standards | "Previously On" source-pack aggregator over timeline + ledger + epistemic. |

---

## 1 · The promise/payoff ledger (P8)

A flat list of promises to the reader, each with a payoff slot. Every
foreshadow, Chekhov's gun, mercy, debt, threat, posed mystery, vow, or scheduled
reveal is one record. The whole point is the **unpaid sweep**: a gun that never
fires, a mercy that never returns, a mystery posed and forgotten is a continuity
hole. The editor diffs each chapter against the open threads.

### Mutable state, not append-only — the key design call

The ledger is the **`revelation-schedule.json` analog**, not the `timeline.json`
analog. A promise's status legitimately changes over its life (`open` → `paid`),
so — deliberately — there is **no git seal** here. This keeps the clean P19
distinction G8 established intact:

- **Timeline** (G8) = *what happened*, append-only, git-sealed (a sealed edit is a
  BREACH).
- **Ledger** (G9) = *what was promised*, mutable, freely edited (a status moves
  open → paid as the story delivers).

A silently dropped thread surfaces as perpetually `open` — that is the report,
not a breach. Conflating the two would muddy G8's discipline; the "don't lose a
thread" guarantee is served by the open/overdue reports themselves.

### Deterministic half vs agent half

Exactly the preflight/timeline division. The tool keeps the store honest
(`validate`/`check`) and **surfaces** the open threads (`open`); the **semantic
judgement** — does *this* draft pay off *this* promise? — stays agent-side
(`editors-hat` Pass 2). The tool never reads prose.

### Overdue needs a frontier (honesty about future-targeted data)

A promise is **overdue** when it is open, has a `due_by_chapter`, and that chapter
has been reached. "Reached" can't be inferred from the data — the ledger holds
future hint/reveal chapters — so overdue detection **requires `--through N`** (the
latest drafted chapter). Without it, `check` reports open/paid counts and says to
pass `--through`. Overdue is **WARN**, never a hard block: a 7-book series
legitimately holds a promise open across volumes; the editor decides if it is a
real drop.

### Kinds + schema

Kinds: `foreshadow`, `chekhov`, `mercy`, `debt`, `threat`, `question`, `vow`,
`reveal`. Required fields: `id`, `kind`, `promise`, `planted_chapter`, `status`
(`open`/`paid`/`abandoned`/`subverted`). Optional: `reinforced_chapters`,
`due_by_chapter`, `payoff` + `paid_chapter`, `who`, `notes`, `source`. Validation:
duplicate id / missing required / bad `planted_chapter` / unknown `status` →
**ERROR**; unknown `kind` / paid-without-chapter / open-with-paid-chapter /
out-of-order due-by → **WARN**. (`status` is ERROR-on-unknown because it gates the
open/paid logic; `kind` is WARN like the timeline's taxonomy.)

### Seeding (no invention)

`promises.json` is seeded **only** from `revelation-schedule.json` — the one
canon-tracked setup→payoff store — as 7 `reveal`-kind promises (`planted_chapter`
← `plant_chapter`, `reinforced_chapters` ← `hint_chapters`, `due_by_chapter` ←
`full_reveal_chapter`, `who` ← `characters_who_learn`). None are paid yet (no
reveal has reached its full-reveal chapter). The other kinds (mercy, chekhov,
debt, vow, threat, question) are appended by the editorial pass as chapters lock.
Per CLAUDE.md's "never invent structure to fill the gap," nothing was seeded
beyond what the revelation schedule already asserts.

### The two stores stay complementary, not redundant

`revelation-schedule.json` remains the source of truth for **scheduling** (which
reveal `forge-write` must advance in a given chapter — Step 8). `promises.json` is
the source of truth for **payoff status across all kinds**, so the editor's
unpaid-thread sweep covers reveals too. Reveals are mirrored into the ledger as
the seed; the schedule keeps driving the "advance this now" decision.

---

## 2 · Character-sim discovery mode (P15)

A `forge-write` sub-mode (`/forge-write <ch> sim "<Character>" "<situation>"`).
Before a hard beat, role-play a Codex character in-voice for a few turns to
discover how they would actually react — loaded from their sheet, their
`voice/exemplars.md` section, and **the epistemic entry for this chapter
boundary** so the sim can't leak future knowledge. Output is discovery
scaffolding; **it never ships as prose** — the chapter is still drafted through
the normal Steps 4-9 using what the sim revealed. No engine — it is a skill
addition (the model role-plays under the same prose constraints).

---

## 3 · Recap source-pack aggregator (idea #3)

`kit/recap/recap.py` merges three already-maintained stores for a chapter range —
the timeline (what happened), the ledger (what's still promised), and
epistemic-states (what the POV learned) — into one **source pack**. It writes
**no prose**: the "Previously on…" is a Storyteller-voice task and stays
agent-side. A thin, standalone aggregator (no cross-imports from sibling kit
tools); any missing source is skipped with a note so a partly-wired project still
gets a usable pack. Needs no binding key of its own — it reads `timeline`,
`promises`, `epistemic_states`, `pov_character` from the binding. Generator, not a
gate: exit `0` always.

---

## Wiring

| File | Change |
|---|---|
| `kit/ledger/ledger.py` | NEW — the promise/payoff engine. |
| `kit/recap/recap.py` | NEW — the recap aggregator. |
| `promises.json` | NEW — repo root (Book layer), seeded from the revelation schedule. |
| `kit.config.json` | `paths.promises: "promises.json"`. |
| `kit/kit.config.example.json` | documented `promises` key. |
| `kit/README.md` | two tool-table rows, binding-keys list, full ledger + recap sections. |
| `kit/LAYERS.md` | `kit/ledger/` + `kit/recap/` under Standards; `promises.json` under Book. |
| `CLAUDE.md` (forge-novel) | repo-map `promises.json` row + `ledger`/`recap` in the kit row. |
| `editors-hat/SKILL.md` | Pass 2 — open-thread sweep, judge each, then update the ledger. |
| `forge-write/SKILL.md` | usage line + Character-Sim section; Step 5 read open threads (+ optional recap); Step 8 update the ledger after drafting. |

---

## Validation gates (run before commit)

1. `py_compile` + `ruff check kit/ledger/ kit/recap/` clean.
2. `validate` / `check` PASS on the seed (7 promises, ids unique, 0 paid).
3. **Overdue trigger:** `check --through 9` flags `rev-integration-global-scope`
   (due ch9) as a WARN; `--through 8` is clean.
4. **Structural negatives:** a throwaway store with a duplicate id + missing
   field + `planted_chapter` 0 + bad status → 4 ERROR exit 3; unknown kind /
   paid-without-chapter / open-with-paid → WARN.
5. **Views:** `open --through 8`, `open --overdue`, `render --kind reveal` render
   text/json/md.
6. **Recap:** `recap --chapter 1-8` merges 10 events + 6 open threads + Nate's
   learned-this-chapter; `--format json` well-formed; missing-source path skips
   with a note.
7. PostToolUse prose-lint hook unaffected (no shared code touched).
8. `git status` — only intended files staged; David's 2 untracked reports excluded.

## Status

**BUILT + VALIDATED 2026-05-31.** All gates passed. The ledger surfaces
planted-but-unpaid threads and flags overdue ones (WARN, frontier-gated); the
recap aggregator merges the three continuity stores into a prose-free source pack;
the character-sim mode is wired into `forge-write` as discovery-only. Seeded from
canon-tracked `revelation-schedule.json` only — no invented promises. Both engines
are binding-driven (CLI > `kit.config.json` > built-in), consistent with the G7
kit. The ledger is deliberately **mutable state** (no git seal), preserving G8's
append-only timeline distinction.
