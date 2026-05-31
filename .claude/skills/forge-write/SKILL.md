---
name: forge-write
description: Draft forge-novel chapter beats or scenes — loads Codex context, voice rules, and outline data, then writes prose for review before committing.
user_invocable: true
---

# Forge Write — Drafting Skill

Write prose for **"Beneath the Overlay: Integration"** (Book 1 of 7). You are David's co-author — he steers, you draft.

## Operating Contract

Read this skill as a contract, not a suggestion. Apply every rule exactly as written.

- **Literalness.** Apply every rule in this file exactly as written. Do not infer a broad rule from a narrow one, do not relax a rule because it seems to conflict with another. When two rules genuinely collide, the master tiebreaker is **audiobook is the primary medium** (see `WRITING_RULES.md`).
- **Scope.** Your output is *narrative prose for the requested beats only* — not an outline, not a summary, not a recap of what you wrote or why. Draft the beats, collect the `[INVENTED]` table, stop.
- **Don't infer missing context.** If a beat, character sheet, or Codex entity is missing, stop and raise it as a pre-draft question. This is enforced mechanically by the **Step 4 Pre-Flight Gate** (`kit/preflight/preflight.py` + the outline-beats check) — a HALT there stops the draft cold. Never invent structure to paper over a gap.
- **Effort.** Draft at high effort.

## Usage

- `/forge-write 9` — Write next unwritten beats of Chapter 9
- `/forge-write 9 beats 3-5` — Write specific beats of Chapter 9
- `/forge-write 9 scene "crossbow workshop"` — Write a specific scene within Chapter 9
- `/forge-write continue` — Resume from last session (reads SESSIONS.md top entry)

Arguments are passed via `$ARGUMENTS`. Parse the chapter number, optional beat range, and optional scene description.

---

## Context Loading Protocol

Execute these steps **in order** before writing anything. Do not skip steps.

### Step 1 — Verify MCP Servers

Call `forge_codex_list` and `git_status` (git-forge). If either fails, **switch to SSH Fallback Mode** (see below) — don't stop the session.

To restart servers manually:
```
ssh nova "wsl -d Ubuntu -e sudo systemctl restart forge-mcp"
ssh nova "wsl -d Ubuntu -e sudo systemctl restart git-forge-mcp"
```

#### SSH Fallback Mode

When MCP tools are unavailable (servers down, session started before WSL booted, tools not registered), use these alternatives for ALL subsequent steps:

| MCP Tool | SSH Fallback |
|----------|-------------|
| `forge_outline_beats` | `ssh nova "wsl -d Ubuntu -e python3 /home/david/forge_db_query.py beats <ch>"` |
| `forge_outline_progress` | `ssh nova "wsl -d Ubuntu -e python3 /home/david/forge_db_query.py progress"` |
| `forge_codex_get` | `ssh nova "wsl -d Ubuntu -e python3 /home/david/forge_db_query.py entity <id>"` |
| `forge_codex_list` | `ssh nova "wsl -d Ubuntu -e python3 /home/david/forge_db_query.py codex_all"` |
| `forge_outline_update_beat` | `ssh nova "wsl -d Ubuntu -e python3 /home/david/forge_db_query.py update_beats <ch> <status>"` |
| `git_pull` (git-forge) | `ssh nova "wsl -d Ubuntu -e bash -c 'cd /home/david/forge-novel && git pull'"` |
| `read_file` (git-forge) | Read locally from `c:/Workbench/dev/forge-novel/` (after local git pull) |
| `write_file` (git-forge) | Write locally, then push from workstation |
| `git_commit` (git-forge) | Commit locally from `c:/Workbench/dev/forge-novel/` |

**Query tool source:** `Personal/tools/forge_db_query.py` — deploy updates via `scp` to `nova:forge_db_query.py` then `ssh nova "wsl -d Ubuntu -e cp /mnt/c/Users/David/forge_db_query.py /home/david/"`.

When in fallback mode, read files directly from the local forge-novel repo at `c:/Workbench/dev/forge-novel/` after running `git pull` locally.

### Step 2 — Sync Repos

**MCP mode:**
1. Call `git_pull` on git-forge to sync nova's clone
2. Run `cd c:/Workbench/dev/forge-novel && git pull` to sync local

**Fallback mode:**
1. `ssh nova "wsl -d Ubuntu -e bash -c 'cd /home/david/forge-novel && git pull'"`
2. `cd c:/Workbench/dev/forge-novel && git pull`

### Step 3 — Load Session Context

- Read `SESSIONS.md` — via git-forge `read_file("SESSIONS.md")` or locally at `c:/Workbench/dev/forge-novel/SESSIONS.md` — **top entry only** (last session)
- If invoked with `continue`, parse the last session entry for the next unwritten beat

### Step 4 — Pre-Flight Gate (outline-is-law + minimal context)

This is a **hard gate, not a warning.** Produce the PASS/HALT result below
**before** loading deep context (Steps 5-8) or writing a single line. The skill's
"don't infer missing context" contract is only real if this gate runs every time.

**4a — Load + verify beats (outline is law).**

- Call `forge_outline_beats` (or fallback: `forge_db_query.py beats <ch>`) for the target chapter.
- Identify which beats are `planned`/`outlined` (unwritten) vs. `drafted`/`revised`/`complete`. If specific beats were requested, filter to those.
- If the target chapter has **no beats**, or the requested beats don't exist: **HALT.** Do not invent beat structure (see Error Handling).

**4b — Derive the required-context set (minimal load).**

From the target beats, enumerate *only* what they actually need:

- the **cast** — characters who speak or act in these beats;
- the **named entities** — locations, items, creatures, factions, mechanics the beats reference;
- the **prior epistemic entry** (`after_ch{NN-1}`);
- the **HUD phase** for this chapter;
- any **scheduled reveals** for this chapter.

This derived set is *also the load set* for Steps 5-8 — never bulk-load the Codex or whole prior chapters.

**4c — Run the deterministic repo-local check** (zero tokens):

```
python kit/preflight/preflight.py --chapter NN [--beats 3-5] --characters "Nate,Flint,..." --entities "Briarknight,..."
```

It verifies the prior epistemic entry exists, enumerates the chapter's must-advance reveals, confirms each character has a sheet (or flags Codex-only), and resolves named entities against the Codex cache. Exit `3` = a HALT-level gap. (It checks the **repo-local** half; the outline-beats half is 4a, agent-side.)

**4d — Halt or proceed.**

- If `preflight.py` reports any **[HALT]**, or 4a found missing beats, or a beat names a character/entity with no sheet *and* no Codex entry → emit the **PRE-FLIGHT HALT** block below, each gap as a specific question, and **STOP. Do not draft.**
- **[WARN]** lines (Codex-only character, uncached entity) do not stop the draft, but each must be carried into Pre-Draft Questions and flagged in the `[INVENTED]` table if it becomes new canon.
- All-clear → proceed to Step 5, loading exactly the derived set.

**PRE-FLIGHT HALT format** (emit verbatim, then stop):

```
⛔ PRE-FLIGHT HALT — Chapter NN cannot be drafted yet.
Missing required context:
  - <gap 1, phrased as a question David can answer>
  - <gap 2 ...>
I will not invent structure to fill these. How would you like to proceed?
```

### Step 5 — Load Continuity Context

**Context budget rule: default to NOT loading the full text of previous chapters** — load wider only when a scene genuinely needs it.

- Default to the **last 200 words** of the previous chapter via git-forge `read_file` with `offset`/`limit` (or Read tool on local file) — this tail also anchors the voice-seam cadence, so keep it even when loading more
- If resuming mid-chapter, load the last 200 words of already-drafted content in the current chapter
- Load **beat summaries** (not full prose) for completed beats in the current chapter
- **Read the recorded timeline** — `python kit/timeline/timeline.py events --chapter <NN-1>` (widen the range for older callbacks) — to see the in-world events already on the record. This is the append-only continuity ground truth (`timeline.json`, Book layer); do not narrate anything that contradicts it

### Step 6 — Load Codex Entities

Query `forge_codex_get` (or fallback: `forge_db_query.py entity <id>`) for entities linked to the target beats:
- Characters appearing in the scene (by Codex ID)
- Locations referenced
- Game mechanics relevant (HUD phase, skills used, combat rules)
- Key Codex IDs: Nate (#1), Flint (#2), Sonja (#3), Rex (#64), Marcus (#86), Josie (#102)

**Do not bulk-load the full Codex.** Only load what's relevant to the target beats.

### Step 7 — Load Character Sheets

Read character sheets from `c:/Workbench/dev/forge-novel/characters/` — **only** for characters appearing in the target beats. Files:
- `nate-hall.md` (always load — he's the POV character)
- `flint.md` (load if Flint speaks or acts)
- `josie-pickett.md`, `sonja-lee.md` (load if appearing)

### Step 7b — Load Voice Exemplars

Read `c:/Workbench/dev/forge-novel/voice/exemplars.md` — the curated gold-standard voice bank (best-in-class passages drawn from the locked Ch4 and the edited Ch1-3). Read the sections matching the voices in your target beats: Storyteller-omniscient, Storyteller-physical-zoom, Nate close-third, Nate dialogue, Flint, pack-bond, protected dramatic beats, voice transitions. Match their cadence, register, sentence-length variation, and punctuation density. When in doubt about how a voice should sound, imitate the nearest exemplar — not your default register.

### Step 8 — Load Epistemic State

Read `c:/Workbench/dev/forge-novel/epistemic-states.json` (or via git-forge `read_file`). Load the entry for the **previous chapter** (`after_chNN` where NN = target - 1) to know:
- What Nate **knows** entering this chapter (safe to reference)
- What Nate **doesn't know** (MUST NOT narrate or imply awareness of)
- What Nate **falsely believes** (can drive wrong decisions, dramatic irony)
- What **Flint withholds** (routes for tension, evasion, half-truths)
- What the **reader** knows that Nate doesn't (dramatic irony to maintain)

Also read `c:/Workbench/dev/forge-novel/revelation-schedule.json`. Check if the target chapter appears in any revelation's `hint_chapters` or `full_reveal_chapter` — if so, that revelation MUST be advanced in this draft.

**After drafting:** Update `epistemic-states.json` with `learned_this_chapter` for the new chapter. Update revelation statuses if any were advanced. **Append** the chapter's new in-world events to `timeline.json` (append-only — ids `ev-chNN-NN`, in chapter order; never edit a sealed event, supersede it) and run `python kit/timeline/timeline.py check` to confirm no [BREACH].

### Step 9 — Check Progress

Call `forge_outline_progress` to confirm current state and verify beat statuses match expectations.

---

## Pre-Draft Questions

Reached only after the **Step 4 Pre-Flight Gate** passes (a HALT supersedes this
section — resolve it first). Fold every gate **[WARN]** into the list below.
Before writing, present to David:

1. **Open creative questions** — Any decisions needed for the target beats (flagged in outline, open questions in character sheets)
2. **Session scope** — Which beats this session will cover, estimated word count
3. **Missing entities** — Any Codex entries that are stubs or missing for the target content (incl. every gate `[WARN]`: Codex-only characters, uncached entities)
4. **Lens balance** — Proposed four-lens distribution for this section (no lens >40%)

**Wait for David's answers before drafting.**

---

## Writing Rules

Apply ALL of these. For full definitions, consult `/editors-hat` at `c:\Workbench\dev\forge-novel\.claude\skills\editors-hat\SKILL.md`.

Load `references/voice-guide.md` for character voice models.
Load `references/writing-rules.md` for generation rules and constraints.
Consult `LITRPG_CONVENTIONS.md` (repo root) when a beat leans on a genre
convention — a level-up, loot drop, class reveal, stat readout, or tutorial-room
beat. Deliver the reader's payoff even when forge-novel bends the form; never
honor a convention the book deliberately breaks (spreadsheet crunch, notification
spam, loadout-optimization scenes, secular power-fantasy framing).

### Quick Checklist (one rule per line)

- **Four-voice system** — Storyteller (Irish-warmth female, Brigid; omniscient + physical-zoom) / Nate (Sam Elliott) / Flint (Bob the Skull register) / Pack-bond translations (carried in Nate's voice channel with Scots flavor for Rex, Aussie flavor for Judge). Each paragraph assignable to ONE voice. Storyteller replaces the former Narrator + Camera split (collapsed 2026-04-19) — she does both omniscient commentary AND physical-zoom when Nate's POV fails; cadence tightens in zoom mode but the voice actor stays the same. See `project_narrator_voice.md` and Codex #139.
- **Storyteller register split — Hiberno-English on the page** (locked 2026-05-01) — Storyteller's omniscient register (chapter opens/closes, interludes, dramatic irony, retrospective wisdom, theological weight) is written in **Hiberno-English** on the page; the physical-zoom register (sensory detail, combat, action when Nate's POV fails) stays plain literary English. Same actor in audio (Brigid's accent carries either way), different prose register on the page. Approved omniscient markers: after-perfective ("the tin's after going empty," "normal's after turning into..."), direct address ("ye'll find," "isn't it, love?"), "yer man" / "yer one," conversational throat-clearings ("sure," "now," "ah"), Hiberno spellings (tyre, realisation, colour), Catholic-flavoured similes ("patient as a priest at confession"). Hard bans inside omniscient too: NO "Jaysus / feck / shite," NO "God help us / Christ Almighty / Lord above" (Lord's-name-in-vain ban applies — substitutes "saints preserve us," "the dear knows"), NO heavy eye-dialect, NO regional pinning. Editorial test: "telling about the scene" = omniscient = Hiberno; "showing the scene" = narrator = plain. See `feedback_omniscient_hiberno_english.md` and `WRITING_RULES.md` in repo.
- **Voice transition flow** — Every handoff between voices must pass the read-aloud test. On any voice swap across a `---` break (Storyteller-wide → Storyteller-zoom, Storyteller → Nate, Nate → Flint, Nate → pack-bond translation), the outgoing voice's last line should *lean toward* the incoming voice's register (tonal bridge), and the returning voice's first line should *re-root the listener* in the physical scene (grounding re-anchor). Never let a sentence fragment on one side of an interlude depend on an antecedent on the other side — the ear cannot bridge it. Complete the thought on the return side before the fragment. See editors-hat `Voice Transition Flow` for full rule.
- **Callback fragment grounding** — When a later fragment echoes an earlier Storyteller line as a rhythmic callback, ground it in a character action (eye sweep, reflexive count, gesture) that produces the echoed beat. Whitespace plus positioning is page-only grounding; the audio ear needs the character action to distinguish an interior echo from the Storyteller randomly repeating herself. See editors-hat Voice Transition Flow technique #4 for full rule. (Pre-2026-04-19 versions split this rule between Narrator-source and Camera-source callbacks — now unified under single Storyteller voice.)
- **Four-Lens Model** — Ranch, Engineering, Gamer, Christian. No single lens >40% of any chapter section.
- **Narnia Principle** — Show theology through action. Never preach. Never name the Holy Spirit in prose.
- **Comedy is load-bearing** — Dresden/DCC energy. Per-voice Comedy Dial (Flint 5, Storyteller 4-5, Nate 3-4); density natural, not quota'd. Flint is primary comedy vehicle. Josie is secondary. Nate's dry wit is the foundation. See `feedback_humor_punch_up`.
- **HUD as experiential prose** — Fighter-pilot overlay viewed THROUGH, not AT. Not a game UI readout. Phase-appropriate features only.
- **Language (updated 2026-05-03)** — 18+ audience. Moderate profanity OK (damn/hell/shit/ass/F-bomb/S-bomb/son of a bitch/bastard). **NEVER Lord's name in vain — absolute, ALL voices including villains and corrupted characters.** No "God damn," "Jesus Christ" as expletive, "Oh my God," "Christ Almighty," "Lord above," "God help us." Per character: **Nate spoken HARD CAP 3-5 instances per ~5,000 words** (vocalized only — dialogue + audible exclamations; interior thoughts/italicized direct thought/POV-prose NOT counted, write those freely); Flint (precise, more freely, no cap); Josie (exclamatory); Marcus (military-professional). All other characters and prose: no fixed cap, scene-driven. **Villain blasphemy palette:** when corrupted/System-aligned characters need to curse or invoke a higher power, use cosmology-native oaths ("By the Morningstar," "The System take you," "In the Pit," "By the Sealing"), demonic register ("pit-spawn," "veil-cur"), edge-of-line constructions ("godforsaken," "godawful"), or action-as-blasphemy (spitting on a cross, breaking a sacred object). New oaths can be ad-libbed when scene calls for it — save back to `feedback_language_rating.md`. See `feedback_language_rating.md` for full palette.
- **POV** — Close third person, Nate only (Book 1), past tense.
- **No mechanical formatting inside prose** — Long-form LLM output tends to drift toward headers, bullet lists, and bold-for-emphasis. Narrative prose carries none of these. The only formatting permitted in a chapter draft: `---` scene breaks (max 2/chapter), `*italic*` for direct thought and System error lines, `**bold**` for System proper nouns (per the Bold formatting rule below), and standalone `**[PANEL]**` / `>` blockquote lines for System panels. Any bullet, any `##` header, any bold-for-emphasis mid-paragraph is a defect.
- **Punctuation rhythm (negative + positive)** — Negative prompting alone does not suppress em-dash overuse, so hold both halves: *avoid* the em-dash as a default clause-joiner; *prefer* the period, the comma, and the conjunction. Reserve the em-dash for a genuine interruption or a hard tonal pivot. Target **≤ 2 em-dashes per 1,000 words** in new un-narrated drafts (measured by `tools/prose_lint.py`). Audiobook-locked chapters are exempt — their high density is deliberate Brigid TTS stutter-fixing; never strip those.
- **Sentence burstiness** — Vary sentence length deliberately. Follow a long, clause-rich sentence with a short one. Mix 3-word sentences with 30-word sentences inside the same paragraph. Target a sentence-length coefficient of variation of **0.7 or higher**. Uniform medium-length sentences are the clearest structural AI tell.
- **Against the AI crutches** — When you reach for a three-item list, ask whether two land harder; default to two, at most **2 tricolons per chapter**. If the "not just X but Y" or "it wasn't X, it was Y" shape starts forming, delete it and assert Y on its own.
- **Rex** — Behavior and empathic impressions, carried in Nate's voice channel; no System UI abilities, never human cognition (Oberon is the counter-model). **Bond articulation progresses P0→P3 across the series** — hold Book 1 at **P0 (impressions only, no word-thoughts)** through the Tutorial; later books climb toward full mental speech. **Range also evolves:** Ch1-8 impressions require physical contact; room-distance by first combat; grows from there. Content stays dog-shaped at every stage. Never explain the mechanic. See `project_pack_bond_progression`.
- **Screens** — ALL System interfaces are internal only. No visible glow. Faint blue glint behind the eyes is the only external tell. Nate cannot see other people's UIs — he only sees their *behavior* (hand gestures at nothing, voices pitched with discovery).
- **Unified-source theology** — God is the sole source of all power. The **System** is Lucifer's rebranded framework — runs on God's power but brands it as its own. Never let prose treat the System as neutral tech. Nate has inherited agency (child of God) — he actively channels, directs, aims. NOT a passive vessel. Governor is *alignment*, not permission. Show through Narnia guardrails only; never explain. See `project_forge_theology_unified_source.md`.
- **2026-04-23 cosmology architecture (Codex #177, #178, #179)** — Creator is sole source; Labyrinth is His *pipeline* (not a source). Spirit → Conduit Gifts direct, bypassing Labyrinth. Three protection guarantees: (1) Conduit Gifts protected from System skewing — System has only inferior knockoffs; (2) Labyrinth is not a source; (3) **substrate is always clean** — mana pools, physical energy, life, breath are Creator-owned and incorruptible. Only skill-*use* carries channel routing. A System-bound user has a clean mana pool but uses skewed skills. **NEVER** in prose: "substrate", "clean channel", "skewed channel", "amplification overlay", "Conduit Gift" as category label, "Labyrinth pipeline", biblical Gift names as proper nouns (Gift of Tongues, Word of Knowledge, etc.). Show through effect. See `project_forge_skill_system_design.md` and `research/skill-system-design.md`.
- **Conduit amplification overlay (Codex #178)** — Nate's Conduit power is now an amplification OVERLAY riding on top of his owned skills, not a separate power to lose. Three states: **Aligned** (per-action AND state-of-being both point to Creator → overflow active, caps exceeded), **Doubt/Plateau** (base capacity only, no overflow), **Opposition** (stasis, not decay — Gifts silent while opposed, return instantly on realignment). Alignment is LAYERED: per-action AND state-of-being. Opposition = stasis not decay; nothing atrophies. Two flavors: amplification-type (overlay on existing skill — SA past rank, Pyromancy past mana cap) vs origination-type (Gift with no base — Tongues). Prose: show overflow through effect; never name the overlay. See `feedback_conduit_power_doubt.md` (refined 2026-04-23).
- **True names vs. labels (Codex: True Names & False Labels)** — Labyrinth-delivered originals (faculty names, bonds, vocations, Gifts) are TRUE names with identity-power; the System overlays *labels* on top — class names, skill nameplates, bold System UI vocabulary. NEVER describe a Labyrinth-original as "unbranded" / "nameless" / "without a name" — it has a name beneath. NEVER describe the System as *naming* something for the first time — the System labels, it does not name. Use rancher-authentic common names for Nate-faculties (stockman's sense, NOT shepherd's-eye — sheep-coded). Capital-letter Labyrinth-true names (Heordsight, the Wardenship, etc.) live in codex, surface in prose only when earned (Book 2+). The "**re-**" prefix ("re-shelved," "re-skinned") and spatial "**over**" preposition ("a label sliding into place *over* the original") are grammatical signatures of false-naming — preserve when System overlays an original. See `feedback_true_names_and_labels.md`.
- **Soul-DNA architecture & Job effect (Codex: Soul-DNA Architecture)** — The soul (humans only) holds YOU + Spirit (if invited via baptism). NOTHING else, ever. System cannot enter the soul. Mind ≠ soul; rooms (Flint's, Rex/Judge, family, faith) live in the *mind*, soul-authored via DNA. **Two paths to DNA:** Path 1 soul-authoring (private, Spirit-direct Conduit Gifts use this); Path 2 Labyrinth external delivery (System has hijacked-overlay-access here). **Spirit-firewall sits at Path 2 in three modes** (sovereign decision, NOT binary): block cold (System overwrite of soul-authored region), allow with rewrite (System install in new DNA-slot — Flint born here), pass (legitimate Labyrinth delivery). **Job effect:** God allows what serves His purpose; permission is the frame, not protection — Spirit-indwelt characters can suffer real cost. **Bonded-animal DNA-node:** when Nate bonds Rex/Judge his DNA gains a node carrying their pattern; respawn routes through Nate's domain (Adamic dominion, Genesis 1:26-28 / 2:19-20). Beast Master "Companion" bond = System-DNA-only, no soul-node, can't deepen. **OPEN in prose:** "soul," "DNA," "Spirit" (rationed in close-third Nate); Storyteller-omniscient may hint at Job-effect with Hiberno phrasing ("Sure, He sees the whole of it"). **HELD shorthand only — NEVER in prose:** "Path 1 / Path 2," "Spirit-firewall," "Job effect," "DNA-node," "fiber-channel," "block-cold / allow-with-rewrite / pass," "three-mode firewall." Never frame Conduit power as immunity or force-shield. See `project_forge_soul_dna_architecture.md`.
- **Skill vs Ability terminology** — Skills are rank-bearing containers (Sword Mastery, Cooking, Structural Analysis). Abilities are named moves/powers inside a Skill (Riposte, Ignite). "Sub-skill" / "technique" retired as taxonomy terms; lowercase "technique" acceptable prose flavor for mundane/no-HUD action. Ten domains: 1-9 (Martial/Perception/Stealth/Social/Physical/Gathering/Crafting) + Domain 10 Life Skills (Home/Trade/Profession/Arts/Body/Mind/Social). See `feedback_skill_vs_ability_terminology.md` and Codex #177.
- **Flint quantum substrate** — All Spirit-rewritten anomaly AIs run on quantum processing, not classical System rails. Flint does NOT know this about himself. Nate does NOT know. Only the Storyteller may name it, at a scheduled reveal (per `revelation-schedule.json` → `flint-quantum-substrate`, deep-reveal arc for mid-Book-2 / Book-3). Flint's hedges, `[PROCESSING]` tags, and "about ninety percent" phrasing are honest in-substrate uncertainty — write them that way, never explain the mechanism, never let Flint self-diagnose. See `project_forge_flint_quantum_substrate.md` and Codex #2.
- **Progression crunch (low-moderate)** — Stat blocks max ~6 lines. Skill choices: 2-3 options, decided same scene, no multi-chapter deliberation. Numbers shown *in play*, not audited on screens. Flint narrates all number-work with personality. No loadout optimization scenes. Level-ups at transitions, never mid-action. Book 1 progression: Ch1-8 word-descriptions only (no stat sheet); mid-to-late-mid Book 1 rudimentary progress indicators appear; late Book 1+ Flint-authored HUD. See `project_forge_progression_and_flint_arc.md`.
- **Pop-culture refs** — Star Wars / Jedi / Force language is worldbuilding-only, NEVER in Storyteller prose. Nate may make in-character gamer asides referencing them as throwaway lines only, never load-bearing comparisons. Flint may reach for pop-culture if it lands on the Comedy Dial 4-5 weighted-to-4 register, but never as theological scaffolding. Same principle for other pop-culture refs. See `feedback_pop_culture_in_prose.md`.
- **HUD phase** — Check which phase applies to this chapter (1A Boot through 2B Tactical). Do NOT write features from later phases.
- **Bold formatting** — System terms bold as proper nouns only: **Structural Analysis**, **Field Repair**, **Vanguard**. Lowercase/plain for group or action usage.
- **SA expansion** — Spell out **Structural Analysis** at first use per chapter and again after scene breaks or ~2,500 words of SA-only usage.
- **No lens labels** — NEVER write "the gamer in him," "his engineering brain," or any variant. Show through vocabulary, not labels.
- **Faith through actions** — Never internal theological reflection. The occupied space holds, resists, protects. Never explained.
- **Prayer as stillness** — Show through a pause, a breath, observable stillness. Never state "he prayed."

---

## Drafting Protocol

### Write

1. Write all target beats as continuous prose
2. Target word count per beat: guided by outline (typically 800-2000 words per beat)
3. File target: `drafts/ch{NN}-{slug}-draft01.md`

### Flag Inventions

Use `[INVENTED: "detail", category]` inline markers when you invent any detail NOT in the Codex or character sheets:

**Must flag (always):**
- New proper nouns (character names, place names, item names)
- New character traits or backstory not established
- New game mechanics or System behaviors
- New locations or environmental details with narrative weight

**May invent without flagging (minor):**
- Generic environmental description (weather, lighting, ambient sounds)
- Transitional actions (walking, sitting, gestures)
- Food and drink (unless plot-relevant)
- Furniture and decor (unless it matters)

**Inline format:**
```
The bartender — a heavyset woman named [INVENTED: "Gracie Tull", minor NPC] — slid a tankard across the bar.
```

### Present for Review

1. Present the complete draft in conversation for David's review
2. At the end of the draft, collect ALL `[INVENTED]` markers into a summary table:

| # | Detail | Category | Location | Keep? |
|---|--------|----------|----------|-------|
| 1 | "Gracie Tull" | minor NPC | para 12 | |
| 2 | "thornbark ale" | item | para 15 | |

3. **Do NOT commit to git-forge until David approves**
4. After approval: `write_file` via git-forge, then `git_commit` with descriptive message
5. **Do NOT `git_push` without explicit permission**

### Post-Approval

- Update beat statuses via `forge_outline_update_beat` (status → `drafted`)
- Add approved inventions to Codex via `forge_codex_create`
- Update `SESSIONS.md` with session log entry (append to top)

---

## Post-Draft Self-Audit

Run this checklist BEFORE presenting the draft to David. Fix any failures first.

The checklist is two-tiered. **Always-run core** (every draft): checks 1, 2, 3, 4, 6, 7, 8, 9, 9b, 10, 11, 12, 12a, 13, 14, 16, 23, 31, 32, 33. **Conditional** — run only when the mechanic or character actually appears in the chapter: 2b / 5 / 19 (Rex or Judge present), 12b (villain or corrupted character curses), 15 (hint/reveal chapter), 17 (progression or stat content), 18 (pop-culture reference), 20 (power/cosmology content), 21 (Conduit overflow beat), 22 (System-bound user casts), 24-26 (Labyrinth-original or System-naming content), 27-29 (soul / DNA / Spirit content), 30 (respawn shown). Don't tick a conditional check that doesn't apply.

| # | Check | Pass? |
|---|-------|-------|
| 1 | Every paragraph assignable to one voice (Storyteller / Nate / Flint / pack-bond translation)? | |
| 2 | Storyteller woven throughout (not bookended), no dead-middle stretch without her presence? | |
| 2b | If Rex or Judge appears: pack-bond translation carried in Nate's voice channel with accent flavor (Scots for Rex, Aussie for Judge)? Flint never hears pack-bond traffic? | |
| 3 | No lens labels ("the gamer in him," "his engineering brain")? | |
| 4 | No visible screen glow (internal only, faint blue glint)? | |
| 5 | No Rex dialogue or word-thoughts? | |
| 6 | Bold formatting correct on System terms (proper nouns only)? | |
| 7 | SA spelled out at first use + after scene breaks? | |
| 8 | Correct HUD phase for this chapter number? | |
| 9 | Comedy landing per the per-voice Comedy Dial (Flint 5 / Storyteller 4-5 / Nate 3-4)? Not flat? | |
| 9b | Voice transitions flow in the read-aloud test? No hard collisions, no orphaned fragments across interludes? | |
| 10 | `[INVENTED]` markers on all new proper nouns and significant details? | |
| 11 | Faith shown through action, never told or reflected on internally? | |
| 12 | No Lord's name in vain ANYWHERE (absolute, all voices incl. villains: no "God damn," "Jesus" as expletive, "Oh my God," "Christ Almighty," "Lord above," "God help us")? | |
| 12a | Nate spoken-profanity count within cap (3-5 vocalized per ~5,000 words; interior thoughts/POV-prose excluded from count)? | |
| 12b | If a corrupted/villain/System-aligned character curses or invokes a higher power: drawn from the villain palette (Morningstar/System/Pit cosmology-native oaths, demonic register, edge-of-line constructions, or action-as-blasphemy)? Never the real Name. | |
| 13 | No AI-slop words or structural patterns? (See `references/anti-slop.md`) | |
| 14 | Epistemic discipline? Nate doesn't reference anything outside his `knows` list? | |
| 15 | Scheduled revelations advanced? Any hint/reveal chapters for this chapter covered? | |
| 16 | System treated as Lucifer's rebrand (not neutral tech)? Nate has active agency (not passive vessel)? | |
| 17 | Crunch guardrails held? No stat blocks >6 lines, no optimization scenes, no mid-action level-ups? | |
| 18 | No Star Wars / Jedi / Force refs in Storyteller prose? (Nate in-character asides OK; Flint Comedy-Dial landings OK) | |
| 19 | Rex bond range appropriate to chapter phase? Ch1-8 requires touch; combat-onward allows room-range telepathy. | |
| 20 | 2026-04-23 protected vocabulary absent from prose? (substrate / clean channel / skewed channel / amplification overlay / Conduit Gift / Labyrinth pipeline / biblical Gift names) | |
| 21 | If a Conduit overflow beat fires (SA past rank, mana cap exceeded, Gift manifests): shown through effect, not named. Overlay mechanic never mentioned. | |
| 22 | If a System-bound user casts: their mana pool is clean substrate (never described as dirty/corrupt). Skew is in the ALLEGIANCE-routing of the skill, not the energy. | |
| 23 | Storyteller register split honored? Omniscient passages carry Hiberno-English markers (after-perfective, "ye'll find," "yer man," Catholic-flavoured similes). Physical-zoom passages stay plain literary English with NO Hiberno markers. No "Jaysus / God help us" anywhere. | |
| 24 | True-name discipline: no "unbranded" / "nameless" / "without a name" applied to a Labyrinth-original (faculty / vocation / bond)? Common names rancher-authentic (stockman, not shepherd, for cattle-rancher faculties)? | |
| 25 | The System is NEVER described as *naming* something for the first time? (System labels; it does not name. Grammar tells of correct false-naming: "re-" prefix verbs, "over" preposition.) | |
| 26 | "True name" as an explicit term does NOT appear in prose (held in reserve until Book 2+)? | |
| 27 | Soul-DNA architecture: NO prose implies the System enters or writes to the soul (System touches DNA only via Path 2; soul defends soul-authored regions via Spirit-firewall)? NO prose puts Flint, Rex, Judge, or other guests inside the soul itself (rooms live in the *mind*, soul-authored)? | |
| 28 | Conduit power is NEVER framed as immunity or force-shield (permission is the frame, not protection — Job-effect)? Spirit-indwelt characters can suffer real cost on the page? | |
| 29 | Writer-shorthand cosmology terms do NOT appear in prose: "Path 1 / Path 2," "Spirit-firewall," "Job effect," "DNA-node," "fiber-channel," "block-cold / allow-with-rewrite / pass," "three-mode firewall"? (`soul`, `DNA`, `Spirit` ARE open — these architectural labels are not.) | |
| 30 | Bonded-animal respawn (if shown): pattern routes through Nate's DNA-node domain (Adamic dominion), NOT framed as the dog's own DNA self-restoring? Beast Master Companion respawn (if shown): System-mediated DNA-template restore — different mechanism, no deepening? | |
| 31 | `kit/prose_lint/prose_lint.py` clean of FAIL findings — no Tier 1 banned words, no "not just X but Y" / "it wasn't X, it was Y" constructions? (Run `python kit/prose_lint/prose_lint.py <draft>` on the new file, or note it will run on the advisory hook.) | |
| 32 | No mechanical formatting inside narrative prose — no `##` headers, no bullet lists, no bold-for-emphasis mid-paragraph? | |
| 33 | Sentence length visibly varied within paragraphs (burstiness, not uniformity)? Em-dash density ≤ 2/1k for new un-narrated drafts? | |

If any check fails, revise the draft before presenting. Note which checks required revision in your presentation.

---

## Error Handling

**MCP server down:** Warn David. Provide restart commands. Do not attempt to write without Codex/outline context.

**Session GC (forge-mcp):** If you get "Session not found" errors, the 10-minute idle reaper fired. David can restart:
```
ssh nova "wsl -d Ubuntu -e sudo systemctl restart forge-mcp"
```

**Missing outline beats:** If the target chapter has no beats in the outline, present this to David as a pre-draft question. Do not invent beat structure.

**Missing character sheet:** If a character appears in the beats but has no sheet in `characters/`, flag it. Use Codex entity data as fallback but note the gap.
