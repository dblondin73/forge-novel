# Beneath the Overlay: Integration — Project Instructions

Guidance for Claude Code when working in the `forge-novel` repository.

## What this repo is

Book 1 of a 7-book Christian LitRPG series. David ghostwrites with Claude as
co-author — **David steers, Claude drafts.** The **audiobook** (ElevenLabs
full-cast narration) is the primary deliverable and the master tiebreaker for
every craft decision: when page-sophistication and audio-flow conflict, audio
flow wins.

## Authority order (when guidance conflicts)

1. David's in-session direction
2. `WRITING_RULES.md` — the *how*: voice cast, prose rules, theology-in-craft,
   audiobook punctuation, the 14 hard bans, editorial pass order
3. `REFERENCE.md` — the *what*: locked worldbuilding, 153 Codex entities
4. The `/forge-write` and `/editors-hat` skills
5. `LITRPG_CONVENTIONS.md` — the *why it lands*: genre reader-contract +
   honor/bend/break stances. A reference, not a rule — it **yields** to canon,
   craft, and the audiobook; it tells you what the reader expects so divergence
   is a choice, not an accident
6. `epistemic-states.json` / `revelation-schedule.json` — what Nate knows when

When a tie remains: **audiobook is the primary medium** breaks it.

## How to work here

- **Drafting:** invoke the `/forge-write` skill. **Editing:** `/editors-hat`.
  Do not free-draft without the skill's context-loading protocol — it loads the
  Codex, voice rules, epistemic state, and voice exemplars you need.
- **Prose quality:** run `python kit/prose_lint/prose_lint.py drafts/chNN-*.md`
  before committing a draft. It is a zero-token, deterministic AI-tell linter
  (em-dash density, banned vocabulary, sentence-length burstiness, the
  `not just X but Y` crutch, and more). It **reports only — never auto-strip**,
  especially em-dashes: on narrated chapters those are deliberate audiobook
  stutter-fixes (see `WRITING_RULES.md`). See `kit/README.md`.
- **Voice:** read `voice/exemplars.md` — the curated gold-standard voice bank —
  before drafting a given voice.
- **Genre contract:** when a beat leans on a LitRPG convention (a level-up, loot
  drop, class reveal, stat readout, tutorial-room beat), consult
  `LITRPG_CONVENTIONS.md` for its honor/bend/break stance. Deliver the reader's
  payoff even when the form bends; never honor a convention forge-novel
  deliberately breaks.

## Operating contract

Take these instructions and the skills literally — apply each rule exactly as written.

- Take these instructions and the skills literally; do not generalize or relax
  a rule because it seems to conflict with another — the authority order above
  resolves conflicts.
- Chapter prose is **continuous fiction**: no `##` headers, no bullet lists, no
  bold-for-emphasis inside narrative paragraphs. (System panels, `*italic*`
  thought/error lines, `**bold**` System proper nouns, and `---` scene breaks
  are the only permitted markup.)
- If context is missing — a beat, a character sheet, a Codex entity — stop and
  flag it. Never invent structure to fill the gap.

## Repo map

| Path | Contents |
|---|---|
| `drafts/` | `chNN-*-draft01.md` — chapters; edit in place, git versions them |
| `research/` | worldbuilding & design docs (`old-versions/` is archived) |
| `characters/` | nate-hall, flint, josie-pickett, sonja-lee |
| `voice/exemplars.md` | curated gold-standard voice bank |
| `kit/` | **Standards layer** — portable, genre-agnostic craft tools (`prose_lint`, perplexity, `preflight`, `timeline`) + methods. Bound to this novel via `kit.config.json`. See `kit/LAYERS.md` |
| `tools/` | forge-specific Workflows (chronicler Codex, editorial fan-out) — Novel-layer orchestration |
| `reports/` | dated editorial / lint audit output |
| `.claude/skills/` | `forge-write`, `editors-hat` (versioned with the prose) |
| `REFERENCE.md` `WRITING_RULES.md` `SESSIONS.md` | canon, craft rules, session log |
| `LITRPG_CONVENTIONS.md` | genre contract — reader expectations + honor/bend/break stances |
| `kit.config.json` | binds the kit's portable tools to this novel's files (POV character, state paths) |
| `epistemic-states.json` `revelation-schedule.json` `prose_lint_config.json` | knowledge & reveal tracking; per-chapter lint flags |
| `timeline.json` | append-only in-world event log (Book layer); continuity ground truth — never edit a sealed event, append a superseding one (`kit/timeline/timeline.py`) |

## Git

`origin` is a multi-push remote: it **pulls from GitLab** and **pushes to both
GitLab and GitHub**. `git push origin main` dual-pushes. Never push without
David's explicit say-so; never `git_commit` a draft before David approves it.

## Status

See `WRITING_RULES.md` → "Chapter Status". As of the last update: Ch1-8
unlocked for re-pass; Ch9-10 await first editorial pass.

## History note

This file previously held the build plan for the `git-forge` MCP server. That
server is built and running; the old plan is archived at
`research/old-versions/CLAUDE-git-forge-build-plan.md` and in git history.
