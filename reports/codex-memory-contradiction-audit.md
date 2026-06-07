# Codex/Memory Contradiction Audit
Candidates 48 | Confirmed 23 | Dismissed 25


---

## [C1] HIGH · dangling-reference · dangling-confirmed
**Topic:** Invented Codex IDs #177/#178/#179/#180/#181 do not exist in canon (max ID #153) — cited across memory and locked research docs
**A (project_forge_soul_dna_architecture.md; research/soul-dna-architecture.md; research/true-names-and-false-labels.md; research/cornerstone-settlement-design.md; research/skill-system-design.md):** Cite Codex #177 (Labyrinth-as-pipeline / Skill System Architecture), #178 (Conduit Overlay / Amplification), #179 (Substrate-vs-allegiance routing), #180 (True Names & False Labels), #181 (Soul-DNA Architecture) as authoritative cross-references; #181 self-flagged 'pending creation' in memory but 'Ingested 2026-05-09' in research/soul-dna-architecture.md.
**B (REFERENCE.md):** 'Source: forge-mcp Codex — 153 active entities'; Quick Stats Total 153; maximum defined ID is #153 (Conduit Kinetics). NO entries #177, #178, #179, #180, or #181 exist anywhere in the file. The Labyrinth is actually #17; the cited #177 looks like a typo/hallucination of #17.
**Fix:** Two-part fix. (1) Reconcile the #181 status lie first (cheapest, highest-confidence): edit research/soul-dna-architecture.md lines 3-4 to match reality — change "Codex #181 (forge ...) / Ingested to forge codex 2026-05-09" to "Codex draft — pending forge codex ingestion" (the same honest wording true-names-and-false-labels.md line 3 already uses). (2) De-authorize the invented ID block: until forge-mcp is reachable and the entities are actually created, the 2026-04-23/05-09 decisions should be referenced by NAME, not by a fabricated number — e.g. replace "Codex #177" with "[Skill System Architecture — pending Codex ID]" etc. across research/*.md, prompts/magic_system.md, prompts/forge-novel-session-start.md, research/skill-taxonomy-build.py, and both .claude/skills SKILL.md files; and drop the "LOCKED 2026-04-23" framing on numbers that were never minted. Then, when MCP/SSH access returns (the existing REFERENCE.md TODO), create the entities, capture their REAL assigned IDs, and backfill the placeholders. Do NOT assume #177-#181 will be the actual IDs — the next free ID after #153 is #154, so the eventual real numbers will almost certainly differ. Adjacent invented IDs (#154, #170-#174, #136, #180) need the same sweep.

---

## [C2] HIGH · dangling-reference · stale-unmarked-confirmed
**Topic:** Invented Codex #177 mapped to TWO unrelated concepts across research docs (Skill System Architecture vs Labyrinth-as-pipeline)
**A (research/cornerstone-settlement-design.md (Codex cross-reference table, §9)):** Codex #177 | Skill System Architecture — domain × ten + use-based progression precedent.
**B (research/soul-dna-architecture.md and research/true-names-and-false-labels.md):** Codex #177 = Labyrinth-as-pipeline.
**Fix:** Disambiguate the colliding placeholder ID. Since the Skill System Architecture and the Labyrinth-overlay/pipeline are distinct entities, assign them separate IDs (e.g., keep #177 = Skill System Architecture per cornerstone, reassign the Labyrinth-overlay to a new placeholder #179, or vice versa) and update both Path-2 docs (soul-dna-architecture.md §2 + cross-ref; true-names-and-false-labels.md §1/§2 + cross-ref) accordingly. Better: treat all three as provisional and add a one-line "(provisional ID — pending real Codex assignment; current canon tops out at #153)" note next to each #177/#178 citation so the placeholders are flagged until MCP Codex access returns and real numbers are assigned. No change needed to the cornerstone §9 table for duplication — it is not duplicated.

---

## [C3] HIGH · dangling-reference · stale-unmarked-confirmed
**Topic:** Codex #94 identity — Imago Dei Foundation (REFERENCE) vs 'Fantasy Register Discipline' (research docs)
**A (research/skill-system-design.md; research/cornerstone-settlement-design.md; research/skill-taxonomy-build.py (header)):** Codex #94 (Fantasy Register Discipline) | Prose register — keeps this doc's vocabulary out of prose. 'See prompts/magic_system.md and Codex #94 (Fantasy Register Discipline).'
**B (REFERENCE.md):** The Barrier — Imago Dei Foundation — Codex #94: created in God's image, that power was natural in Eden; after the Fall a barrier was placed over it; the System artificially bypasses this barrier.
**Fix:** In the three research docs, stop citing the prose-register rule as "Codex #94." Replace every "Codex #94 (Fantasy Register Discipline)" with a pointer to the actual authority — e.g. "See WRITING_RULES.md (fantasy-register rules / 14 hard bans) and memory feedback_fantasy_not_religious_register." Specifically: skill-system-design.md line 8 heading and line 10; cornerstone-settlement-design.md ~line 12; skill-taxonomy-build.py docstring lines 5 & 7. This frees the #94 ID for its sole canonical meaning (The Barrier — Imago Dei Foundation in REFERENCE.md). (Separately/optionally: drop or repoint the co-cited "prompts/magic_system.md" since that file/dir does not exist.)

---

## [C4] HIGH · memory-vs-canon · stale-unmarked-confirmed
**Topic:** Nate's HUD baseline color: green (REFERENCE Codex #11/#75, research/hud-design-spec.md) vs blue (memories, REFERENCE Late-Stage)
**A (REFERENCE.md (Codex #11, #75) and research/hud-design-spec.md):** Codex #11: 'briefly receives the standard blue interface (5 sec) before it degrades to two monochrome green arcs (Phase 1 Basic).' Codex #75: 'Phase 1: monochrome green, health/stamina only.' research/hud-design-spec.md (claiming to BE Codex #75) is built entirely on green ('Monochrome green | Base data | Phase 1+'; 'two curved lines like parentheses made of light'; Visual Language table assigns Nate = 'Green, amber, blue-green', System UI = 'Cold blue').
**B (codex_magic_visibility_split.md / codex_hud_visual_vocabulary.md / REFERENCE.md Late-Stage):** 'Nate's HUD: Monochrome blue (wireframe / blueprint-simile form). Not nature-green. Applied retroactively to Ch2-8 on 2026-04-14 (replaced prior green references).' Canonical prose: 'two faint blue arcs... monochrome and stubborn (ch02 L247 post-edit).' REFERENCE.md Late-Stage confirms 'Nate's HUD is blue wireframe.'
**Fix:** Propagate the 2026-04-14 green→blue retcon to the three unmarked green surfaces. (1) REFERENCE.md Codex #11 (L123): "two monochrome green arcs" → "two monochrome blue arcs (blue wireframe)"; append "(updated 2026-04-14: blue wireframe — see Magic Visibility & Color Split, L594)". (2) REFERENCE.md Codex #75 (L126): "Phase 1: monochrome green" → "Phase 1: monochrome blue (wireframe)". (3) research/hud-design-spec.md — highest priority, live top-down drafting ref that currently INVERTS the scheme: fix Visual Language table (L41) Nate green→blue wireframe and ensure System-UI row (L42) reads as blue distinguished by FORM not hue; convert all Phase 1A-1D and Color Language green references (L51, L76, L81, L86, L92, L98, L101, L147) to blue; add a dated top-of-file note "2026-04-14: Nate's baseline HUD is monochrome BLUE wireframe (was green); green references superseded." If a full rewrite is deferred, at minimum add a prominent SUPERSEDED banner at the top of hud-design-spec.md so a drafter is warned before reaching the green text.

---

## [C5] HIGH · memory-vs-canon · stale-unmarked-confirmed
**Topic:** External tell of an active System interface: faint blue glint behind the eyes (Codex #80) vs no external tell whatsoever (memories)
**A (REFERENCE.md (Codex #80, Screen Visibility Rules)):** 'All System interfaces are internal only — no physical light emitted. The only external tell is a faint blue glint behind the eyes.'
**B (feedback_blue_panels_internal.md / codex_system_screens_private.md):** feedback_blue_panels_internal.md (David Ch4 ruling 2026-04-14): 'There is NO visible blue glow, blue glint, or blue light in or behind the viewer's eyes that an outside observer can see... nate shouldn't notice blue in the eyes this is something that is completely internal to the viewer of the panel.' codex_system_screens_private.md: 'No one else can see another person's screen... It has no external display.'
**Fix:** Edit REFERENCE.md line 132 (Codex #80) to align canon with David's 2026-04-14 ruling. Replace "All System interfaces are internal only — no physical light emitted. The only external tell is a faint blue glint behind the eyes." with: "All System interfaces are internal only — no physical light emitted, and NO external tell of any kind (no glow, glint, or light in or behind the viewer's eyes). The interface is completely internal to the viewer; an outside observer perceives nothing. A character reading a panel is telegraphed only through behavior — unfocused eyes, a pause, gestures at empty air — never through visible light. (See memory: feedback_blue_panels_internal, David Ch4 ruling 2026-04-14; codex_system_screens_private.)"

---

## [C6] HIGH · mutually-exclusive · real-contradiction
**Topic:** Nate's HUD form: cockpit/fighter-pilot full-field assigned to Nate (REFERENCE) vs cockpit form Nate NEVER gets (memory)
**A (REFERENCE.md (Codex #1 & #11; Late-Stage 'HUD Visual Vocabulary' table)):** Codex #1 & #11: interface is 'a fighter-pilot HUD, not the standard blue screen.' Late-Stage table assigns: 'Cockpit | Multi-pane fighter-pilot wraparound | Nate (Phase 3+).' (research/hud-design-spec.md also frames the whole HUD as a 'fighter-pilot overlay.')
**B (codex_hud_visual_vocabulary.md):** Form E (Cockpit/Full-Field): 'System's full-deployment HUD... Nate's HUD never looks like this.' Nate's NEVER list: 'Panels (form D), cockpit (form E), polished reactor-core (form A rich version). These are System-user forms and Nate is anomaly.'
**Fix:** Fix the REFERENCE.md Late-Stage table to match the detailed form vocabulary, since the memory is the more specific, image-derived authority and REFERENCE.md's own "fighter-pilot HUD" was a prose metaphor over-literalized into a form row. In c:/Workbench/dev/forge-novel/REFERENCE.md line 608, remove Nate from the Cockpit row: change "| Cockpit | Multi-pane fighter-pilot wraparound | Nate (Phase 3+) |" to "| Cockpit | Multi-pane fighter-pilot wraparound | System users (full-deployment combat HUD) — NOT Nate |". (Optional same-pass cleanup: align line 605 Iris-compass phase label and the Scanner/reticle row with the memory's form-A-line-art-only rule.) Alternatively, if David actually intends Nate to graduate into a cockpit form at Phase 3+, the memory's three NEVER statements must be updated with a dated "Phase 3+ exception" marker — but absent that direction, treat REFERENCE.md as the stale side.

---

## [C7] HIGH · stale-unmarked · stale-unmarked-confirmed
**Topic:** Conduit Consequence Model — Codex #93/#10 body says drift = gradual power FADE / 'zero when selfish' vs locked model = stasis-not-decay (nothing atrophies)
**A (REFERENCE.md (Codex #93 body, Codex #10 body)):** Codex #93: '(2) Minor drift (pride, selfishness) → gradual power fade like a weakening signal. (3) Major violation → hard shutoff, breaker flips.' Codex #10: 'Output variable — exceeds maximum when aligned, zero when selfish.'
**B (feedback_conduit_power_doubt.md / project_forge_theology_unified_source.md / project_forge_skill_system_design.md / research/skill-system-design.md):** Opposition state = stasis, NOT decay. 'Gifts go silent but do not atrophy... nothing is lost, only overflow toggles.' Restoration through repentance reopens flow at the prior ceiling. 'Conduit opposition: stasis (not decay).'
**Fix:** Add an inline supersede marker to Codex #10's body. Change line 139 from "Output variable — exceeds maximum when aligned, zero when selfish." to "Output variable — exceeds maximum when aligned; overflow goes silent (NOT zeroed/decayed) when opposed. **Superseded by the 2026-04-23 Three-State Amplification Overlay (see Late-Stage section): opposition = stasis, not decay — nothing atrophies; flow returns at prior ceiling on realignment.**" Secondary (lower priority): add an inline "(superseded — see Late-Stage Three-State Amplification Overlay)" tag at Codex #93's body (line 79-80) so the remote supersede notice is discoverable from the Power-Systems section.

---

## [C8] HIGH · mutually-exclusive · stale-unmarked-confirmed
**Topic:** Tutorial macro-structure: flat 10-room linear run (Codex #96/#106/#107) vs 6-floor branching model (memories, REFERENCE Late-Stage, drafts)
**A (REFERENCE.md (Codex #96 Tutorial Room Structure; #106 Briarknight; #107 Room 10 Boss Fight; #104 Room 7; #105 Room 5-6)):** Codex #96: 'Safe Room staging + 10 combat rooms (Room 1 through Room 10 boss). One fight per room. Group split at Room 6. Boss room: Briarknight + adds.' #106: Briarknight 'took everything it learned from nine rooms.' #107: 'Room 10 Boss Fight.'
**B (project_forge_tutorial_structure.md / project_forge_tutorial_curriculum.md / REFERENCE.md Late-Stage / drafts/ch07 + ch10):** '6 floors total, spanning ~2 earth weeks. Early floors (1-2) multi-room — 2-3 combat rooms plus rest/crafting per floor; later floors (5-6) single bigger room. Within each floor, branching path choices.' REFERENCE Late-Stage restates '6 floors / ~2 Earth weeks' as 'Extends Codex #96.' Drafts: ch07 ends 'Floor 2 Access Available' / 'Floor 1 is done'; ch10-graduation says Briarknight 'wasn't anything the Tutorial had produced in nine rooms.'
**Fix:** In REFERENCE.md, mark the three room-model entries as superseded and align them to the 6-floor canon. Minimal: append to the Codex #96 heading/body "(SUPERSEDED by Late-Stage 'Tutorial Curriculum & Structure' — 6 floors / hybrid branching; room-numbering retired)"; same superseded note on #106 ("nine rooms" -> recast as "what it learned across the prior floors") and #107 ("Room 10 Boss Fight" -> Floor 6 graduation/evaluation capstone). Also change the Late-Stage Tutorial entry's label from "Extends Codex #96 (Tutorial Room Structure)" to "Supersedes Codex #96/#106/#107 (room topology)" so it matches the sibling "Supersedes Codex #93" pattern and stops mislabeling a replacement as an extension. If any current draft still uses literal "nine rooms"/"Room 10" boss language, reconcile to floor language during the next editorial pass.

---

## [C11] HIGH · numeric-spec · stale-unmarked-confirmed
**Topic:** Quick Stats category counts do not match their own listed ID lists (Game Mechanic 41-vs-46, Lore 50-vs-53)
**A (REFERENCE.md (Quick Stats, Game Mechanic row line 427, Lore row)):** Game Mechanic | 41 | [list expanding to 10,11,12,14,15,26,34,35,37,41,43,44,46,47,48,55,56,59,72,73,74,75,79,87,91,93,94,95,96,97,98,99,100,103,107,108,109,140-145,148,149,151,152,153]; Lore | 50 | [list].
**B (REFERENCE.md (same rows' ID lists, expanded)):** The Game Mechanic list expands to 46 distinct entries, not 41 (140-145 alone is 6 IDs). The Lore row claims 50 but lists 53.
**Fix:** Re-tally the Quick Stats table to match the listed IDs (or regenerate it from live forge-mcp). Minimal correction: Game Mechanic count 41 -> 48; Lore count 50 -> 51. Then reconcile the Total: corrected Count column sums to 10+6+48+2+3+51 = 120, which does not equal the asserted 153, so either (a) the Key IDs lists are themselves incomplete (missing ~33 entities the header counts) and need the missing IDs added, or (b) the Total 153 is stale. Recommend regenerating the whole table from the authoritative Codex so counts, ID lists, and total all agree, since three independent figures (per-row counts, expanded lists, and total) currently disagree.

---

## [C12] HIGH · numeric-spec · stale-unmarked-confirmed
**Topic:** Quick Stats Total 153 unsupported by its own category rows (rows sum to 112; 36 in-range IDs omitted, several fully written-up)
**A (REFERENCE.md (Quick Stats Total line 431; header lines 4-5)):** 'Total | 153' and header 'forge-mcp Codex — 153 active entities across all types.'
**B (REFERENCE.md (sum of the six Quick Stats category rows)):** Character 10 + Faction 6 + Game Mechanic 41 + Item 2 + Location 3 + Lore 50 = 112, not 153. By listed-ID counts (10+6+46+2+3+53) the table accounts for 120 distinct IDs spanning 1-153. 36 IDs in the 1-153 range (incl. #110-#136, #138, #146, plus written-up entries #86 Marcus Webb, #102 Josie, #106 Briarknight) appear in NO Quick Stats row. The Inspirations block (#19-25, #33, #62, #63) has no row either.
**Fix:** In REFERENCE.md Quick Stats (lines 425-431), reconcile the table. Minimal options: (a) regenerate the six category rows from the live forge-mcp Codex so the Counts sum to the Total; or (b) if 153 is the authoritative live headcount and the rows are a curated subset, change the Total cell to the actual row sum (112) and add a one-line note under the table, e.g. '*Category rows enumerate the curated subset transcribed here; the 153 figure is the live forge-mcp headcount — query forge-mcp for the full set.*' Either removes the unmarked 41-entity discrepancy. No story canon is affected.

---

## [C14] MEDIUM · numeric-spec · real-contradiction
**Topic:** Judge's Forge Codex entity ID: 'no Codex ID yet' (REFERENCE) vs #135 (memories)
**A (REFERENCE.md):** Judge — Blue Heeler (no Codex ID yet).
**B (feedback_rex_bond_bidirectional.md / project_narrator_voice.md):** 'Judge = Omega. Female. Blue Heeler (Australian Cattle Dog) — Forge Codex Entity #135.' project_narrator_voice.md repeats '#135' (line 82).
**Fix:** Resolve which side is true by querying forge-mcp Codex for entity #135 (what entity actually occupies that ID). Two outcomes: (a) If #135 is genuinely Judge in the live Codex, then REFERENCE.md is stale — update line 23 to "**Judge** — Codex #135" and add Judge to the Quick Stats Character row (key IDs + raise count 10→11, reconcile Total). (b) If #135 is some other entity or empty, then both memories invented the ID — strike "— Forge Codex Entity #135" from feedback_rex_bond_bidirectional.md line 63 and project_narrator_voice.md line 82, replacing with "(no Codex ID assigned yet)" to match canon. Until verified against forge-mcp, treat REFERENCE.md ("no ID yet") as authoritative per the project's authority order.

---

## [C15] MEDIUM · terminology-drift · stale-unmarked-confirmed
**Topic:** 'alpha' as a pack-role label — retired (WRITING_RULES) vs still asserted as current (REFERENCE Rex #64, memories)
**A (WRITING_RULES.md):** 'Retire "alpha" as a label. The pack model is correct (Genesis Stewardship, Codex #43), but "alpha" is dated science (the Schenkel captive-wolf study, since debunked). Prefer "Nate is Rex's person / they are pack." Internal-doc cleanup; never let "alpha" reach prose.'
**B (REFERENCE.md (Rex entry, Codex #64) / feedback_rex_bond_bidirectional.md / project_narrator_voice.md):** REFERENCE.md: 'Nate is Rex's only alpha — they are pack.' feedback_rex_bond_bidirectional.md builds its entire pack section on 'Nate = Alpha', 'Rex = Beta', 'Judge = Omega'; project_narrator_voice + WRITING_RULES voice table both tag Rex 'beta-pack' and Judge 'omega-pack.'
**Fix:** Execute the internal-doc cleanup WRITING_RULES.md already ordered. Minimal, non-destructive edits (preserve the pack-bond DESIGN, only retire the label):
1. REFERENCE.md line 21 — change 'Nate is Rex's only alpha — they are pack.' to 'Nate is Rex's person — they are pack. ("alpha" as a role label retired per WRITING_RULES.md 2026-05-01; pack model = Genesis Stewardship / Codex #43, not dominance.)'
2. feedback_rex_bond_bidirectional.md — reframe the 'Pack hierarchy' section from alpha/beta/omega to role-without-the-label (e.g. Rex = steady counselor/second; Judge = tension-breaking glue/youngest) and add the retired-term note.
3. project_narrator_voice.md — keep the voice characterizations but drop/annotate 'beta'/'omega' as register tags, or add the same retired-term note.
4. WRITING_RULES.md voice table — relabel 'beta-pack register' / 'omega-pack register' to 'counselor register' / 'jester-peacemaker register' (or keep but footnote that these are descriptive, not the retired dominance terms), since the retiring doc shouldn't keep the derivatives live.
None of these touch prose, so no audiobook/TTS risk.

---

## [C16] MEDIUM · numeric-spec · stale-unmarked-confirmed
**Topic:** Two-Faculty Model attributed to Codex #95 (research docs) vs #95 = System Dual Interface (REFERENCE); model canonically tied to #16/#94
**A (research/skill-system-design.md (line 553); research/skill-taxonomy-build.py (line 9)):** skill-system-design.md: '| Codex #95 (System Dual Interface) | Two-Faculty Model |'; skill-taxonomy-build.py: 'Faculty: analytical / relational / both / "" — per Codex #95 Two-Faculty Model.'
**B (REFERENCE.md):** Codex #95 is System Dual Interface ('Blue screen redesigned as character sheet only...'). The Two-Faculty Model is an un-numbered 2026-04-19 Late-Stage note that 'Extends Codex #16 (Five-Layer Cosmology) and #94 (Imago Dei Foundation)' — i.e., #16/#94, never #95.
**Fix:** Two one-token edits, no canon change needed. (1) research/skill-system-design.md line 553: change `| Codex #95 (System Dual Interface) | Two-Faculty Model |` to `| Codex #94 (Imago Dei Foundation) + #16 (Five-Layer Cosmology) | Two-Faculty Model |` (matching REFERENCE.md's 'Extends #16 and #94'). Note #94 already appears in the row above (line 552) as 'Fantasy Register Discipline' — that title is itself suspect vs REFERENCE.md which calls #94 'Imago Dei Foundation', so verify #94's true title against the live Codex while fixing. (2) research/skill-taxonomy-build.py line 9: change `per Codex #95 Two-Faculty Model` to `per the Two-Faculty Model (REFERENCE.md, extends Codex #16/#94)`. Once the Two-Faculty Model is backfilled to forge-mcp with its own Codex ID, repoint both references to that ID.

---

## [C19] MEDIUM · memory-vs-canon · stale-unmarked-confirmed
**Topic:** Cohort member classes: nine listed 'TBD' in REFERENCE roster vs fully assigned in cohort memory and hard-baked into drafts/cast.json
**A (REFERENCE.md (Late-Stage 'Tutorial Cohort Roster — 12 Survivors')):** Ana Torres | TBD class; Walt Keane | TBD class; Sam Hargrove | TBD class; Kyle Greene | TBD class; Mack Turner | TBD class; Dr. Martin Voss | TBD class — academic; Pete Bowman | TBD class; Heather Kim | TBD class; Isabel Wu | TBD class.
**B (project_forge_tutorial_cohort.md (+ drafts, audiobook/scripts/cast.json, VOICE-CAST.md)):** Ana Torres | Healer; Walt Keane | Smith/Crafter; Sam Hargrove | Guardian; Kyle Greene | Berserker; Mack Turner | Ranger/Scout; Dr. Martin Voss | Mage/Scholar; Pete Bowman | Pathfinder; Heather Kim | Ward Mage; Isabel Wu | Alchemist. Classes hard-baked into cast.json/VOICE-CAST.md (e.g., 'Sam Hargrove (Guardian),' 'Kyle Greene (Berserker, MSG-foil)').
**Fix:** Backfill REFERENCE.md lines 538-546: replace the nine "TBD class" cells with the locked classes from project_forge_tutorial_cohort.md — Ana Torres=Healer, Walt Keane=Smith/Crafter, Sam Hargrove=Guardian, Kyle Greene=Berserker, Mack Turner=Ranger/Scout, Dr. Martin Voss=Mage/Scholar (academic), Pete Bowman=Pathfinder, Heather Kim=Ward Mage, Isabel Wu=Alchemist. (Authority order makes REFERENCE.md the source of record, so the fix is to bring it up to the manuscript's already-locked state, not to walk the drafts back.) Optionally add a one-line "(classes locked 2026-04-18; see project_forge_tutorial_cohort.md)" provenance note so the two stay synced.

---

## [C20] MEDIUM · stale-unmarked · stale-unmarked-confirmed
**Topic:** Camera voice retired/folded into Storyteller (2026-04-19) vs still mandated as distinct pullaway voice + treated as live voice with own comedy dial
**A (project_narrator_voice.md):** 'Narrator and Camera collapsed into a single Storyteller voice on 2026-04-19... DEPRECATED — Camera voice (Jenny)... no longer assigned after the Storyteller collapse.'
**B (project_forge_tutorial_structure.md / feedback_humor_punch_up.md / feedback_prose_must_earn_its_place.md):** tutorial_structure: 'Camera voice (not Narrator) handles pullaways so three-voice discipline holds (project_narrator_voice).' humor_punch_up: per-voice matrix lists 'Camera | 4 | Pointed, specific, stacked punchlines' AND 'Narrator | 4-5' as two distinct live voices; 'Camera with bite' cited as a current target. prose_must_earn echoes 'a Camera sentence,' 'Voice redundancy in Camera.'
**Fix:** Propagate the 2026-04-19 Storyteller collapse into the three stale files, mirroring how REFERENCE.md L560 was already updated. (1) project_forge_tutorial_structure.md L13: change "Camera voice (not Narrator) handles pullaways so three-voice discipline holds" to "the Storyteller handles pullaways in physical-zoom mode (Camera and Narrator folded into one voice 2026-04-19, see project_narrator_voice)"; update L12/L18 "Camera pullaways"/"Camera lifts" to "Storyteller pullaways" and fix the header description; add a one-line dated note: "Updated 2026-04-19: former Camera role is now the Storyteller's physical-zoom mode." (2) feedback_humor_punch_up.md: merge the Camera (L25) and Narrator (L27) matrix rows into a single "Storyteller | 4-5" row (physical-zoom mode tightens toward Dial 4); update L36-37 and L65 "Camera" references to "Storyteller (physical-zoom)"; revise the description field; add a dated supersede note. (3) feedback_prose_must_earn_its_place.md L16 and L35: change "a Camera sentence" / "Voice redundancy in Camera" to "a Storyteller physical-zoom sentence" / "Voice redundancy in Storyteller physical-zoom mode." If editing is undesirable, at minimum add a "SUPERSEDED 2026-04-19: Camera folded into Storyteller — see project_narrator_voice" banner to each of the three files.

---

## [C21] MEDIUM · stale-unmarked · stale-unmarked-confirmed
**Topic:** ElevenLabs production model described as three-voice (Irish Narrator + neutral Camera + Nate) in current master-tiebreaker file vs full-cast Storyteller model
**A (feedback_audiobook_is_primary_medium.md):** 'The ElevenLabs three-voice production (Irish Narrator, neutral Camera, Sam-Elliott Nate)... project_narrator_voice — three-voice system depends on this rule.'
**B (project_narrator_voice.md):** 'The novel uses a full-cast voice system... This replaces the earlier three-voice Narrator/Camera/Nate model — Narrator and Camera collapsed into a single Storyteller voice on 2026-04-19.'
**Fix:** Surgically update the two stale voice-model references in feedback_audiobook_is_primary_medium.md (do NOT touch the tiebreaker rule it carries, which is still valid). Line 9: change "The ElevenLabs three-voice production (Irish Narrator, neutral Camera, Sam-Elliott Nate)" to the current full-cast/Storyteller model, e.g. "The ElevenLabs full-cast production (Storyteller — Irish woman omniscient-with-zoom — plus Sam-Elliott Nate and per-character voices; Narrator+Camera collapsed into Storyteller 2026-04-19, see project_narrator_voice)". Line 25: change "project_narrator_voice — three-voice system depends on this rule" to "project_narrator_voice — full-cast voice system depends on this rule". This removes the unmarked-stale description while preserving the master-tiebreaker principle and the valid cross-reference.

---

## [C24] MEDIUM · numeric-spec · real-contradiction
**Topic:** Group split location: Room 6 (Codex #96, drafts) vs Floor 4 (curriculum memory, cast.json)
**A (REFERENCE.md (Codex #96)):** 'Group split at Room 6.'
**B (project_forge_tutorial_curriculum.md (+ project_forge_tutorial_cohort.md, cast.json)):** 'Floor 4 — Choice practice... Combat shape: Branching rooms; group splits and reunites... Camera pullaway to foil group's path.' Mack Turner tagged 'Floor 4 branch anchor' in cohort memory and cast.json.
**Fix:** Reconcile the two coordinate systems with one authoritative mapping, then update whichever side is wrong. Minimal version: in REFERENCE.md, where the 6-floor curriculum "Extends Codex #96," add an explicit room-to-floor map (e.g., "Rooms 1-10 distribute across the 6 floors; the designed group split = Room 6 = Floor 4"). Then fix the topology mismatch: either (a) change the curriculum/structure memories so Floor 4 is a one-time performance-sorted split that does NOT reunite (matching drafted canon), and drop "group splits and reunites" / per-floor branching; or (b) if reunite-then-resplit is intended, update Codex #96 and ch08 accordingly. Also retag Mack Turner consistently (cohort memory + cast.json) to the reconciled split location. If C8 (the broader room-vs-floor geometry conflict) is being fixed separately, fold C24 into that fix rather than patching it independently.

---

## [C25] MEDIUM · numeric-spec · stale-unmarked-confirmed
**Topic:** Phase 2 HUD palette: green-base / blue-green-environmental four-color ladder (Codex #75, design doc) vs blue-baseline + amber-threat + gold-anomaly (memories)
**A (REFERENCE.md (Codex #75) + research/hud-design-spec.md):** Codex #75: 'Phase 2 (Ch9+): green base, amber threats, blue-green environmental, gold divine architecture.' (Mirrored in hud-design-spec.md Color Language table: monochrome green base, amber threat, blue-green environmental, all Phase 2+.)
**B (codex_hud_visual_vocabulary.md / codex_magic_visibility_split.md):** Nate baseline = monochrome blue; threat indicator = AMBER; anomaly flares gold/white. No 'green base' or 'blue-green environmental' layer exists in the current color memories.
**Fix:** Add a dated reconciling note on the SOURCE A side pointing to the 2026-04-14 green→blue retcon, and correct the stale base color. Minimal edits: (1) In REFERENCE.md Codex #75, change 'green base' to 'blue/wireframe base' and replace 'blue-green environmental' with an environmental tier that doesn't presume a green base, then append '(base color updated 2026-04-14: Nate's HUD baseline is monochrome blue wireframe, not green — see codex_magic_visibility_split.md / Magic Visibility & Color Split appendix).' Also fix Codex #11's 'two monochrome green arcs' to 'two monochrome blue arcs.' (2) In research/hud-design-spec.md, add a note under the Color Language table: 'NOTE (2026-04-14 retcon): Nate's HUD baseline is monochrome BLUE wireframe, not green; amber threat and gold divine tiers stand; the green-base / blue-green-environmental ladder below is superseded.' The amber-threat and gold-divine rows need no change since both sources already agree on them.

---

## [C26] MEDIUM · numeric-spec · stale-unmarked-confirmed
**Topic:** Phase 2 / amber-threat timing: gated Ch9+ (Codex #75, design doc) vs amber already canonical prose in Ch8 (memories)
**A (REFERENCE.md (Codex #75) + research/hud-design-spec.md):** Codex #75: 'Phase 2 (Ch9+): green base, amber threats...' — amber threats gated to Phase 2 = Ch9 and later. hud-design-spec.md: amber is Phase 2A, triggered 'first time outside the Tutorial,' Ch9-11.
**B (codex_hud_visual_vocabulary.md / codex_magic_visibility_split.md):** 'Threat indicator — Color: AMBER (Ch 8 canon: "Not wireframe. Not panel. Amber.")'; 'Amber as threat-indicator category... (ch08 L447 post-edit).'
**Fix:** Fix the two memory files, not the canon. In codex_hud_visual_vocabulary.md L125-127 and codex_magic_visibility_split.md L104-105: (1) remove/correct the phantom citation — the quote "Not wireframe. Not panel. Amber." does not exist at ch08 L447 (or anywhere in ch08-spike-draft01.md); (2) stop labeling Ch8's amber as the Phase-2A "threat-indicator category." If a "Not wireframe. Not panel. Amber." line is genuinely wanted, it belongs in Ch9+ per Codex #75 / hud-design-spec Phase 2A; if the intent was only to document the early amber PROCESSING tag (Ch4/Ch8), re-label it as such so it no longer reads as an in-Tutorial deployment of the Ch9+ amber threat indicator. This dissolves the apparent Ch8-vs-Ch9 seam.

---

## [C30] MEDIUM · numeric-spec · stale-unmarked-confirmed
**Topic:** Brigid omniscient-register style value disagrees across the two 'locked' production-settings files (0.10 vs 0.15)
**A (project_narrator_voice.md):** Production settings (locked 2026-04-10): stability=0.50, style=0.10, speed=0.85.
**B (feedback_audiobook_voice_routing.md (+ WRITING_RULES.md line 23)):** storyteller_omniscient (slow/literary): stability 0.50, style 0.15, speed 0.85.
**Fix:** In project_narrator_voice.md line 15, update the Storyteller production block to reflect the two-register split (or mark the single-block value historical). Replace the lone "style=0.10" with the register-aware spec and a pointer: e.g. "Production settings: model=eleven_v3, similarity_boost=0.75, use_speaker_boost=true. Two registers (see feedback_audiobook_voice_routing.md + scripts/cast.json as authoritative): storyteller_omniscient = stability 0.50 / style 0.15 / speed 0.85; storyteller_narrator = stability 0.30 / style 0.35 / speed 1.05." First confirm scripts/cast.json's actual style value (0.10 vs 0.15) and make all three sources (memory A, memory B, cast.json, WRITING_RULES.md) agree on it.

---

## [C31] MEDIUM · stale-unmarked · stale-unmarked-confirmed
**Topic:** Storyteller frequency '3-4+ per chapter' count — retired but still asserted as live fact
**A (feedback_narrator_frequency.md (+ WRITING_RULES.md line 35)):** 'Since the 2026-04-19 collapse... the previous "3-4+ per chapter" floor is obsolete.' WRITING_RULES.md: 'The "3-4 per chapter" count is RETIRED.'
**B (feedback_humor_punch_up.md):** Related-memories block: 'feedback_narrator_frequency.md — Narrator appears 3-4+ times per chapter; this memory sets the intensity for those appearances.'
**Fix:** In C:\Users\dblon\.claude\projects\c--Workbench-dev-forge-novel\memory\feedback_humor_punch_up.md, line 77, replace the stale count with the current weaving framing. Change:
'- `feedback_narrator_frequency.md` — Narrator appears 3-4+ times per chapter; this memory sets the *intensity* for those appearances'
to:
'- `feedback_narrator_frequency.md` — Storyteller is woven throughout each chapter (the old "3-4+ per chapter" floor is RETIRED post Narrator+Camera collapse); this memory sets the *intensity* of those appearances'
This removes the asserted-as-live retired count while preserving the legitimate cross-link and the intensity relationship.

---

## [C41] LOW · terminology-drift · real-contradiction
**Topic:** 'technique' lumped with 'sub-skill' as a retired earlier-draft term (skill-system memory) vs still-valid prose register (every other source)
**A (project_forge_skill_system_design.md (line 21)):** '"Sub-skill" and "technique" were earlier drafts; Ability is the locked term.'
**B (feedback_skill_vs_ability_terminology.md / research/skill-system-design.md / REFERENCE.md):** feedback_skill_vs_ability_terminology.md: 'Lowercase "technique" is acceptable prose vocabulary for low-register/mundane/no-HUD actions'; REFERENCE.md: 'Lowercase technique is OK in mundane prose register'; skill-system-design.md: '"Technique" is acceptable prose vocabulary for low-register / mundane / no-HUD actions.'
**Fix:** Edit project_forge_skill_system_design.md line 21. Replace: '"Sub-skill" and "technique" were earlier drafts; Ability is the locked term.' with: '"Sub-skill" was an earlier draft (retired); "Ability" is the locked leaf-name for System-surfaced named moves. "Technique" is retired only as a taxonomy leaf-name — lowercase "technique" remains valid prose vocabulary for low-register/mundane/no-HUD actions (see feedback_skill_vs_ability_terminology.md, REFERENCE.md, research/skill-system-design.md).' No canon edits needed; the four governing sources already agree — only this one memory line overstates the retirement.

---

## [C43] LOW · stale-unmarked · stale-unmarked-confirmed
**Topic:** Named cohort count: '~8-10' with TBD priorities (structure memory) vs locked 12-survivor named roster (cohort memory, REFERENCE, drafts)
**A (project_forge_tutorial_structure.md):** 'Named-character cohort of ~8-10 (Josie established; contract-signing foil-warrior, contract-refusing healer, named crafter as priorities).'
**B (project_forge_tutorial_cohort.md + REFERENCE.md (Late-Stage roster)):** '12 survivors at Tutorial graduation [12 named survivors locked]... User locked 2026-04-18; Nate's Tutorial pocket survivor roster is locked: [12 names].' Drafts confirm 12 ('twelve survivors,' 'contact list, twelve names long' in ch10).
**Fix:** Update project_forge_tutorial_structure.md line 18: change "Named-character cohort of ~8-10 (Josie established; contract-signing foil-warrior, contract-refusing healer, named crafter as priorities)" to "Named-character cohort of 12 survivors at graduation (locked roster in project_forge_tutorial_cohort.md; foil-warrior = Kyle Greene, contract-refusing healer = Ana Torres, named crafter = Walt Keane)." Add a one-line cross-reference to project_forge_tutorial_cohort.md so the two same-date memories stay synced.