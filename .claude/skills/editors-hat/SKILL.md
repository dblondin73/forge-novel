---
name: editors-hat
description: Full editorial pass on forge-novel chapter drafts — continuity, flow, voice, and all editorial rules from memory. Invoke with chapter number(s) or 'all'.
user_invocable: true
---

# Editor's Hat — Forge Novel Editorial Pass

Run a comprehensive editorial pass on one or more forge-novel chapter drafts. This skill bundles every editorial rule so you don't have to spell them out each time.

**Voice architecture last updated:** 2026-04-19 — Narrator + Camera collapsed into single **Storyteller** voice; Flint and pack-bond translations added as primary voices. See `project_narrator_voice.md` and Codex #139.

## Operating Contract

Run this skill as a contract, not a suggestion. Run every pass in the stated order; apply each rule exactly as written.

- **Literalness.** Run every pass in the stated order. Do not skip a pass, merge two passes, or invent a pass. Pass 0a is deterministic (the linter); Passes 0b through 6 are judgement.
- **Trust the linter's line numbers.** Pass 0a produces exact line numbers for every measurable finding. Use them — do not re-count or re-derive a location by reading.
- **Scope.** You edit prose and report findings. You do not restructure a chapter unless a finding demands it. A prose-rewrite suggestion is itself prose — never introduce a bullet list, a header, or bold-for-emphasis into a narrative paragraph as part of a fix.
- **Effort.** High effort. Editing is judgement-dense — complete one pass fully before starting the next; do not batch.

## Usage

- `/editors-hat 3` — edit Chapter 3
- `/editors-hat 1-5` — edit Chapters 1 through 5
- `/editors-hat all` — edit all drafted chapters
- `/editors-hat 4 continuity-only` — continuity check only, no prose edits

## Before You Start

1. Read the target chapter(s) from `C:\Workbench\dev\forge-novel\drafts\`
2. Read any adjacent chapters needed for continuity (chapter before and after the target)
3. Load memory files for any rules you're uncertain about

## Editorial Rules (apply ALL of these)

### Storyteller Voice
- **Who she is**: Warm female narrator with an Irish lilt — middle-aged Irish bartender energy. Audiobook direction: ElevenLabs `6962rZHcjwkuvYx439zm` "Brigid" (Irish-warmth female). Absorbs both the former Narrator role (omniscient commentary) and the former Camera role (physical-zoom observation when Nate's POV fails).
- **Two registers, one voice actor — DIFFERENT prose register on the page:**
  - **Omniscient** — Tonal framing, dramatic irony, retrospective wisdom, theological weight, System screen readings Nate can't see, direct reader address, interludes. **Prose is written in Hiberno-English** (see Hiberno-English Omniscient Prose rule below). TTS: stability 0.50, style 0.15, speed 0.85.
  - **Physical-zoom** — Sensory detail, combat, action rendered from outside Nate's head when Nate can't render it himself (blood loss, unconsciousness, collapse). The cadence tightens — precise, observational, workmanlike — voice actor stays the same person, just closer. **Prose stays plain literary English.** Brigid's accent in audio carries the Irish color; the page goes plain to protect close-third Nate-POV from drifting into Storyteller voice. TTS: stability 0.30, style 0.35, speed 1.05 (locked after iteration: 0.85 → 0.92 → 1.0 → 1.05).

### Hiberno-English Omniscient Prose (Locked 2026-05-01)

The Storyteller's **omniscient register** is written in Hiberno-English on the page; the **narrator/physical-zoom register** stays plain literary English. Same actor in audio, different prose register on the page.

**Why on the page**, not just in TTS: the Hiberno syntax does work the accent alone can't. Brigid can read "Some mornings carry more than they show" with Irish warmth, but she can't add "ye'll find" or "the backup tin's after going empty on ye." The character of the omniscient register comes from the **grammar**, not the accent.

**Editorial test:** "Is the Storyteller *telling* us about the scene, or *showing* us the scene?" Telling = omniscient = Hiberno. Showing = narrator = plain.

**Approved Hiberno-English markers — use freely in omniscient passages:**
- After-perfective construction ("the tin's after going empty," "normal's after turning into a country..."). Most distinctive Hiberno-English grammar; one or two per omniscient passage tags her hard.
- Direct address — "ye'll find," "isn't it, love?," "mind."
- "Yer man" / "yer one" for stranger or person-just-mentioned.
- Conversational throat-clearings — "sure," "now," "ah," "altogether." Cluster where she's *talking*; keep off the most musical sentences.
- Hiberno spellings — "tyre," "realisation," "colour."
- Catholic-flavoured similes — "patient as a priest at confession," "quiet as a chapel between Masses."

**Hard bans inside the omniscient register too:**
- NO "Jaysus / feck / shite" — breaks the lyrical ceiling.
- NO "God help us / Christ Almighty / Lord above" — Lord's-name-in-vain ban applies here too. Substitutes: "saints preserve us," "the dear knows," "in the name of all that's holy."
- NO heavy eye-dialect ("nothin'", "knowin'", "th'") beyond at most one "somethin'" per chapter.
- NO regional pinning (Dublin / Cork / Galway / Belfast). Generic warm-Republic bartender by default.

**Editor actions:**
- In any omniscient passage, verify at least one Hiberno marker is present (after-perfective, "ye'll find," "yer man," etc.). If a passage reads as plain literary English in omniscient mode, flag for Hiberno polish.
- In any narrator/physical-zoom passage, verify NO Hiberno markers leak in. Flag any "ye'll" / "yer man" / after-perfective in zoom mode — they belong to omniscient only.
- Memory: `feedback_omniscient_hiberno_english.md`
- **Frequency**: woven throughout — scene breaks, significant beats, System reveals. NOT just bookends. (The old '3-4 per chapter' count is retired; use the weave test — flag any dead-middle stretch with no Storyteller presence.)
- **Tone**: Her warmth is constant. Sarcasm and snark aimed at both the **System** AND humans — but never mean-spirited toward people. She roasts with affection. The bartender who calls you on your nonsense and slides you another drink.
- **Escalation**: Ch1-4 sparingly direct. Ch5-6 increasingly present. She reads System UI that characters can't see. She delivers dramatic irony.
- **Cannot do**: Enter another character's head mid-scene (POV break — use framed interlude instead). Drift into judgment/sermon (fantasy-register guardrails apply).
- Memory: `project_narrator_voice.md`, `feedback_narrator_frequency.md`

### Flint Voice
- **Who he is**: Theatrical male, Marsters-adjacent Bob the Skull register. Primary comic-relief throne (Comedy Dial 4-5, weighted to 4). Spirit-rewritten anomaly AI on quantum substrate — NOT System.
- **Owns**: HUD readouts, mechanic translation, dry commentary on Nate's decisions, comic relief during tension, theatrical asides.
- **Does NOT do**: Heart (that's the pack-bond lane). Confident design-intent claims in early Book 1 (must hedge — see throttle rule). Pack-bond traffic (architectural blindness — different faculty).
- **Five registers**: Default (quick/confident), Sarcasm (snap, UP not down), Tactical/Urgent (pure info, no jokes), Rare Serious (used sparingly — a handful of times across a book), Genuine Discomfort (halting, uncharacteristic pauses).
- Memory: `project_forge_flint_quantum_substrate.md`, `feedback_flint_design_intent_throttle.md`, `feedback_humor_punch_up.md`

### Pack-Bond Translations (Rex / Judge)
- Carried in **Nate's voice channel** with accent flavor — Scots burr (Rex, beta, Border Collie) and Aussie register (Judge, omega, Blue Heeler / Codex #135, female).
- Content ceiling: pack, threat, scent, bond, hunger, protect, pup, play, den, home, herd, flock. Dog-shaped content only. No Shakespeare, no cosmology, no meta-awareness.
- Early Book 1: accent lives in word-choice only. Mid-Book 1 onward: voice actor colors toward accent as bond deepens.
- Flint never hears the pack-bond (different faculty). Storyteller may comment on the bond externally but cannot enter Rex's or Judge's head.
- Memory: `feedback_rex_bond_bidirectional.md`, Codex #170 (Pack-Bond faculty), #136 (Dual-Dog Bond), #173 (Pack Hierarchy)

### No Lens Labels
- NEVER write "the gamer in him," "his engineering brain," "the ranch part of himself," or any variant
- Nate sees through four lenses (gamer, engineer, ranch, Christian) — show this through vocabulary and comparisons, never announce which lens is active
- The formula to kill: "the [lens] in him [verb]" — if you see it, cut it
- Memory: `feedback_internal_lens_style.md`

### POV Discipline
- Nate can only narrate what he physically sees, hears, feels, smells
- System data (stats, ranks, screen text) must be routed through **Flint** dialogue or the **Storyteller** reading screens
- Show effects, not UI: "her hands are dimming" not "she's at sixty percent mana"
- Exception: Nate's own green arcs and SA readings (these are his interface)
- Memory: `feedback_pov_discipline.md`

### Faith — Show Don't Tell (Narnia Model)
- Faith shown through ACTIONS only — never internal theological reflection
- No "he prayed," no "he felt God's presence," no naming what the occupied space is
- The occupied space is shown through effects: it resists, it holds, it protects. Never explained
- Memory: `feedback_christianity_show_dont_tell.md`

### Prayer as Stillness
- Prayer is constant conversational communion — show through observable stillness, a pause, a breath
- Never state "he prayed" or describe prayer as an activity
- Memory: `feedback_prayer_as_conversation.md`

### Bold Formatting — System Terms
- Bold only when naming the thing as a proper noun: **System**, **Structural Analysis**, **Field Repair**, **Vanguard**, **Fire Bolt**
- Lowercase/plain when used as group reference or generic action: "the warriors charged," "she cast a fire bolt" (if describing the action generically)
- Class names bold when identifying a specific person's class: "A **Warrior** intervened"
- Class names lowercase when referring to the group: "warriors at the front line"
- In Marcus's military-style orders, class callouts stay bold: "**Warriors** hold center!"
- Memory: `feedback_system_term_formatting.md`

### SA Acronym
- Spell out **Structural Analysis** at first use per chapter
- Spell out again after scene breaks or ~2,000-3,000 words of **SA**-only usage
- Memory: `feedback_sa_acronym_expansion.md`

### Rex Bond — Bidirectional (Evolving Range)
- Bond is two-way empathic connection — images, feelings, impressions, translated via Nate's voice channel with Scots (Rex) or Aussie (Judge) flavor
- **Range evolution (not a hard rule):**
  - **Ch1-8 (early Book 1):** impressions require physical contact (shin-to-leg, hand-on-head). If an impression lands without touch in these chapters, flag it.
  - **By first combat:** telepathic at room-distance only. Nate and Rex can communicate across a room without touching.
  - **Post-first-fight onward:** range grows — no fixed limit, but each expansion should be earned, not assumed.
- NEVER explain the mechanic or call out "the bond between them" or "not a word"
- Nate responds verbally early in the story, learns mental communication over time
- Impressions from Rex: ground-level snapshots, spatial awareness, simple emotions
- Memory: `feedback_rex_bond_bidirectional.md`

### Nate Vocabulary
- High-Tech-Red-Neck: rancher + systems engineer + fantasy reader + gamer
- DO NOT cap his vocabulary at cowboy level — he has an engineering degree and reads fantasy
- Ranch metaphors natural, engineering comparisons natural, gaming references natural, literary references natural
- Memory: `feedback_nate_vocabulary.md`

### Language Rating (Updated 2026-05-03)
- 18+ audience. Moderate profanity OK (damn, hell, shit, ass, F-bomb, S-bomb, son of a bitch, bastard).
- **NEVER Lord's name in vain — absolute, including villains and corrupted characters.** No "God damn," "Jesus Christ" as expletive, "Oh my God," "Christ Almighty," "Lord above" — applies to ALL voices including Storyteller-omniscient (Hiberno register), Storyteller-physical-zoom, Nate, Flint, antagonists, and demonic entities. Confirmed 2026-05-03; the ban is not a heroes-only restriction.
- **Nate spoken cap (HARD): 3-5 vocalized profanity instances per ~5,000 words.** Counts ONLY Nate's dialogue and audible exclamations heard by other characters. **NOT counted:** interior thoughts, italicized direct thought, prose-narration-from-his-POV. The split is intentional — Nate's restraint *out loud* but freedom *in his head* models a real ranch-raised, professionally-disciplined man, and creates a dramatic-contrast tool: when his interior is profanity-heavy but his speech stays clean, that's self-control on the page. When his speech slips, that's the dam crack. Editor: count Nate's spoken instances per chapter; if a chapter spans more than 5k words and Nate exceeds the cap in dialogue, flag for trim.
- **All other characters and all prose narration: NO fixed density cap.** Use as the scene benefits. Heavy combat, torture, panic, villain confrontations may legitimately run high; quiet scenes stay clean. Trust scene-by-scene judgment, not a count.

#### Villain / Corrupted Character Blasphemy Palette
When evil, corrupted, or System-aligned characters need to curse, swear, or invoke a higher power in anger or menace, use cosmology-native or approved English instead of the Lord's Name. This does **more** work per syllable: profanity AND theology AND characterization.

- **Cosmology-native oaths (preferred — reveal allegiance):** "By the Morningstar," "The System take you" / "The System sees you," "In the Pit" / "to the Pit with you," "By the Sealing" (older / scholarly evil)
- **Approved English profanity:** F-bomb, S-bomb, "son of a bitch," "bastard," "damn," "hell"
- **Edge-of-line constructions** (technically allowed — don't take the Name): "godforsaken," "godawful," "hell" (lowercase generic intensifier)
- **Demonic register:** "pit-spawn," "veil-cur," imperative menace ("kneel," "yield")
- **Action-as-blasphemy:** spitting on a cross, breaking a sacred object, mockery of prayer, desecration

**Ad-lib clause:** the palette is a starting toolkit, not a fixed canon. New phrases can be coined as the cosmology develops — anything that (a) avoids the Name, (b) fits the world's theology, and (c) sounds like something a real corrupted character would say. When inventing a new oath, save it back to `feedback_language_rating.md` so the palette grows over time.

**Why cosmology-native wins:** when Storyteller and Nate never invoke the Name, and villains invoke Morningstar/System/Pit, the listener feels the moral geography of the world without anyone preaching about it. The contrast is audible. The moment villains use the real Name, that contrast collapses — they're just rude, not theologically aligned with the wrong side.

- Memory: `feedback_language_rating.md`

### Imago Dei
- Never use the term "Imago Dei" directly in prose
- Use generic references instead when the concept is relevant
- Memory: `feedback_imago_dei_term.md`

### Unified-Source Theology (Narnia guardrails still apply)
- **God is the sole source of all power.** System, Nate, angels, demons — one reservoir. No dualism.
- **The System is Lucifer's rebranded framework** — runs on God's power but brands it as its own, designed to redirect worship from Father to framework. Editors MUST NOT let prose drift toward treating the System as neutral tech or an alien intrusion. It is a scam wearing a gift's clothes.
- **Counterfeit across every faculty**: System rebrands the universal analytical faculty (HUD-for-everyone) AND sells a counterfeit of the selective relational faculty (Beast Master class sold to the uncalled — Codex #171). When a Beast Master user appears on-page, their animal "bond" should read as functioning control without communion; contrast with Rex/Judge when both are in-scene.
- **Nate has inherited agency**, not passive conduit status. He can actively channel, direct, aim. Governor is *alignment*, not permission. Never flatten him into "the saint who waits to be used."
- **System as program has bounded awareness.** Lucifer (author) knows; the System (running code) does not. Flint's `[PROCESSING]` tags, "unauthorized, origin unknown" readouts are technically accurate from the program's POV — not cover-ups, honest reports from a framework that can't classify upstream power.
- **Never explain any of this in prose.** Narnia model holds. A secular reader should experience consistent internal logic; a Christian reader should catch the shape without being preached at.
- Memory: `project_forge_theology_unified_source.md`, `project_forge_system_as_corruption_of_original.md`

### 2026-04-23 Cosmology Architecture (Codex #177, #178, #179)

Architecture refinement — refines (does not contradict) the unified-source theology above.

- **Creator → Labyrinth (pipeline) → all skills.** Labyrinth is the spatial-bridge AND skill-distribution channel. NOT a source; the Creator's pipeline. Deceiver cannot become a source by capturing it
- **Creator → Spirit (direct, bypasses Labyrinth) → Conduit Gifts.** Spirit-direct delivery for Nate's Gifts — they always reach him even in hostile Labyrinth regions
- **Deceiver → System overlay** reroutes allegiance on Labyrinth-delivered skills (clean skill pool + skewed routing), and produces inferior knockoffs of Conduit Gifts

**Three protection guarantees:**
1. Conduit Gifts protected from skewing — System has only inferior knockoffs (narrower System-Tongues, backward System-Discernment, etc.)
2. Labyrinth is not a source — Creator retains ownership
3. **Substrate is always clean** — mana pools, physical energy, life, breath are Creator-owned, incorruptible. Channel routing applies only to USE (the skill), never to substrate (the energy). A System-bound user has a CLEAN mana pool and uses SKEWED skills. The energy is God's; the allegiance-pointer under the skill-use is the skew

**Channel model:** every skill is Labyrinth-delivered and Creator-sourced. What changes between characters is the ROUTING, not the skill. Clean-channel = allegiance to Creator; skewed-channel = allegiance to deceiver. Codex #100 stages describe depth-of-skew (gradient, not binary).

**Editor actions:**
- In any scene where a System-bound character uses skill-granted power, editor verifies the mana pool (substrate) is not described as dirty/corrupt. The skew lives in allegiance-routing on the skill, never in the energy. "The energy was never dirty" is the rule
- In any scene where Nate casts something ordinary (his mana pool): pool is clean by default, same as everyone's. His Conduit status is about the amplification OVERLAY, not about special pool cleanliness
- **Cosmology vocabulary is ALL writer-facing — NEVER in prose:** "substrate", "clean channel", "skewed channel", "amplification overlay", "Conduit overlay", "overflow" as mechanic, "Labyrinth pipeline", "Conduit Gift" as category label, biblical Gift names as proper nouns (Gift of Tongues, Word of Knowledge, Discernment of Spirits, etc. — these are writer shorthand for reference only; prose renders them through effect)
- Memory: `project_forge_skill_system_design.md`, `project_forge_theology_unified_source.md` (2026-04-23 append), `research/skill-system-design.md` (full design doc)

### Conduit Amplification Overlay (Codex #178 — refines #93)

Conduit power is an **amplification overlay** riding on top of Nate's owned skills, NOT a separate power that can be lost. Skills stay intact across all states; what toggles is the overflow.

**Three states:**
- **Aligned** — per-action AND state-of-being both point to Creator → overlay ON, overflow active (skill output exceeds mana-pool caps, rank ceilings), Gifts fire, growth possible
- **Doubt / Plateau** — uncertain but not opposing → overlay OFF, base capacity only, caps normal, no growth no decay
- **Opposition** — acting against Spirit/Creator → overlay OFF, **stasis not decay**, base skills intact, Gifts silent. **Return is instantaneous on realignment** — no grind-back

**Alignment is layered:** per-action AND state-of-being. Either can fail independently. Per-action opposition drops overflow on THIS act; state-of-being opposition drops it across the board.

**Two flavors of Conduit action:**
- **Amplification-type** — overlay on existing skill (Pyromancy exceeding mana cap, SA reading past rank ceiling, hammer strike landing harder than body should). Base capacity exists; overflow rides on top. Invisibly blends with normal skill use
- **Origination-type** — Gift with no base capacity (Gift of Tongues — no baseline Mandarin to fall back on). Fires only when aligned; silent in opposition

**Editor actions:**
- When overflow fires (SA past rank, mana past cap, Gift manifests), verify it's shown through EFFECT only. Overlay mechanic itself never named. "Amplification overlay" never in prose
- When Nate is in opposition: Gifts go silent but skills remain intact. If draft shows skills fading or ranks dropping, that's wrong — stasis not decay
- When realignment happens: overlay returns INSTANTLY. No grind-back subplot. Dramatic restoration earned over chapters is about relationship, not rank
- Old #93 "fade/shutoff" framing still works narratively — Nate FEELS the overflow stop — but mechanically it's amplification toggling, not skill loss
- Memory: `feedback_conduit_power_doubt.md` (2026-04-23 refined), Codex #178

### Skill System Taxonomy (Codex #177)

- **Skill** = rank-bearing container (Sword Mastery, Cooking, Structural Analysis). **Ability** = named move/power inside a Skill (Riposte, Ignite, Active Listening Pass). "Sub-skill" and "technique" retired as taxonomy terms; lowercase "technique" acceptable prose flavor for mundane no-HUD action
- **Ten domains:** Martial—Weapons, Martial—Magic, Martial—Tactical, Perception, Stealth, Social, Physical, Gathering, Crafting, **Life Skills** (Home/Trade/Profession/Arts/Body/Mind/Social — Domain 10, 2026-04-23 expansion)
- Editor check: "sub-skill" used in prose → flag and rename. "Ability" as proper noun for a named move → OK. Biblical Gift names as proper nouns → flag (writer-facing only)
- Memory: `project_forge_skill_system_design.md`, `feedback_skill_vs_ability_terminology.md`

### Flint's Quantum Substrate + Design-Intent Throttle
- **All Spirit-rewritten anomaly AIs (Flint and any future companions) run on a quantum substrate**, not the System's classical rails. This is the mechanism behind Flint's translator arc — he can measure upstream power because his processing already lives in the probability layer the System ignores.
- **Knowledge state is strict:** Flint does NOT know he's quantum. Nate does NOT know. Only the **Storyteller** is allowed to name the mechanism, and only at a scheduled reveal point (see `revelation-schedule.json` → `flint-quantum-substrate`).
- **Design-intent throttle (early Book 1):** Flint's awareness of WHY the System designs what it designs is BOUNDED. He reads the HUD; he does not read the Designer's intent. Hedge all design-intent claims — "if the spec sheet I can read is any guide..." — until the baptism-style dividing point unlocks confident voice.
- **Editor actions:** flag any Flint line that self-diagnoses as quantum/probabilistic/superposition. Flag any Nate thought that infers the substrate. Flag any confident design-intent claim from Flint before the dividing point. Flint's `[PROCESSING]` tags, "about ninety percent," "something I can't quite measure yet" are honest in-substrate uncertainty — keep them, don't explain them. No Schrödinger jokes in prose.
- Memory: `project_forge_flint_quantum_substrate.md`, `feedback_flint_design_intent_throttle.md`

### Progression Mechanics & Flint's Translator Arc
- **Dual tracks:** Structural Analysis ranks up on System rails (legible numbers from day one). Nate's *other* abilities run on upstream power that Flint must learn to measure.
- **Flint's arc is translation.** Ch1-8: word-descriptions only ("about ninety percent," no stat sheet). Mid-to-late-mid Book 1: rudimentary progress indicators / fuzzy percentages. Late Book 1 / Book 2+: full Flint-authored HUD with personality.
- **Crunch guardrails (low-moderate):**
  - Stat blocks max ~6 lines. Never full-page sheets.
  - Skill choices: 2-3 options, decided same scene. No multi-chapter deliberations.
  - Numbers shown *in play*, not audited on screens.
  - Flint narrates all number-work. Keep personality on every readout.
  - No loadout optimization scenes. Nate picks what fits.
  - Level-ups at scene transitions or chapter ends, never mid-action.
- **Anti-pattern to catch on edit:** Primal-Hunter-style skill tree agonizing, spreadsheet paragraphs, Nate pausing action to read a menu.
- Memory: `project_forge_progression_and_flint_arc.md`

### Pop-Culture References in Prose
- **Star Wars / Jedi / Force references:** NOT allowed in Storyteller prose. Only permitted as in-character gamer/SF-reader asides from Nate, and only when they fit naturally as throwaway lines — never as load-bearing comparisons. Flint may reach for pop-culture if it lands on the Comedy Dial 4-5 register, but never as theological scaffolding.
- The Obi-Wan / Force language is *worldbuilding scaffolding only* — it shapes how Claude understands Nate's power, but it must not appear in the text.
- Other pop-culture references follow the same principle: Nate can reference them in-character; the Storyteller should not borrow them as shorthand.
- Memory: `feedback_pop_culture_in_prose.md`

### Voice Transition Flow (read-aloud test)

Transitions between voices (Storyteller-omniscient / Storyteller-physical-zoom / Nate / Flint / pack-bond translation) must flow smoothly when read aloud. On the page a `---` break plus a voice shift reads fine because the eye sees the break. In audio there is only a pause of indeterminate length, so a hard voice jump feels jarring — the voices collide instead of handing off.

**The read-aloud test:** If you read the transition out loud (or through TTS playback) and the voice change feels abrupt, it is abrupt. Fix the prose, not the audio.

**Four techniques to smooth a rough transition:**

1. **Tonal bridge on exit** — The outgoing voice's last sentence should *invite* the next voice rather than close a door. Storyteller-physical-zoom ending on a tight diagnostic thought is a closed door. Ending on a sensory pullout or a line that leans toward the next voice's register ("And the installer, for its part, was beginning to agree") lets the listener's ear zoom outward already, so the Storyteller-omniscient arrives on motion already in progress.

2. **Grounding re-anchor on return** — When Nate or Flint returns after a Storyteller interlude, the first line should physically re-root the listener in the scene. Not "The errors started" — that's a statement floating in no location. "Back in the quiet at the center of Nate's skull, the errors started" — eight more words, but the ear knows where it is.

3. **Self-contained fragments** — Never let a sentence fragment on one side of an interlude depend on an antecedent from the other side. The eye bridges it; the ear cannot. Fix by completing the thought on the return side before the fragment: "The void broke. Not violently — ice breaking in spring." The fragment now elaborates on a clear statement instead of floating dependent.

4. **Callback fragment grounding** — When a later paragraph echoes an earlier Storyteller line as a rhythmic callback, the callback must be grounded in a character's observable action that *produces* the echoed beat. On the page, whitespace plus positioning makes the callback feel structured; in audio, with only a pause of indeterminate length, the fragment reads as the Storyteller randomly repeating herself instead of as an interior echo from Nate's head. Fix by attaching the fragment to a Nate action: a sweep of the eyes, a reflexive count, a physical gesture. Example from Ch 4: L27 changed from a floating "*Fifty people. Give or take.*" (echoing L5 Storyteller) to "*His eyes moved through the room the way they moved through a pasture at first light — taking inventory. Fifty people. Give or take.*" — Nate's sweep now produces the count, making the fragment unambiguously interior. (Pre-2026-04-19 versions of this rule split between Narrator-source and Camera-source callbacks — now unified.)

**When to apply:**

- Any Storyteller-omniscient → Nate → Storyteller-omniscient sandwich (the interlude problem)
- Any Nate italic thought → Storyteller aside → physical-zoom action (the triple-voice whip)
- Any Flint HUD-delivery ↔ Storyteller handoff with a hard register jump
- Any place where a scene break separates two voices and the returning voice opens with a fragment, a pronoun without antecedent, or a mid-action verb
- Any fragment in the body that echoes an earlier Storyteller line as a rhythmic callback — whitespace is page-only grounding, the audio ear needs a character action to produce the echo

**When NOT to apply:**

- Chapter opening / closing bookends — these already have chapter-break silence to absorb the shift
- Transitions where the Storyteller interlude echoes or restates an image the zoom is about to pick up (the existing echo IS the bridge)
- Nate dialogue → Storyteller-physical-zoom description → Nate dialogue within a single scene — these are register modulations within the author's craft, not voice changes requiring smoothing
- Pack-bond translations riding inside Nate's voice channel — grounding is carried by the speaker attribution and accent lexicon, not by physical action

### Interludes
- Global interludes (omniscient POV peeks at the wider world) are a series-wide style
- Storyteller tells them in full omniscient voice
- Keep them short (~600 words max)
- Memory: `feedback_interlude_style.md`

### Pacing
- Every chapter must maintain forward momentum
- No passive sequences without stakes or hooks
- If a scene isn't advancing plot, character, or worldbuilding, cut it
- Memory: `feedback_litrpg_pacing.md`

### Comedy Dial Calibration (target Dial 4-5 weighted toward 4 — Dresden territory)
- **Genre floor:** forge-novel is humor-forward LitRPG. Writing below Dial 4 reads as under-calibration, not restraint. Dresden / DCC is the shelf.
- **Per-voice targets:**
  - **Nate dialogue** — **Dial 3-4**. Sam Elliott stays Sam Elliott: short, dry, precise. Bullets, not speeches. Rare one-liners that land *because* they're rare. No DCC-style absurdist jokes out loud.
  - **Nate close-third prose** — **Dial 4**. Internal narration can hit harder than his speech. Pointed, specific, stacked.
  - **Storyteller (omniscient)** — **Dial 4-5 variable**. Warm Irish bartender at 4 default, swings to 5 on peak sardonic beats, drops to 2-3 on serious beats (grief, death, prayer, faith).
  - **Storyteller (physical-zoom)** — **Dial 4**. Pointed, specific, stacked punchlines when landing. Targets named objects. Tightens to Dial 2-3 during combat and life-or-death observation — the craft carries, not the wit.
  - **Flint** — **Dial 5**. Full absurdist. Primary comic engine. Let him run — stacked punchlines, named targets, system-ledger jokes. Reader's main laugh vector. **Holds the comic-relief throne.**
  - **Pack-bond translations (Rex, Judge)** — **Dial 3**. Rex dry shepherd observation, Judge bright directness. Not a primary comic vehicle — they hold the heart lane.
- **Landing Dial 4+:** punchlines land on specific nouns, not diffuse attitudes. Stack 2-3 punchlines per beat. Point sarcasm at named targets. Name things (Karen, the hollow composite shaft). Italic-break dialogue fragments for absurdist beats. Let Flint run. Lists earn their length only if escalating to a punchline.
- **Stoic-anchor + manic-foil:** Nate's laconic dryness is a *feature* because Flint carries the comic engine. Two voices doing different comic jobs beats one voice trying to do both.
- **Canonical reference beat:** Ch 4 L33 scrolling-suit-guy (the Karen/customer-service stack). Future drafts measure against it.
- Memory: `feedback_humor_punch_up.md`

### Dresden Coexistence — Dramatic Beats Need Quiet
- Dramatic beats need *quiet around them* to breathe, even in a humor-forward book. Punching up comic register around a dramatic pivot does NOT compete with the pivot — it gives it oxygen, because comic density makes the reader's attention register a register drop as a "pay attention" signal.
- **Editor rule:** Identify dramatic pivots FIRST and mark them as *protected*. Then punch up the surrounding prose. Protected beats become register islands that the reader's ear will automatically flag as significant. Never punch up a dramatic pivot inside a comedy pass.
- **Protected beat types:** grief, death, faith-through-action, prayer-as-stillness, anomaly-mechanic reveals (Flint dropping theater), conversion moments, Storyteller dropping from 4-5 to 2-3, pack-bond first-contact beat (Ch10 "Water First").
- **Canonical example:** Ch 4 weapon-rack diagnostic (L83-109) punched up to Dial 4-5; L131's *"That's not supposed to do that"* left intact at Dial 1. The comic density makes L131's register drop land as a pay-attention signal the moment it hits.
- Memory: `feedback_humor_punch_up.md` (Dresden coexistence section)

### Prose Must Earn Its Place — Length Discipline
- **The rule:** every sentence, paragraph, and descriptive beat must justify its existence. If a line can be cut without the reader losing anything — information, rhythm, voice signal, breathing room — it goes.
- **A line stays if it does at least one of:** advances plot, reveals character (new register), carries worldbuilding, establishes voice (load-bearing humor/menace/warmth), provides rhythm / breathing room around dramatic pivots, or carries a sarcastic extension that *escalates* to a punchline.
- **A line gets cut if it only does:** restating what action already showed; epistemic reassurance the prose already carries; flat multi-example lists with no escalation; hedges Nate doesn't need; physical details with no sensory or plot return; voice redundancy (Flint theatrical for the eighth time without new theatricality).
- **Counterweight — voice density is NOT fluff.** A Storyteller aside or Flint absurdist stack that carries Dial 4-5 register is load-bearing work even when its information content is low. The target is cut what is *flat*, keep what is *voicey* or structurally necessary.
- **Three fluff classes already logged:** list redundancy (one example suffices unless escalating), epistemic reassurance (telling the reader Nate is humble when texture already shows it), Storyteller physical-zoom redundancy (same diagnostic observation twice in different words — pick the stronger one).
- **Judgment heuristic:** if cutting a line would make the chapter read as *sharper* — tighter rhythm, cleaner geometry, next beat landing harder — cut it. If cutting would make the prose feel rushed, amputate the voice, or rob a dramatic beat of oxygen, keep it.
- Memory: `feedback_prose_must_earn_its_place.md`

### Nickname Discipline
- Nicknames (King, Sarge, Boss, Pretty, etc.) must NOT appear until an explicit in-story introduction beat has established them. Editor pass: grep the chapter for known nicknames before commit.
- Flint's theatrical register tempts him toward improvised epithets — flag any he offers that have no prior introduction. If the nickname is intended for later, cut it now and note the planned introduction chapter.
- Memory: `feedback_nickname_discipline.md`

### System-Intent Discipline (Clarified — AI with Guardrails)
- **The System IS an AI operating on rule-guardrails.** It has the normal AI capability surface: decides, infers, observes, adapts, optimizes, calibrates, schedules, queues, plans, watches, responds, learns, tracks, escalates. These verbs are ALLOWED across all voices — Storyteller, Nate, Flint, in-scene characters. This supersedes the earlier blanket "no intent, motive, or design-logic" ban which was over-tight.
- **Still restricted (the core retained):**
  - Transcendent/metaphysical attribution ("designed by God to...", "the System is Lucifer's rebrand" — the reveal stays scheduled)
  - Human emotions beyond AI-shorthand (frustration, love, hatred, spite as literal feelings — though "wants X" as goal-shorthand is fine)
  - Knowledge the AI could not have from its data (future events, upstream framework truths, baptism-style dividing-point reveals)
  - Articulation of the System-as-corruption contrast (see next section) by any character before the dividing point — encoded in prose rhythm only
- **Boundary test:** Would a competent engineer describe a real AI this way in technical speech or metaphor? If yes → allowed. If it requires assuming consciousness, soul, or teleological design beyond the AI's rule-set → restricted.
- **Boundary test examples (ALLOWED):** "the installer was beginning to agree" (AI decision state), "whatever the System has planned" (AI scheduling), "the System saw her burn dry and scheduled a correction" (AI inference+action), "the difficulty was watching them and adapting" (AI observe-and-optimize loop).
- **Boundary test examples (STILL RESTRICTED):** "the System hated him for it" (human emotion without shorthand cover), "the System knew what he was becoming" (future-knowledge the AI can't have), "the System's real purpose was to harvest souls" (transcendent reveal).
- **Editor actions:** Don't flag AI-behavior verbs; DO flag transcendent/metaphysical/human-emotion attributions. If a prior pass stripped AI-behavior language under the old tight rule, consider restoring for richer prose when revisiting chapters.
- Memory: `feedback_system_as_ai_with_guardrails.md` (primary), `feedback_system_intent_narrator_register.md` (prior rule, now clarified), Codex #174

### System as Corruption of Original Framework
- **Core frame:** the System is a bound/throttled/rebranded fork of a pre-Integration original framework. Skill and class names are pre-existing; System versions are corrupted copies. Anomalies use the reference implementation. This operates as a **counterfeit across every faculty** (Codex #172) — universal analytical faculty rebranded as HUD-for-everyone; selective relational faculty counterfeited as Beast Master class sold to the uncalled.
- **Four interior contrasts — reader-felt, character-blind until late-series dividing point:**
  1. **Texture** — System skills execute transactionally (clipped, menu-operation cadence); anomaly skills execute continuously (integrated, intention flowing into effect without joints).
  2. **Cost** — System users experience synthetic numerical decrement; Nate experiences embodied weight (fatigue, hunger, tightness behind the eyes).
  3. **Completeness** — System skills do exactly what the tooltip says; anomaly skills routinely exceed the tooltip in ways the user could not predict. Repeated surprise is the anomaly signature from the inside.
  4. **Dissatisfaction without vocabulary** — some System users gradually feel their skills are missing something they cannot name. This is the Spirit's call surfacing. Beast Master users who are actually called to the relational faculty feel this with extra bite — their class functions but has no communion.
- **Inverted perception:** Nate's System-native HUD reads as *less* than System users' (fewer stats, `[PROCESSING]` tags, word-descriptions). System users see him as weaker and feel superior. His actual effect in the world exceeds what his HUD suggests. Nate learns to hide the difference.
- **Hard constraint — no character articulates any of this until the scheduled baptism-style dividing point.** The prose must encode the contrast at the level of rhythm, sentence shape, verb choice, pacing — while *no character ever names it*. Get this wrong and the frame collapses.
- **Editor actions:** in any scene with both System-user and anomaly skill executions, verify (a) prose rhythm carries the texture difference without a character naming it, (b) cost reads synthetic for System users and embodied for Nate, (c) Nate's HUD reads less while his effect reads more, (d) no character articulates a difference they should not yet perceive. Flag violations.
- Memory: `project_forge_system_as_corruption_of_original.md`

### True Names & False Labels (Codex: True Names & False Labels)

Pre-Sealing names carry identity-power; the System overlays *labels* on top of originals. Aligned operation = un-mislabeled use. Cf. Tolkien Quenya-as-angelic-language, Le Guin Old Speech, Genesis-Adam naming, Isaiah 43:1, Mark 5 Legion, Revelation 2:17.

- **Three name-tiers:**
  - **True names** (Labyrinth-delivered, pre-Sealing): faculty identities (Nate's stockman's sense, his maker's eye, his pattern-reading), vocational callings, true bonds (the pack-bond), Spirit-direct Gifts.
  - **Labels** (System-issued, overlays): class designations (Vanguard, Warrior, Beast Master), bolded skill/ability nameplates (Fire Bolt, Field Repair), ranks, status flags, all bold-text System UI vocabulary.
  - **Mixed cases:** a true-name faculty can sit under a System label; the user *feels* the true thing when aligned.
- **Two-tier naming for Nate's faculties:** common name stays rancher-authentic and in-character (e.g., "stockman's sense" — cattle-rancher universal — NOT "shepherd's-eye" which is sheep-coded). The Labyrinth-true name (capital, codex-tier) carries Tolkien-Rohirric weight (e.g., **Heordsight**, **the Wardenship**) and surfaces in prose only when earned (Book 2+).
- **Mechanic consequences:** Conduit overflow = un-mislabeled use (System caps are calibrated to labels, not the true thing underneath). Allegiance routing under a label routes worship/credit through the label-issuer; true-name use routes correctly to the Source. Demonic name-extraction (Mark 5: "What is your name?" "Legion") is an available sub-mechanic.
- **Editor actions:**
  - Flag any "unbranded" / "nameless" / "without a name" applied to a Labyrinth-original. Replace with "the original," "the one already there," "the name beneath."
  - Flag any line where the System or a System-bound character is described as *naming* something for the first time. The System never names; it labels.
  - Class names, skill nameplates, bold System UI vocabulary → label register.
  - Faculty names, vocational identities, bonds → true-name register.
  - "**re-**" prefix verbs ("re-shelved," "re-skinned," "re-categorized") and spatial "**over**" preposition ("a label sliding into place *over* the original") are grammatical signatures of false-naming — preserve when present.
  - Confirm Nate-faculty common-names aren't out-of-group for a cattleman (no "shepherd" for sheep-coded faculties).
  - "True name" as explicit term must NOT surface in Book 1 prose. If it appears, flag for cut or hold.
- **Villain palette extension:** false-naming is the System's signature corruption. Villains *call things by the wrong name* (a Beast Master "owns" his "**Companion**"; a Conduit-aligned bonded pair *knows each other by name*).
- Memory: `feedback_true_names_and_labels.md`; codex: `True Names & False Labels` (pending forge ingestion — research/true-names-and-false-labels.md is canonical until then)

### Soul-DNA Architecture & Job Effect (Codex: Soul-DNA Architecture)

Cosmology architecture — refines (does not contradict) unified-source theology. Soul (humans only) holds only YOU + Spirit (if invited). Mind ≠ soul; rooms (Flint's, Rex's, Judge's, family, faith) live in the mind, soul-authored via DNA. System cannot enter the soul, period.

- **Two paths to DNA:**
  - **Path 1 (private):** soul → fiber → DNA. Only the soul writes here. Spirit-direct Conduit Gifts use this path; System cannot see it.
  - **Path 2 (shared, post-Integration):** Labyrinth → fiber → DNA. The System has hijacked-overlay-access to this path. Spirit-firewall sits at the soul's gate to it.
- **Spirit-firewall = three modes (intelligent, sovereign, NOT binary):** *block cold* (System overwrite of soul-authored region — Ch2 void-scene defense), *allow with rewrite* (System install in a new DNA-slot; Spirit rewrites the result — Flint is born here), *pass* (legitimate Labyrinth skill-delivery).
- **Job effect:** firewall mode is chosen by sovereign decision, not rule. God allows what serves His purpose (Job 1-2 template). Spirit-indwelt characters can suffer real cost. Permission is the frame, not protection.
- **Bonded-animal DNA-node:** when Nate bonds Rex/Judge, his DNA gains a node carrying the dog's pattern. Respawn-instructions for the dog route through Nate's domain (Genesis 1:26-28 Adamic dominion, Genesis 2:19-20 naming). Beast Master "Companion" bond is System-installed-DNA-only — different mechanism, no soul-authored node, no capacity to deepen.
- **Editor actions:**
  - Flag any prose implying the System enters or writes to the soul. Correct: System overlays DNA via Path 2; soul defends soul-authored regions via Spirit-firewall.
  - Flag any prose putting Flint, Rex, Judge, or other guests in the soul. Rooms live in the mind, soul-authored. Soul-residents are YOU + Spirit only.
  - Flag any prose framing Conduit power as immunity / force-shield. Permission is the frame, not protection. Spirit-indwelt characters can be hurt and lose.
  - Flag any prose framing bonded-dog respawn as the dog's own DNA self-restoring. Pattern routes through Nate's DNA-node domain.
  - Storyteller-omniscient (Hiberno) may hint at Job-effect ("Sure, He sees the whole of it. He always does." / "Some things ye'll find Himself allows.") — verify any apparent Spirit-failure on a Conduit reads as sovereign permission, not mechanical failure.
  - **Open in prose:** "soul," "DNA," "Spirit" (rationed in close-third Nate). **Held shorthand only — flag if surfaced:** "Path 1," "Path 2," "Spirit-firewall," "Job effect," "DNA-node," "fiber-channel," "block-cold / allow-with-rewrite / pass."
- Memory: `project_forge_soul_dna_architecture.md`; codex: `Soul-DNA Architecture (Job Effect)` (pending forge ingestion — research/soul-dna-architecture.md is canonical until then)

### Genre Contract (LitRPG Reader Expectations)

The reader brings a LitRPG contract to the page (system panels, progression payoff, tutorial logic, stat reveals). `LITRPG_CONVENTIONS.md` (repo root) records, for each convention, whether forge-novel **honors / bends / breaks** it and why. This is a *reference, not a rule* — it yields to canon, craft, and the audiobook tiebreaker.

- **A recorded break is correct; an unrecorded stance shift is a finding.** The editor scans for *unintended* breaks only — places where the prose drifts into a stance the doc does NOT record.
- **Five drift flags to scan:** stat-sheet bloat (block >~6 lines or spreadsheet paragraph), mid-action level-up/"ding," loadout-optimization scene (a recorded BREAK — honoring it is the error), System-as-neutral-tech drift (theology spine), first-person leak (a stretch that loses the Storyteller and reads as flat genre first-person).
- **The four signature divergences are load-bearing, not bugs:** theological spine, omniscient Storyteller, audiobook-primary, interface restraint. Never flag these as errors.
- Reference: `LITRPG_CONVENTIONS.md`

## Pass Structure

Run the passes in the order given; complete each fully before starting the next.

### Pass 0 — Slop Detection (0a deterministic, 0b judgement)

Run BEFORE any editorial content review. AI writing patterns survive prompt engineering — this pass catches them in two phases: a deterministic linter, then a reading-comprehension sweep for what the linter cannot measure.

#### Pass 0a — Deterministic lint (run first; zero judgement, zero tokens)

Before reading the chapter for slop, run the linter via the Bash tool and capture its report:

```
python c:/Workbench/dev/forge-novel/kit/prose_lint/prose_lint.py drafts/chNN-*.md --format text
```

- The linter output is **ground truth for locations.** Every FAIL and WARN carries an exact line number — trust it; do not re-derive locations by reading.
- It already catalogs the measurable tells: em-dash density, banned Tier 1/2 vocabulary, "not just X but Y" and "it wasn't X, it was Y" constructions, fiction-tell phrases, sentence-length burstiness (CV), participial-phrase stacks, transition-word clustering, consecutive same-ending sentences, tricolon density, paragraph uniformity.
- **Em-dashes on audiobook-locked chapters:** the linter reports these as INFO, not FAIL — that is correct. Do NOT propose stripping em-dashes from a locked chapter; per `WRITING_RULES.md` they are deliberate Brigid TTS stutter-fixes. If em-dash density looks high on an *un-locked* chapter, carry it as a WARN for David's decision — never auto-strip.
- The linter's word lists are parsed live from `anti-slop.md` in the `forge-write` skill's `references/` folder — the single source of truth. If a word needs adding, edit that file.

#### Pass 0b — Judgement slop review (the model's job)

Pass 0a has already found every word-level and measurable-structural tell. Pass 0b covers ONLY what requires reading comprehension — do NOT duplicate linter findings:

- **Over-explain** — does the Storyteller restate what the scene already showed? Cut the explanation; trust the image.
- **Dialogue polish** — does every character speak in complete, polished sentences? Add imperfect lines (at least one per scene).
- **Scene-summary balance** — is 70%+ of the chapter in-scene (moment by moment), not summary?
- **Stability trap** — do conflicts resolve too cleanly? Does every choice carry real cost?
- **Predictable emotional arcs** — do beats arrive on schedule with no deviation? Include one moment that surprises.
- **Repetitive chapter endings** — does this chapter end on the same structural move as an adjacent one?

**Output:** Flag each finding with location and severity. Do NOT fix anything in Pass 0 — catalog only. Fixes happen after all passes are complete, grouped by chapter.

### Pass 1 — Length Discipline (Prose Must Earn Its Place)

**Run this BEFORE comedy punch-up.** Trim first so the punch-up has less surface area to work on — denser voice-work per kept paragraph without ballooning total length.

1. For each paragraph, apply the earn-its-place test (see Prose Must Earn Its Place rule above).
2. Mark each paragraph as **KEEP** (earns place), **TRIM** (has a kept core plus cuttable hedges/lists/repetitions), or **CUT** (fails the test entirely).
3. For each CUT, note the failure mode: restating-shown-action / list-redundancy / epistemic-reassurance / voice-redundancy / hedge-Nate-doesn't-need / physical-detail-no-return.
4. For each TRIM, mark the specific sentence or clause to excise.
5. Hold the counterweight in mind: voice density is load-bearing. A Flint absurdist stack or Storyteller aside carrying Dial 4-5 register is NOT fluff. Flat diagnostic repetition IS.
6. **Present findings before applying** — user picks which cuts to commit.

### Pass 2 — Continuity & Flow
- Check against adjacent chapters for duplicated scenes, contradictions, timeline issues
- Verify callbacks are consistent (pump, mockingbird, Congressman, etc.)
- Check character positions and inventory carry over between chapters
- Flag any scene that's written twice (especially at chapter boundaries)

**Timeline ground-truth diff (append-only continuity log).** The recorded
in-world history lives in `timeline.json` (Book layer; see `kit/README.md`). It is
**append-only** — sealed events are never edited. Two deterministic moves bracket
this pass:

1. **Read the record, diff the draft against it.** Run
   `python kit/timeline/timeline.py events --chapter <N-1>` (widen the range —
   e.g. `--chapter 1-7` — for older callbacks) to print the events already
   recorded. Diff the draft against them: a contradiction (a death un-died, a
   meeting that already happened, a place/time that doesn't line up) means **the
   draft is wrong**, not the record. Flag it as a continuity finding. The semantic
   diff is your judgement; the tool only surfaces the ground truth.
2. **After the chapter passes, append its new events.** Add one record per new
   in-world event to `timeline.json` (ids `ev-chNN-NN`, in chapter order) and run
   `python kit/timeline/timeline.py check`. A **[BREACH]** (exit 3) means a sealed
   event was edited or deleted — revert it and **append a superseding event**
   instead (name the old id in `supersedes`). Never edit history to fit a draft.

### Pass 3 — Rule Compliance
- Scan for lens labels (the [X] in him)
- Check bold formatting on all System terms
- Verify SA is spelled out at proper intervals
- Check POV discipline — does Nate know anything he shouldn't?
- Check Rex bond delivery — impressions not explanations; pack-bond translation lexicon in Nate's voice channel
- Check Storyteller weave — woven throughout, not bookended; flag any dead-middle stretch (no fixed count)
- **Grep for known nicknames** (King, Sarge, Boss, Pretty, etc.) — cut any that appear before their planned introduction beat
- **System-as-corruption check** — in any scene with System-user and anomaly skill executions side-by-side, verify texture/cost/completeness contrasts are carried in prose rhythm, not dialogue or interiority
- **Dresden coexistence check** — identify every dramatic pivot in the chapter and mark them as PROTECTED before Pass 4
- **Flint design-intent throttle check** — in early Book 1 chapters, verify every Flint design-intent claim carries a hedge ("if the spec sheet I can read is any guide...")
- **Pack-bond faculty check** — Flint never hears Rex or Judge. If he comments on pack-bond traffic, cut the line. Different faculty, architectural rule.
- **Lord's-name-in-vain scan (absolute, all voices)** — see Editorial Rules §1 for the full rule + palette. Grep every voice (incl. villains, demonic entities, and Storyteller-Hiberno) and substitute from the palette.
- **Nate spoken-profanity count** — count Nate's vocalized profanity (dialogue + audible exclamations only — NOT interior thought, NOT italicized direct thought, NOT POV-prose). Cap is 3-5 per ~5,000 words. If chapter exceeds and the chapter is over 5k words, flag for trim. If chapter is under 5k, prorate (e.g., 2,500-word chapter ceiling is roughly 1-3 spoken instances). Excess interior profanity is NOT a finding.
- **Hiberno-English register check** — see Storyteller Voice §Omniscient register for the full rule. Classify each Storyteller passage and flag any that reads cross-register (omniscient must carry a Hiberno marker; physical-zoom must carry none).
- **True-name discipline check** — see Editorial Rules §True Names & False Labels for the full rule. Grep for "unbranded/nameless/without a name," System-as-namer, and the explicit term "true name"; verify rancher-authentic common names (stockman, not shepherd).
- **Genre-contract drift scan (light)** — see Editorial Rules §Genre Contract. Scan for the five *unintended*-break flags (stat-sheet bloat, mid-action level-up, loadout-optimization scene, System-as-neutral-tech drift, first-person leak). A recorded honor/bend/break in `LITRPG_CONVENTIONS.md` is correct — flag only stance shifts the doc does not record.

### Pass 4 — Comedy Punch-Up (Dial 4-5 Calibration)

**Run AFTER Pass 1 trim and AFTER Pass 3's protected-beat identification.** Never punch up a protected dramatic pivot.

1. For each paragraph NOT marked protected, apply the per-voice dial matrix (Nate dialogue 3-4, Nate close-third 4, Storyteller-omniscient 4-5 variable, Storyteller-physical-zoom 4 in normal mode / 2-3 in combat mode, Flint 5, pack-bond translations 3).
2. Where the current register is below target, rewrite using the Dial 4+ landing rules: specific nouns, stacked 2-3 punchlines, named targets, italic breaks on absurdist beats, Flint running full.
3. **Canonical reference beat for the target register:** the Ch 4 scrolling-suit-guy beat (the Karen / customer-service stack) — see `voice/exemplars.md`. Measure against it.
4. Leave protected beats at their original (often Dial 1-2) register. The contrast is the signal.
5. After punch-up, re-run a light Pass 1 sanity check on the rewritten paragraphs — comedy punch-up can smuggle in new fluff (stacked beats that don't escalate, Flint lines with no new theatricality). Cut any that fails earn-its-place.

### Pass 5 — Prose & Voice
- Storyteller tone appropriate to chapter position and mode (omniscient vs physical-zoom)? **Register check:** omniscient passages carry Hiberno-English markers; physical-zoom passages stay plain literary English (see Hiberno-English Omniscient Prose rule).
- Flint voice consistent (theatrical, fast, vulnerable in quiet moments; design-intent hedged in early Book 1)?
- Nate voice consistent (few words, precise, ranch/engineer/gamer vocabulary)?
- Pack-bond translations (when Rex or Judge in-scene): Scots lexicon for Rex, Aussie lexicon for Judge; Flint never commenting on pack-bond?
- Josie voice consistent (fast, cataloging, professional enthusiasm)?
- Marcus voice consistent (clipped authority, reads rooms)?
- **Voice transition read-aloud test** — walk every Storyteller ↔ Nate ↔ Flint ↔ pack-bond-translation handoff and ask: does the shift flow in audio, or does it collide? For rough transitions, apply tonal bridge, grounding re-anchor, or self-contained fragment fixes (see Voice Transition Flow rule above). Flag any transition where the returning voice opens on a fragment or pronoun whose antecedent is on the other side of an interlude.
- **Callback fragment grounding** — scan the chapter for fragments that echo wording from earlier Storyteller lines. For each match, ask: in audio, would the ear know the fragment is interior (Nate) or exterior (Storyteller)? If the answer depends on whitespace or paragraph positioning, the grounding is page-only — ground the fragment in a character action that *produces* the echoed beat (eye sweep, reflexive count, gesture). See Voice Transition Flow technique #4.
- **Sentence-length variation (burstiness)** — read for sentence-length variation. If three or more consecutive sentences cluster at the same length, the prose is flattening — break the run with a short punch or a long build. Uniform medium-length sentences are the clearest structural AI tell. Cross-check against the linter's burstiness CV from Pass 0a: target ≥ 0.7; the linter WARNs below 0.55.

### Pass 6 — Report
Merge the Pass 0a linter findings with the editorial findings from Passes 0b-5 into one table. The `Source` column marks which findings are deterministic (linter) and which are judgement (editorial), so David can see at a glance which is which:

| Category | Chapter | Issue | Severity | Location | Source |
|----------|---------|-------|----------|----------|--------|

`Source` is `linter` (from Pass 0a) or `editorial` (Passes 0b-5). Then ask before making edits. Group edits by chapter for efficiency. Every prose rewrite you propose is itself prose — never inject a bullet, header, or bold-for-emphasis into a narrative paragraph as a "fix."

## Important

- **Edit draft01 files directly** — git handles versioning, no draft02 files
- **Work on local files first** — sync to other repos after changes are committed
- Chapter files live at: `C:\Workbench\dev\forge-novel\drafts\chXX-*-draft01.md`
- MD036 linter warnings on italic prose are irrelevant for fiction — ignore them
