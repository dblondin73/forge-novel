# Voice Exemplar Bank — Beneath the Overlay

Curated gold-standard prose. Each entry is a **locked or fully-edited excerpt**
that defines how a voice should sound. `/forge-write` loads this file before
drafting (Context Loading Protocol, Step 7b) and matches the cadence, register,
sentence-length variation, and punctuation density of the closest exemplar.

**Target size: ~12,000-15,000 words total.** Research on voice mimicry shows
reproduction quality climbs sharply once the model has 10-20k words of real
samples; below that, output is "similar but somehow off." Curated *passages* —
not whole chapters — so every word here is best-in-class and the file stays
loadable inside a context budget.

---

## How to use this file

**When drafting (`/forge-write`):** read the sections matching the voices in
your target beats. Imitate the nearest exemplar's cadence — not your default
register. These passages are the canonical target.

**This file is read-only reference.** Never draft new prose into it. When a
source chapter is re-edited, re-sync the affected excerpt from its source.

---

## How to curate (David's editorial call)

This is a scaffold. The passages themselves are David's selection — drop them
in below the section headers. Selection criteria for a gold-standard excerpt:

- It comes from a **locked or twice-edited** chapter (Ch4 is locked; Ch1-3 are
  edited). Never seed from an un-passed draft.
- It is the **strongest** instance of that voice/function in the manuscript —
  the passage you would point a new collaborator to and say "sound like this."
- It is **self-contained** — readable without the surrounding scene.
- It carries **visible sentence-length variation** (burstiness) — not a uniform
  block. Run a candidate through `tools/prose_lint.py` if unsure.

**Entry format** — label every excerpt so it can be re-synced:

```
### <short title>
> Source: ch04-safe-room-draft01.md, paragraphs <range or description>
> Function: <what this passage exemplifies>

<the excerpt verbatim>
```

Three passages are pre-nominated as canonical in `WRITING_RULES.md` and the
`editors-hat` skill — seed these first:

- **Ch4 — the scrolling-suit-guy / Karen stack** — canonical Comedy Dial 4-5
  reference beat. → Section 5 (Flint) or Section 3 (Nate close-third), wherever
  the stack's voice sits.
- **Ch4 — "That's not supposed to do that"** — canonical *protected dramatic
  beat*, left at Dial 1 against punched-up surroundings. → Section 7.
- **Ch4 — the pasture-inventory eye-sweep ("Fifty people. Give or take.")** —
  canonical grounded callback-fragment. → Section 8.

---

## 1. Storyteller — Omniscient Register (Hiberno-English)

~3,000 words. Chapter opens/closes, interludes, dramatic irony, retrospective
wisdom. Must carry Hiberno markers: after-perfective, "ye'll find," "yer man,"
Catholic-flavoured similes. Source candidates: Ch4 opening, any interlude.

_(curate here)_

---

## 2. Storyteller — Physical-Zoom Register (plain literary)

~2,500 words. Sensory detail, combat, action rendered from outside Nate's head.
Plain literary English — NO Hiberno markers. Cadence tightens in combat.

_(curate here)_

---

## 3. Nate — Close-Third Prose

~3,000 words. Tight-third narration: the High-Tech-Red-Neck blend of rancher,
engineer, fantasy-reader, gamer vocabulary — shown through word choice, never
lens labels.

_(curate here)_

---

## 4. Nate — Dialogue (dry, Sam Elliott)

~1,000 words. Short, dry, precise. Bullets not speeches. Rare one-liners that
land because they are rare.

_(curate here)_

---

## 5. Flint — Dialogue (Bob the Skull register, Comedy Dial 5)

~2,000 words. Theatrical, fast, stacked punchlines on named targets. Include
the Ch4 scrolling-suit-guy stack. Design-intent claims hedged (early Book 1).

_(curate here)_

---

## 6. Pack-Bond Translation (Rex / Judge)

~800 words. Carried in Nate's voice channel — Scots-flavoured for Rex,
Aussie-flavoured for Judge. Dog-shaped content only.

_(curate here)_

---

## 7. Protected Dramatic Beats (register-drop exemplars)

~600 words. The quiet beats that drop to Dial 1-2 against punched-up
surroundings. Include Ch4's "That's not supposed to do that."

_(curate here)_

---

## 8. Voice Transitions (read-aloud-clean handoffs)

~800 words. Storyteller ↔ Nate ↔ Flint handoffs that pass the read-aloud test:
tonal bridge on exit, grounding re-anchor on return, self-contained fragments,
grounded callback fragments. Include Ch4's pasture-inventory eye-sweep.

_(curate here)_
