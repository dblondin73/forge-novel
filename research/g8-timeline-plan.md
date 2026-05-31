# G8 — Append-Only Continuity Timeline (P19): Build Plan

> **Tier-3 graft (P19).** The third leg of the *Bible / State / Timeline*
> discipline. Canon is read-only while drafting; knowledge-state is versioned and
> overwritten per chapter; the **timeline of in-world events is append-only and
> immutable**. forge-novel had the first two (REFERENCE.md + Codex; the versioned
> `epistemic-states.json`) but not the third — the append-only history was the
> identified gap. Source: `skill-mining-fantasy-writing.md` P19 (Claude-Book file
> architecture; claude-rpg-skill append-only ledger). Patterns only — no source
> text reproduced.

---

## What it is

A flat, ordered list of in-world events — **one record per thing that happened**,
grouped by chapter — stored in a Book-layer `timeline.json`. Once an event is
committed it is **sealed**: never edited, never deleted. To correct the record you
**append** a new event and name the old `id` in `supersedes`. That immutability is
the whole point: a contradiction between a fresh chapter and the timeline means
*the chapter is wrong*, not that history was quietly rewritten. It is the
continuity ground-truth the editor diffs a draft against.

| P19 leg | What | Mutability | In this repo |
|---|---|---|---|
| **Bible** | locked canon | read-only while drafting | `REFERENCE.md` + Codex |
| **State** | who-knows-what at each boundary | versioned, overwritten per chapter | `epistemic-states.json` |
| **Timeline** | what happened, in order | **append-only, never edited** | `timeline.json` (new) |

---

## The split (consistent with G7's three layers)

| Layer | Artifact | Role |
|---|---|---|
| **Standards** (`kit/`) | `kit/timeline/timeline.py` | Genre-agnostic engine: validate, append-only integrity gate, event views. Knows no novel. |
| **Novel** | `kit.config.json` `paths.timeline`; `editors-hat`/`forge-write` wiring | Binds the engine to forge's store; tells the skills when to read/append/check. |
| **Book** | `timeline.json` | This volume's event log; resets per book. |

The engine **discovers** the repo-root `kit.config.json` (walk up from CWD, then
script dir) and resolves the store path by the kit's standard order: **explicit
`--timeline` flag > binding `paths.timeline` > built-in `<repo>/timeline.json`.**
Unbound, it runs standalone.

---

## The deterministic half vs the agent's half

Exactly the preflight division of labor. The **semantic continuity diff** — *does
this draft contradict the recorded events?* — is an editorial judgement and stays
agent-side (`editors-hat` Pass 2). The tool does only the **deterministic** half:

- **`check`** — keep the log honest: structural validation **+** append-only
  integrity vs `git HEAD`.
- **`events --chapter N`** — surface the recorded ground truth for the agent to
  diff against.
- **`validate`** / **`render`** — structure-only check; human-readable markdown.

The tool never reads prose and never edits the log.

---

## The append-only gate (`check`)

`check` compares the working `timeline.json` against `git show HEAD:<rel>`:

- a sealed event that was **modified** or **deleted** → **[BREACH]** (exit `3`);
- newly **appended** events → fine;
- file not in HEAD yet, or not a git work tree → sealed-history check skipped
  with INFO (nothing is sealed yet).

**Cross-platform bug caught in validation:** `subprocess.run(text=True)` decodes
git's stdout with the platform default (cp1252 on Windows), which mangles any
non-ASCII event text and makes a sealed event falsely compare as *modified*
against the UTF-8 working copy. Fixed by decoding git output as UTF-8 explicitly
(`encoding="utf-8", errors="replace"`). Proven by a throwaway-repo breach sim:
em-dash events no longer false-positive; real edits/deletes still caught.

---

## Event schema

Required: `id` (stable, unique, never reused), `chapter` (int), `event`. Optional:
`seq` (order within chapter), `kind` (`world`/`system`/`character`/`relationship`/
`knowledge`/`progression`/`combat`/`death`/`item`/`location`/`travel`), `who`
(list), `where`, `when` (free-text in-world clock), `supersedes` (id this
corrects), `source` (provenance). Validation: duplicate id / missing required
field → **ERROR**; non-monotonic chapter order, unknown `kind`, dangling
`supersedes`, duplicate `(chapter, seq)` → **WARN**.

---

## Seeding (no invention)

`timeline.json` is seeded **only** from `epistemic-states.json`
`nate.after_chNN.learned_this_chapter` (ch01–ch08) — the only canon-tracked
per-chapter record available — as knowledge/introduction events, each with `source`
provenance. The log is intentionally thin; the chronicler/editorial pass enriches
it append-only (combat, deaths — e.g. Tyler Sorensen ch6, progression, world
events) as chapters lock. Per CLAUDE.md's "never invent structure to fill the gap,"
nothing was seeded beyond what epistemic-states already asserts.

---

## Wiring

| File | Change |
|---|---|
| `kit/timeline/timeline.py` | NEW — the engine. |
| `timeline.json` | NEW — repo root (Book layer), seeded from epistemic-states. |
| `kit.config.json` | `paths.timeline: "timeline.json"`. |
| `kit/kit.config.example.json` | documented `timeline` key. |
| `kit/README.md` | tool-table row, binding-keys list, full timeline section. |
| `kit/LAYERS.md` | `kit/timeline/` under Standards; `timeline.json` under Book. |
| `CLAUDE.md` (forge-novel) | repo-map `timeline.json` row + `timeline` in the kit row. |
| `editors-hat/SKILL.md` | Pass 2 — read+diff the record, then append + `check`. |
| `forge-write/SKILL.md` | Step 5 read recorded events; Step 8 after-drafting append + `check`. |

---

## Validation gates (run before commit)

1. `py_compile` + `ruff check kit/timeline/` clean.
2. `validate` / `check` PASS on the seed (10 events, ids unique).
3. **Append-only breach sim** in a throwaway git repo: baseline clean (no false
   breach on em-dash events), then a modify + a delete + a legit append → exactly
   2 BREACH, exit 3; the append is *not* flagged.
4. Structural negative test: duplicate id + missing field → 2 ERROR exit 3; unknown
   kind / dangling supersedes / append-order / dup-seq → WARN.
5. `events`/`render` views render text/json/md for a chapter selector.
6. PostToolUse prose-lint hook unaffected (no shared code touched).
7. `git status` — only intended files staged; David's 2 untracked reports excluded.

## Status

**BUILT + VALIDATED 2026-05-31.** All gates passed. The append-only gate fires on
edit and delete (exit 3) and ignores legit appends; the Windows UTF-8 git-decode
bug was caught and fixed in validation. Seeded from canon-tracked
`learned_this_chapter` only — no invented events. Engine is binding-driven
(CLI > kit.config.json > built-in), consistent with the G7 kit.
