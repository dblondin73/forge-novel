# Cowork Prompts — forge-novel

*Ready-to-paste prompts for Claude Cowork tasks. Copy the full prompt text and paste into Cowork.*
*Point Cowork at the forge-novel folder before running any prompt that reads/writes repo files.*
*Both forge-mcp and git-forge must be active in Claude Desktop config for MCP prompts to work.*

---

## Prompt 1 — "MC" to "Nate" Audit

**What it does:** Sweeps the entire repo for stale "MC" references in POV fields,
beat content, and character references. Report only — no changes made.
Run this first before any rename sweep.

**Output:** `reports/mc-to-nate-audit.md` committed and pushed to GitHub.

```
Using the git-forge MCP server, search the entire forge-novel
repository for every instance of the string "MC" appearing in
POV fields, beat content, or character references across all
.md files. Generate a report file called
reports/mc-to-nate-audit.md listing every match with the file
name, line number, and the full line of text. Do not make any
changes yet — report only. When the report is complete, commit
it to the repo with the message "audit MC references for Nate
rename" and push to GitHub.
```

---

## Prompt 2 — Chapter 1 Prose Draft

**What it does:** Reads character files and Chapter 1 beats from forge-mcp,
then drafts ~3,500 words of Chapter 1 prose in Nate's voice using the
Narnia Principle. First actual pages of the book.

**Output:** `drafts/ch01-the-last-normal-tuesday-draft01.md` committed and pushed.

**Run after:** Prompt 1 audit is clean (no stale MC references in character files).

```
Using the git-forge MCP server, read the file characters/nate-hall.md
and characters/flint.md for character context. Then read the
outline for Book 1 Chapter 1 "The Last Normal Tuesday" from the
forge-mcp outline tool — chapter ID 1, all 4 beats. Using the
Narnia Principle (show don't tell, theology is the skeleton not
the dialogue), Nate's established voice (dry, engineering-brained,
ranch-practical), and the beat content as your scene structure,
draft Chapter 1 as prose targeting 3,500 words. Write in close
third person POV from Nate's perspective. Save the draft to
drafts/ch01-the-last-normal-tuesday-draft01.md and commit with
message "Chapter 1 first prose draft" and push to GitHub.
```

---

## Prompt 3 — REFERENCE.md Rebuild

**What it does:** Pulls all active Codex entities tagged "core" from forge-mcp
and rebuilds REFERENCE.md as a scannable quick-reference for locked
worldbuilding decisions. Replaces the stale/erroring version.

**Output:** `REFERENCE.md` at repo root committed and pushed.

```
Using the forge-mcp MCP server, pull all active Codex entities
tagged "core" across all entity types (character, location,
game_mechanic, faction, lore). Organize them into a REFERENCE.md
file with sections: Core Characters, Factions, Game Mechanics,
Locations, Lore and Writing Rules. For each entity include the
name, a 2-3 sentence summary of the key locked decisions, and
the Codex entity ID for reference. This file is the quick-reference
for locked worldbuilding decisions — write it to be scannable,
not exhaustive. Save to REFERENCE.md in the repo root, commit
with message "Rebuild REFERENCE.md from live Codex data" and
push to GitHub.
```

---

## Prompt 4 — Stag Mythology + East Texas Whitetail Research

**What it does:** Uses Claude in Chrome to research whitetail deer behavior
in East Texas, Welsh/Norse/Celtic Christian stag mythology, and synthesizes
story bible notes with 3-4 candidate directions for what the stag actually is.

**Output:** `research/stag-mythology.md` committed and pushed.

**Requires:** Claude in Chrome connector active in Cowork.

```
Using Claude in Chrome, research and compile a reference document
covering the following. Save all findings to
research/stag-mythology.md when complete, then commit with message
"Add stag mythology and whitetail deer research" and push to GitHub.

SECTION 1 — WHITETAIL DEER: EAST TEXAS BIOLOGY AND BEHAVIOR
Research whitetail deer (Odocoileus virginianus) specific to the
East Texas Pineywoods region. Cover: typical size and appearance,
behavioral patterns at dawn (this is the time of the inciting
incident — Nate is on horseback at sunrise), how they react to
horses and humans, what "wrong" behavior would look like to an
experienced East Texas rancher (movements too fluid, not spooked
normally, holding eye contact). The goal is to understand what
Nate's baseline expectation of a deer is so we can define exactly
how the stag deviates from it.

SECTION 2 — WELSH MYTHOLOGY: WHITE STAGS AND MAGICAL DEER
Research white stags and magical deer in Welsh tradition — the
Mabinogion, Arthurian Welsh lore, the Cwn Annwn (Annwn hounds
and the stags they hunt), Arawn's white stag in Pwyll Prince of
Dyfed. Cover: what the white stag symbolizes, whether it acts as
a guide or catalyst, any connection to threshold moments or
otherworld contact, and whether eye contact with the stag carries
specific meaning.

SECTION 3 — CELTIC CHRISTIAN TRADITION: STAG AS DIVINE MESSENGER
Research the stag in Celtic Christian spirituality — St. Hubert
and the stag with the crucifix between its antlers, St. Eustace's
conversion moment, the Irish tradition of the stag as a soul-guide,
any thin-places connection. Cover: whether the stag is seen as a
messenger from God, a threshold creature, or a catalyst for
spiritual awakening. Note any traditions where encountering a stag
triggers an irreversible change.

SECTION 4 — NORSE MYTHOLOGY: DEER AND STAG FIGURES
Research stag figures in Norse tradition — Eikþyrnir (the stag
on Valhalla's roof), the four stags grazing on Yggdrasil
(Dáinn, Dvalinn, Duneyrr, Duraþrór), any stag-adjacent beings
in the Eddas. Cover: what stags represent in the Norse cosmological
framework, whether they appear as boundary or threshold creatures,
and any connection to the world-tree or divine architecture.

SECTION 5 — SYNTHESIS: STORY BIBLE NOTES
Based on all of the above, write a short synthesis section
(half a page) answering: What properties does the stag need
to have to be simultaneously recognizable as a whitetail to
Nate's rancher eye AND wrong in a way only he would notice?
What mythological tradition best fits a creature that triggers
a spiritual awakening on eye contact? Could the stag be a
specific named being from Welsh or Norse tradition, or should
it be something new that draws from both? List 3-4 candidate
directions with a one-sentence case for each.
```

---

## Recommended Run Order

1. **Prompt 1** — Audit first, no risk, tells you what needs fixing
2. **Prompt 4** — Stag research, feeds the next creative session
3. **Prompt 3** — REFERENCE.md rebuild, useful before drafting
4. **Prompt 2** — Chapter 1 draft, run when you have time to read and react

---

*Last updated: 2026-03-20 | Session 004*
