# G7 — Three-Layer Split (Standards / Novel / Book): Build Plan

> **Tier-3 graft (P16).** The organizing principle for David's "forge-novel AND a
> reusable kit" goal. Carve the portable, genre-agnostic craft tooling
> (**Standards**) out of forge-novel's canon (**Novel**) and per-volume state
> (**Book**), so a future project swaps the Novel + Book layers and keeps the kit.
> Scope this pass (David's call): **full physical extraction** — actually move the
> portable tools into `kit/` and generalize them to be config-driven, not just
> document the layering. Source: `skill-mining-fantasy-writing.md` P16.

---

## The three layers

| Layer | What it is | Portability | Examples |
|---|---|---|---|
| **Standards** | Genre-agnostic craft tooling + methods. The kit. | Portable — copy to any prose project. | `prose_lint` engine, perplexity spot-checker, the preflight gate, the HONOR/BEND/BREAK genre-conventions *method*. |
| **Novel** | This book's canon + book-specific orchestration. | forge-novel-only. | `REFERENCE.md`, `WRITING_RULES.md`, `LITRPG_CONVENTIONS.md`, `characters/`, `voice/`, the `/forge-write` + `/editors-hat` skills, the chronicler/fanout Workflows, the Codex tooling. |
| **Book** | Per-volume narrative state. | Per-book; resets each volume. | `epistemic-states.json`, `revelation-schedule.json`, `drafts/`, `SESSIONS.md`, `reports/`, the entity cache, the per-chapter `prose_lint_config.json` (`audiobook_locked` flags). |

Each layer narrows the one above: Standards knows nothing of forge-novel; the
Novel layer binds the Standards tools to its canon; the Book layer is the state
those tools read.

---

## The binding seam — `kit.config.json`

A genre-agnostic tool cannot hardcode `nate`, `epistemic-states.json`, or
`anti-slop.md`. The seam is a single repo-root **`kit.config.json`** that the
Novel layer owns and the Standards tools *discover* (walk up from CWD / the
script dir until found). When no binding is found, each tool falls back to
portable built-in defaults — so the kit runs standalone, and runs **identically**
for forge-novel when the binding is present.

```jsonc
// kit.config.json (repo root) — forge-novel's binding to the Standards kit
{
  "novel": "Beneath the Overlay: Integration",
  "pov_character": "nate",
  "paths": {
    "epistemic_states":    "epistemic-states.json",
    "revelation_schedule": "revelation-schedule.json",
    "characters_dir":      "characters",
    "entity_cache":        ".claude/skills/forge-write/scripts/.forge-known-entities.json",
    "anti_slop":           ".claude/skills/forge-write/references/anti-slop.md",
    "prose_lint_config":   "prose_lint_config.json",
    "draft_glob":          "drafts/ch*-*.md"
  }
}
```

Resolution priority for every configurable path: **explicit CLI flag > kit.config.json binding > portable built-in default.** This preserves today's
behavior exactly (forge keeps its own `anti-slop.md` + `prose_lint_config.json`)
while making the tools portable.

---

## Target structure (in-repo extraction)

`kit/` is a subfolder, not a separate repo — it keeps the `c:/Workbench/dev/forge-novel/` path the skills + hooks depend on intact and keeps one git
history. A separate kit repo is a later step.

```text
kit/                              ← STANDARDS layer
  README.md                       ← what the kit is + how to bind it to a Novel
  LAYERS.md                       ← this three-layer model (the portable doc)
  kit.config.example.json         ← the binding schema, documented
  prose_lint/
    prose_lint.py                 ← engine (config-discovery added)
    prose_lint_rules.py
    prose_lint_segment.py
    prose_lint_hook.py
    prose_lint_defaults.json      ← thresholds only (Standards)
    anti-slop-base.md             ← generic AI-slop starter (no forge bans)
  perplexity/
    prose_predictability.py
  preflight/
    preflight.py                  ← was forge_preflight.py; now binding-driven
  methods/
    genre-conventions-template.md ← the HONOR/BEND/BREAK method (from G6)

kit.config.json                   ← repo root: the Novel→Standards binding
prose_lint_config.json            ← repo root: Book-layer per-chapter flags (moved from tools/)

# Unchanged, now classified Novel: REFERENCE.md WRITING_RULES.md LITRPG_CONVENTIONS.md
#   characters/ voice/ research/ .claude/skills/{forge-write,editors-hat}/
#   tools/{chronicler_codex,editors_hat_fanout}.* (forge-specific Workflows)
#   .claude/skills/forge-write/scripts/{check-proper-nouns,refresh-entity-cache}.py
#   .claude/skills/forge-write/references/anti-slop.md (forge bans)

# Unchanged, now classified Book: epistemic-states.json revelation-schedule.json
#   drafts/ SESSIONS.md reports/ .forge-known-entities.json
```

**What moves:** only the genuinely portable engines (`prose_lint*`,
`prose_predictability`, `forge_preflight`→`preflight`) + the Book-layer
`prose_lint_config.json`. **What stays:** forge-specific orchestration
(chronicler, fanout) and Codex tooling (check-proper-nouns, refresh-entity-cache)
remain in the Novel layer where they already live — they are not portable, so
moving them buys nothing and adds risk.

---

## Path-update inventory (every functional reference that must change)

| File | Old | New |
|---|---|---|
| `.claude/settings.json` (PostToolUse) | `tools/prose_lint_hook.py` | `kit/prose_lint/prose_lint_hook.py` |
| `.claude/skills/editors-hat/SKILL.md` (Pass 0a) | `tools/prose_lint.py` | `kit/prose_lint/prose_lint.py` |
| `.claude/skills/forge-write/SKILL.md` (Step 4c, item 31, contract) | `tools/forge_preflight.py`, `tools/prose_lint.py` | `kit/preflight/preflight.py`, `kit/prose_lint/prose_lint.py` |
| `tools/editors_hat_fanout.workflow.js` (`LINTER` const) | `tools/prose_lint.py` | `kit/prose_lint/prose_lint.py` |
| `prose_lint.py` internals | `DEFAULT_CONFIG`, `DEFAULT_ANTI_SLOP` hardcoded | binding-discovery + portable fallbacks |
| `preflight.py` internals | `nate`, state paths, cache path hardcoded | binding-driven + flags |
| `CLAUDE.md` (forge-novel) | `tools/prose_lint.py`; repo map | `kit/` paths; repo map + layer note |
| `voice/exemplars.md` | `tools/prose_lint.py` | `kit/prose_lint/prose_lint.py` |
| `tools/README.md` | prose_lint/perplexity/preflight sections | moved to `kit/README.md`; tools/README keeps forge-only tools |

**Deliberately left (historical/plan records):** `research/g5-outline-preflight-plan.md`, `g1-editorial-pipeline-plan.md`, and other dated docs cite
`tools/forge_preflight.py` as the state at *their* writing — this plan supersedes
them; revising them would be revisionist. `WRITING_RULES.md` + `anti-slop.md`
cite `prose_lint.py` by name only (no path) — unaffected.

**Out of scope (different repo):** `c:\Workbench\CLAUDE.md` mentions forge-novel
tooling generically; it is the parent project's file, not committed with
forge-novel, and remains accurate.

---

## Validation checklist (run before commit)

1. `python -m py_compile` on every moved/edited `.py` (kit engines).
2. `prose_lint` **before/after diff** — run on a chapter pre-move (captured) and
   post-move; output must be byte-identical (proves the binding preserves forge
   behavior: same anti-slop, same `audiobook_locked`).
3. `preflight.py --chapter 9 --characters ... --entities ...` — same PASS/WARN
   result as G5 validation (Marcus Codex-only, "Meat Grinder" uncached, reveals
   enumerated).
4. Hook path resolves: simulate the PostToolUse JSON on stdin to
   `kit/prose_lint/prose_lint_hook.py`, confirm it finds `kit.config.json` from
   CWD and reports.
5. `ruff check kit/` clean.
6. `git status` — only intended files staged; **David's 2 untracked reports
   excluded**.

---

## Contract guarantees

- **Behavior-preserving for forge-novel.** With `kit.config.json` present, every
  tool resolves the exact same forge files it does today. The before/after lint
  diff is the proof.
- **Genuinely portable.** Each tool runs standalone with built-in defaults when
  no binding is found — the kit is copy-pasteable to another prose project that
  writes its own `kit.config.json`.
- **History preserved.** Moves use `git mv`; blame/log survive.
- **No writing disruption.** The active draft workflow (forge-write / editors-hat
  / the hooks) works unchanged after the rewire — only paths moved.

## Deliverables

| File | Role |
|---|---|
| `kit/` (engines + scaffold) | the extracted Standards layer |
| `kit.config.json` | the Novel→Standards binding seam |
| `kit/LAYERS.md`, `kit/README.md` | the portable architecture + usage docs |
| rewired `settings.json` / both SKILLs / fanout / CLAUDE.md / exemplars | references follow the move |
| `research/g7-three-layer-split-plan.md` | this plan |

## Status

**BUILT + VALIDATED 2026-05-31.** Full physical extraction (David's scope).
All validation gates passed: `py_compile` clean on the six moved engines;
`ruff check kit/` clean; the **prose_lint before/after diff on Ch09 is
byte-identical** (binding preserves forge's anti-slop + `audiobook_locked`);
`preflight` parity confirmed (Ch09 PASS w/ the two expected WARNs + reveal
enumeration via the `nate` POV key from the binding, Ch01 special case,
injected-unknown HALT exit 3); the re-pathed PostToolUse hook
(`kit/prose_lint/prose_lint_hook.py`) discovers `kit.config.json` from CWD and
reports (stdin-simulated, exit 0). All functional references rewired
(settings.json, both SKILLs, fanout `LINTER`, CLAUDE.md, exemplars,
tools/README). The forge-specific Workflows (chronicler, fanout) + Codex tooling
stayed in the Novel layer by design.
