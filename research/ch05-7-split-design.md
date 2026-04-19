# Ch05 Split Design — Floor 1 Tutorial Across 3 Chapters

**Decision date**: 2026-04-19
**Status**: Outline locked, DB restructure pending, prose writing pending
**Trigger**: Original Ch05 (13.9k words, commit `c162258`) crammed Rooms 1-3 into one chapter. Splitting into 3 chapters at 5.5k + 6.5k + 5.5k = **17.5k total Floor 1 budget** gives each fight room to breathe and pulls LitRPG progression mechanics earlier.

---

## Locked Decisions (4)

1. **Ch07 ending** — Floor 1 graduation cue at the end (System message / brief ceremony / floor-completion banner). Treat Room 3 as Floor 1's final room.
2. **First chime placement** — Pull one Power Strike chime forward to Room 1 (Ch05). Readers see the System reward-loop architecture in the FIRST fight, not waiting until Room 2.
3. **Flint progression crunch** — Hybrid tiers + sub-numbers. Example: `"Field Repair: Stage 2 (refinement 31%). Fiber-grain bonding online."`
4. **Ch06 length** — 6,500 words (deeper character work). Full HUD reveal across 4-5 cohort members reading their first character sheets.

---

## Chapter Layout

### Ch05 — "First Blood" (Room 1) — target 5,500w

**Summary**: Tutorial Room 1. Six Thornlings spawn, the cohort takes its first kill and its first losses. Multiple fighters featured (warriors, Mage, Healer first cast). One milestone chime lands during this fight (pulled forward from Room 2) — readers see the System's reward-loop architecture in the very first combat. Nate's crossbow debut, Rex/Judge dog work. Four dead. Ends on door to Rest Area 1 opening.

**Beats (6)**:
1. Corridor approach (carryover from Ch04 ending) — 46 entering Room 1, the math nobody asked for
2. Spawn-burst panic flash, six Thornlings, first wave engagement (3-4 fighters in detail, varied class mechanics visible)
3. Nate's first crossbow shots + Rex/Judge header-and-heeler dog work + first ranching-instinct adaptation
4. Mage overspends Fire Bolt; **first System milestone chime lands on a Warrior (Power Strike unlocks early — moved forward from Room 2)**
5. Wave wraps, four dead, cleanup; weight of un-named losses
6. Door to Rest Area 1 opens; "Forty-six. Four fewer than entered."

---

### Ch06 — "Mana Management" (Rest Area 1 + Room 2) — target 6,500w

**Summary**: The LitRPG dopamine chapter. Rest Area 1 carries the full HUD reveal — 4-5 cohort members visible reading their character sheets (Marcus's Vanguard panel, the Mage's spell list, Josh's Warrior basics, a Healer's reverence at her ability tree, Josie's matter-of-fact Appraiser readout). Nate's PROCESSING + two-arcs contrast lands hard. Josie's crafting scene gives Nate his first Anomaly-channel progression marker via Flint translation (hybrid tier-plus-sub-numbers). Then Room 2: bracketing spawn pattern, "Same monsters. New software." beat, Mage burns dry, Josh fails to chime, three dead.

**Beats (8)**:
1. Rest Area 1 — character sheets opening, healers working, dopamine loop visible across cohort
2. **HUD reveal**: Marcus shares his Vanguard sheet through dialogue; cohort members' first-look reactions (Mage wonder, Josh intimidation, Healer reverence, Josie matter-of-fact)
3. Nate's PROCESSING + two-arcs contrast — "warranty card in a language that doesn't exist yet"
4. **Josie's crafting scene + first Anomaly progression marker via Flint** (hybrid tiers + sub-numbers); thorn bolts crafted
5. Door opens to Room 2; spawn-pattern shift signals the System has adapted
6. Bracketing combat; Mage dimming visibly; Josh fails his chime; female Warrior earns Power Strike (her second milestone if R1 chime was hers, or her first)
7. Rear-spawn deaths — three dead including a Crafter and a kindness (the water-bottle woman)
8. Cleanup, the shock thinning, corridor opens to Rest Area 2

---

### Ch07 — "Trinity Forms" (Rest Area 2 + Room 3) — target 5,500w

**Summary**: Final room of Floor 1. Brief Rest Area 2 with second Anomaly progression marker (Nate files peep sight, SA refines). Room 3 fight: proto-guard mini-boss + 8 basic Thornlings, Marcus runs it as RTS, trinity (tank/healer/DPS) crystallizes. Three thorn bolts find proto-guard joints. Three deaths in cover positions (room itself becomes the weapon). Sam Hargrove's nod to Nate. Brief gold flicker only Rex sees. **Ends on Floor 1 graduation cue** — sets up Floor 2 as next escalation tier.

**Beats (7)**:
1. Rest Area 2 — short; Nate scratches Rex; brief tactical compile; Marcus's headcount + difficulty ramp read
2. Nate files peep sight from torch bracket; **second Anomaly progression marker via Flint** (SA Resolution Tier 2 or similar)
3. Door to Room 3; chamber geometry reveals (cover, elevation, choke points); 8 spawns + the proto-guard
4. Marcus calls the trinity; warriors take the choke; Mage's controlled bursts pay off her Room 2 lesson
5. Nate elevated, three thorn bolts into proto-guard joints; SA painting seams; the curved bolt vindicates Josie
6. Three deaths in cover positions (the room itself as weapon); Sam Hargrove's nod; brief gold flicker only Rex sees; Flint silent
7. **Floor 1 graduation cue** — System message / banner / brief ceremony marking floor completion; setup for Floor 2

---

## Where Mechanics Get Introduced Sooner

- **Ch04 (Room 0)** — modest expansion: when characters first read their HUDs in the safe room, spend 200-400 more words on varied reactions. Mage discovering her spell list, Josie's Appraiser readout, Josh's Warrior basics. Reader tastes the System interface BEFORE combat. *(Optional — for a future Ch04 micro-pass; not required for this Ch05 split.)*
- **Ch05 (Room 1)** — one Warrior milestone chime moved forward from Room 2. Reward-loop visible in first fight.
- **Ch06 (Rest Area 1)** — full HUD reveal chapter. Marcus's sheet detailed through dialogue. Nate's first Anomaly-channel progression marker via Flint.

---

## Nate's HUD as Progression Tool — Implementation

The trick: don't describe the HUD as a static object — show it by what it *tells* Nate in the moment, woven into action.

- **Structural Analysis** wireframe sharpens with use → already established as Nate's progression visual ("new boots on day three")
- **Field Repair** material-bond resolution gets clearer → progression visible through what Nate can craft
- **Flint as translator** → delivers rudimentary tier markers (Stage 1/2/3 + sub-number percentages)
- **Peripheral blue** threat-glow → already established as anomalous spider-sense
- **Glitchy combat log** fragments → Flint catches them, gives Nate strategic intel nobody else has

Pace stays clean because info arrives mid-action, not in expository blocks:

> "**Field Repair: Stage 2** (refinement 31%) — *fiber-grain bonding online,*" Flint said. Nate didn't pause. He kept filing.

---

## File Map

| File | Role |
| ---- | ---- |
| `drafts/ch05-first-blood-draft01.md` | OLD monolithic version (13.9k, all 3 rooms). **READ for reference, DO NOT EDIT.** |
| `drafts/ch05-first-blood-draft02.md` | NEW Room 1 only. **WRITE TO THIS.** |
| `drafts/ch06-mana-management-draft01.md` | NEW Rest Area 1 + Room 2. **WRITE TO THIS.** |
| `drafts/ch07-trinity-forms-draft01.md` | NEW Rest Area 2 + Room 3. **WRITE TO THIS.** |

After all three new drafts are written and committed, archive the monolithic Ch05 to `research/old-versions/` or similar.

---

## DB Restructure Status

**Pending** — forge MCP session expired mid-session 2026-04-19. New Claude session will get a fresh MCP handshake automatically.

**Restructure plan** (execute in next session, Step 1 before any prose):

1. `mcp__forge__forge_outline_show(book_num=1)` — inventory all chapters
2. `mcp__forge__forge_outline_get_chapter(chapter_id=5)` — get current Ch05 beats for deletion
3. **If Ch06+ exist downstream**: delete-and-recreate them with `chapter_num +2`, preserving beats
4. Delete all current Ch05 beats (they describe all 3 rooms — replaced by Room-1-only)
5. `forge_outline_update_chapter(chapter_id=5, ...)` — update title/summary/word_count_target per design doc
6. Create 6 new Ch05 beats per design doc
7. `forge_outline_create_chapter(act=1, chapter_num=6, ...)` — Ch06 with 8 beats
8. `forge_outline_create_chapter(act=1, chapter_num=7, ...)` — Ch07 with 7 beats

---

## Voice Rules in Force (recap)

- **AI-clarification (2026-04-19)**: System IS an AI; AI verbs allowed across all voices (decides, infers, adapts, watches, responds, schedules, queues, plans, optimizes, calibrates, escalates). Only transcendent/metaphysical attribution remains restricted.
- **Profanity**: 18+ audience, moderate OK; **NEVER** Lord's name in vain.
- **Dog body language**: NO `press/pressed against` for Rex/Judge. Allowed: `set`, `planted`, `settled`, `anchored`, `ears pinned`, `weight forward`, `head-on-X`.
- **Bold System terms** as proper nouns only (the **Mage** flared); lowercase for group/action usage.
- **Audiobook is primary medium** — short sentences, sensory grounding, name-readable.
- **Numbers as atmosphere**, not audit-grade headcount.
- **Pop culture refs** OK for Storyteller + Nate (no Star Wars/Jedi/Force — theology collision).
- **POV discipline**: Nate narrates only what he sees; route System data through Flint; show effects not UI.
- **Comedy dial 4-5** weighted toward 4; per-voice matrix in `feedback_humor_punch_up.md`.
- **No `Imago Dei`** in prose; use generic references.
- **System screens are private per-user** (no characters seeing each other's HUDs).

---

## Outline Cascade — Series-Level Implication

If the one-room-per-chapter pattern extends to Floors 2-6 for consistency, Tutorial chapter count grows from ~6 to ~15-18 chapters. **Decision needed in a future session**: does Book 1 end at Tutorial graduation (~18 chapters fits), or extend past it (Book 1 becomes too long, may need to split into two books)?

This is downstream of the Ch05 split — does NOT need to be answered before writing Ch05/06/07.
