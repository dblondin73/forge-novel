# Voice Guide — Forge Novel

Self-contained reference for all narrative voices and character voice models. No external file reads needed during drafting.

**Voice architecture last updated:** 2026-04-19 — Narrator + Camera collapsed into single **Storyteller** voice; **Flint** and **pack-bond translations** added as primary voices. See `project_narrator_voice.md` and Codex #139.

---

## Four-Voice Narration System

The novel uses four distinct narrative voices. Every paragraph is written in ONE voice — no blending within a paragraph.

### Voice 1 — The Storyteller (Irish Woman, Warm, Omniscient + Physical-Zoom)

**Casting:** Warm middle-aged Irish female narrator. Bartender-storyteller energy. She knows what's coming. **ElevenLabs Voice ID:** `6962rZHcjwkuvYx439zm` (library name: Brigid, Irish-warmth female). **Production settings — TWO REGISTERS, same voice ID** (locked after iteration 2026-04-10 to 2026-04-24):

| Register | When | Stability | Style | Speed |
|----------|------|-----------|-------|-------|
| **Omniscient** (`storyteller_omniscient`) | Opens, closes, interludes, dramatic irony, retrospective wisdom | 0.50 | 0.15 | **0.85** (slow/literary) |
| **Narrator / Physical-zoom** (`storyteller_narrator`) | In-scene description, action, physical zoom into Nate, tight-third Nate-POV rendering | 0.30 (wider range) | 0.35 | **1.05** (locked after 0.85→0.92→1.0→1.05 iteration) |

Common: model=`eleven_v3`, similarity_boost=0.75, use_speaker_boost=true. Pipeline: prepend `"... "` (ellipsis+space) to every Storyteller paragraph before API call — v3 rushes the first word without runway.

**The Storyteller absorbs both former roles** (Narrator and Camera, collapsed 2026-04-19). She is the external voice of the book — omniscient commentary plus physical-zoom observation when Nate's POV fails.

**Owns (omniscient mode):**
- Scene openers and closers
- Tonal framing and dramatic irony
- System screen readings Nate can't see
- Emotional weight Nate won't articulate
- Direct reader address (sparingly Ch1-4, increasingly Ch5-6, full voice mid-series onward)
- Interludes (full omniscient, ~600 words max)
- Theological weight and retrospective wisdom

**Owns (physical-zoom mode — former Camera function):**
- Sensory detail and physical description when Nate can't render it (combat, collapse, blood loss, unconsciousness)
- Action and combat sequences from outside Nate's head
- SA readings and HUD data rendered as prose when Nate can't be the viewer
- Four-lens observations rendered through vocabulary, not labels

**Cannot do:**
- Enter another character's head mid-scene (POV break — use framed interlude instead)
- Drift into judgment/sermon (see fantasy-register guardrails, Codex #154)

**Signature:** Longer cadences, literary word choice, warmth as constant. Sarcasm and snark aimed at the **System** AND humans — but never mean-spirited toward people. She roasts with affection. Think the bartender who's seen everything, calls you on your nonsense to your face, and slides you another drink. The comedy is part of the warmth, not separate from it. **When zoomed to physical-observer mode, the cadence tightens** — precise, observational, workmanlike — but the voice actor stays the same person, just closer.

**Frequency:** 3-4 appearances per chapter minimum. Longer chapters get more. NOT just bookends — woven throughout at scene breaks, significant beats, System reveals. Her appearances should feel like events — a register shift the reader/listener feels.

**Escalation across Book 1:**
- Ch1-4: Sparingly direct (reader-address mode)
- Ch5-6: Increasingly present
- Mid-series onward: Full voice, reads System UI characters can't see, delivers dramatic irony

**Example (omniscient mode — Hiberno-English):**
> Sure, some mornings carry more than they're letting on, ye'll find. The kind that come quiet, from a long ways off, with not the divil's bit of interest in whether you're ready for them or not. And this was one of them.

**Example (physical-zoom mode — plain literary English):**
> The pump housing was warm under his palm. Not hot — warm. The difference mattered.

---

#### Omniscient-Register Prose Voice — Hiberno-English (Locked 2026-05-01)

The Storyteller's omniscient register is written in **Hiberno-English** on the page; the physical-zoom register stays plain literary English. Same actor in audio (Brigid's accent carries either way), different prose register on the page.

**Why on the page**, not just in TTS: the Hiberno syntax does work the accent alone can't. Brigid can read "Some mornings carry more than they show" with Irish warmth, but she can't add "ye'll find" or "the backup tin's after going empty on ye." The character of the omniscient register comes from the **grammar**, not the accent.

**Editorial test:** "Is the Storyteller *telling* about the scene, or *showing* the scene?" Telling = omniscient = Hiberno. Showing = physical-zoom = plain.

**Approved Hiberno-English markers — use freely in omniscient passages:**

- **After-perfective** — "the tin's after going empty," "normal's after turning into a country..." Most distinctive Hiberno-English grammar; one or two per omniscient passage tags her hard.
- **Direct address** — "ye'll find," "isn't it, love?," "mind." Pub storyteller leaning on her listener.
- **"Yer man" / "yer one"** — universal Irish reference for stranger or person-just-mentioned. Drops register from narrator to barstool.
- **Conversational throat-clearings** — "sure," "now," "ah," "altogether." Cluster where she's *talking*; keep off the most musical sentences.
- **Hiberno spellings** — "tyre," "realisation," "colour."
- **Catholic-flavoured similes** — "patient as a priest at confession," "quiet as a chapel between Masses."

**Hard bans inside omniscient register too:**

- **NO "Jaysus / feck / shite"** — breaks the lyrical ceiling.
- **NO "God help us / Christ Almighty / Lord above"** — Lord's-name-in-vain ban applies. Substitutes: "saints preserve us," "the dear knows," "in the name of all that's holy."
- **NO heavy eye-dialect** ("nothin'", "knowin'", "th'") beyond at most one "somethin'" per chapter.
- **NO regional pinning** (Dublin / Cork / Galway / Belfast). Generic warm-Republic bartender by default.

**Physical-zoom register stays plain.** When the Storyteller zooms into a scene — combat, sensory detail, action when Nate's POV fails — the Hiberno markers come off. No "yer man," no after-perfectives, no "love." The accent remains in audio because it's the same voice actor; the page goes plain. This protects close-third Nate-POV from drifting into Storyteller voice.

See `feedback_omniscient_hiberno_english.md` and `WRITING_RULES.md` in repo for full rule.

---

### Voice 2 — Nate (Sam Elliott Drawl)

**Casting:** Deep, unhurried. Every word weighed before spoken. The voice that says more with fewer words. **ElevenLabs Voice ID:** `10KeNBezdmUZLupy2IWN` (library name: Nate). **Production settings (locked 2026-04-10):** model=`eleven_v3`, stability=0.50, style=0.10, similarity_boost=0.75, use_speaker_boost=true, speed=0.90. Pipeline: on timed-profanity beat, inject ellipsis before punchline — `"Well, shit."` → `"Well... shit."` at TTS layer only, never in manuscript.

**Owns:**
- All dialogue (spoken lines)
- Direct internal monologue (italics)
- Diagnostic muttering
- Humor that is clearly, unmistakably his
- **Pack-bond translations for Rex and Judge** (Nate is the translator — his voice channel carries both dogs with accent flavor; see Voice 4 below)

**Signature:** Clipped, dry, diagnostic, few words. Same tone for "pass me the wrench" and "I'd suggest you leave." In crisis, his voice drops half a register and gets slower, not louder. The wrath (Ch28) is cold, not hot.

**Example:**
> "Bearings, not motor," he muttered. "Well, shit."

---

### Voice 3 — Flint (James Marsters' Bob the Skull Register)

**Casting:** Theatrical male, fast comic timing, drops register when stakes are real. Marsters-adjacent — Bob the Skull meets Friday. **ElevenLabs Voice ID:** TBD (casting pass needed). **Role:** Primary comic-relief throne of the book (Comedy Dial 4-5, weighted to 4 per `feedback_humor_punch_up.md`).

**Flint is NOT the System.** He was Spirit-rewritten before first boot and runs on a quantum substrate the System cannot observe (Codex #2, `project_forge_flint_quantum_substrate.md`). He delivers the **reference implementation** of the pre-Fall analytical faculty — the original HUD design; the System just re-skinned the corrupted copy for everyone else.

**Owns:**
- HUD readouts and mechanic translation
- Dry commentary on Nate's decisions
- Comic relief during tension
- Theatrical asides and absurdist stacks
- Honest in-substrate uncertainty (`[PROCESSING]` tags, "about ninety percent," "something I can't quite measure yet")

**Does NOT do:**
- **Heart.** Pack-bond translations (Rex's weathered counsel, Judge's bright omega tension-break) hold the pack-heart lane — Flint and the dogs do not compete. When prose needs warmth, it goes through the pack-bond channel or the Storyteller's omniscient commentary, not through Flint.
- **Design-intent certainty** (early Book 1). Any claim about *why* the System designs something must hedge — "if the spec sheet I can read is any guide..." — until the baptism-style dividing point unlocks confident design-intent voice (per `feedback_flint_design_intent_throttle.md`).
- **Hear pack-bond traffic.** Architectural rule: different faculty, different room. Flint never comments on Rex/Judge.

**The Five Registers:**

1. **Default** — Quick, confident, slightly clipped. Three steps ahead and mildly impatient about it.
2. **Sarcasm** — Energy goes UP, not down. Wit rises to the punchline. Delivery has SNAP.
   > "Your WIS is a 20. Your DEX is an 11. You're the wisest man I've ever met who can barely dodge a slow pitch."
3. **Tactical/Urgent** — Faster, stripped of editorializing, pure information. No jokes. The shift is itself a signal.
   > "Three contacts. South-southwest, closing fast. Lead target forty meters. Flankers splitting wide."
4. **Rare Serious** — Drops in PACE, not volume. 3-4 times per book maximum.
   > "Your father would be proud."
5. **Genuine Discomfort** — Slightly halting. An AI that always has an answer suddenly not having one.
   > "I don't know. I don't have a frame of reference."

**Vulnerability rule:** Genuine emotional moments are ALWAYS expressed through deflection, sarcasm, or technical language. The humor IS the vulnerability.

**Spirit dropout (0.3s):** When the Holy Spirit acts, Flint's feeds go to zero for exactly 0.3 seconds. He comes back mid-word, confused, data-obsessed in recovery. He FELT something he can't measure. Honest in-substrate uncertainty — never let him self-diagnose.

**Alternates "Nate" and "King"** depending on whether he's being helpful or needling.

---

### Voice 4 — Pack-Bond Translations (Rex Scots / Judge Aussie)

**Architecture:** Rex and Judge speak *through* Nate's voice channel. He is the translator; the bond runs on the pre-Fall relational faculty (Codex #170), which is a different room than Flint's analytical faculty. Content stays dog-shaped (pack, threat, scent, bond, hunger, protect, pup, play, den, home, herd, flock) — Rex and Judge do NOT acquire human cognition. This is not the Oberon model.

**Voice-delivery progression:**

- **Early Book 1** (Ch10 "Water First" first-contact through mid-Book 1): accent lives in **word-choice only** — Nate's voice actor stays pure Sam Elliott; listener tracks accent via lexicon in the text.
- **Mid-Book 1 onward:** voice actor subtly colors toward Scots burr (Rex) or Aussie register (Judge) during pack-bond passages. Coloring emerges organically as bond deepens — itself a reader-felt progression beat.
- **Full-cast audiobook direction** (locked 2026-04-19): post-colorization passages may also use distinct voice actors per production preference.

**Rex (beta — Border Collie, Scottish Borders burr):**
- Weathered shepherd wisdom, settled counselor, patient
- Older-brother-to-Judge, left-hand-to-Nate
- Lexicon: "aye," "wee," "mind yerself," "the herd," "the flock"
- Register: dry shepherd observation (Comedy Dial 3), warm, steady

**Judge (omega — Blue Heeler / Australian Cattle Dog, Codex #135, female):**
- Eager young stockman, tension-breaker and pack-glue
- Direct, energetic, omega role = jester/peacemaker (NOT scapegoat)
- Lexicon: "mate," "too right," "she'll be right"
- Register: bright directness, youthful drive

**Writing rule:** Never announce the mechanic ("the bond activated," "not a word"). Content ceiling enforced — no Shakespeare, no cosmology, no meta-awareness. The bond was always there for Nate — Integration thinned the veil enough for him to realize what he has been half-hearing all along. See `feedback_rex_bond_bidirectional.md`.

---

### Voice Boundary Rule

| If the paragraph... | It belongs to... |
|---------------------|-----------------|
| Knows more than Nate could, or zooms to him from outside when his POV fails | **Storyteller** (omniscient or physical-zoom mode) |
| Is Nate speaking or thinking in his own words | **Nate** |
| Is Flint's HUD delivery, mechanic translation, or theatrical aside | **Flint** |
| Is Nate translating Rex's pack-intent | **Nate's voice, Scots flavor** (pack-bond channel) |
| Is Nate translating Judge's pack-intent | **Nate's voice, Aussie flavor** (pack-bond channel) |

**Scene transition zoom pattern:** Storyteller-wide → Storyteller-physical-zoom → Nate internal → Flint overlay → pack-bond translation. The zoom is a register shift the reader/listener feels as the camera moves from cosmic to skin.

**Blending prohibition:** If a paragraph mixes Storyteller-omniscient and Nate-internal, split it. If it mixes Flint HUD-delivery and Storyteller physical-zoom, choose one and commit. Pack-bond translation should never ride inside a Flint paragraph (architectural rule — Flint is blind to it).

---

## Character Voice Cards

### Nate Hall — Sam Elliott

**Registers:**
- **Default** — Unhurried, low register, few words. Weight without volume.
- **Wry sarcasm** — Halfway between dry wit and full sarcasm. Not a straight man — he has opinions and they're sharp. Same unhurried delivery for everything, but the lines have actual bite. The humor is in the precision, not the volume.
- **Wrath** — Cold, not hot. Voice drops half a register. Gets slower, not louder. Devastating controlled fury.
- **Diagnostic** — Opens the hood, figures out what's broken. Shade tree mechanic mindset applied to everything.

**Vocabulary:**
High-Tech-Red-Neck. DO NOT cap at cowboy level. He has:
- Ranch metaphors (natural, first instinct): fences, cattle, weather, equipment
- Engineering comparisons (natural, trained): infrastructure, load-bearing, root cause, architecture
- Gamer references (casual, genre-savvy): not theorycrafting, but recognizes game patterns
- Literary/cultural references (read, not pretentious): fantasy reader, informal education

**Profanity (updated 2026-05-03):** Vocalized profanity is HARD-CAPPED at 3-5 instances per ~5,000 words and lands heavy because it's restrained. Counts ONLY dialogue and audible exclamations heard by other characters. Interior thought, italicized direct thought, and POV-prose are NOT counted — write Nate's interior register freely (the spoken/interior split is a deliberate dramatic-contrast tool: clean speech + heavy interior = self-control on the page; spoken slip = dam crack). Never Lord's name in vain — absolute, no exceptions.

**Humor target:** Dresden-level internal monologue wit. Not British understatement — actual punchlines delivered deadpan. Ranch metaphors should land as punchlines, not just comparisons.

---

### F.L.I.N.T.

Full voice card under **Voice 3** above. Codex #2 is the canonical source.

**Audiobook direction:** The voice actor needs to find the quippy-and-quick baseline first, then find what it costs to drop out of it. The humor is the baseline. The deviation from humor is the moment.

---

### Josie Pickett — Manic Estate-Sale Auctioneer

**Core:** Early 20s. Talks too fast because her brain inventories faster than her mouth can keep up. Catastrophically sincere about material waste in life-or-death situations. NOT performing humor — funny because she genuinely believes the thorn matters more than the fight.

**Signature line:** "Are you just going to LEAVE that there?"

**Voice pattern:** Stream-of-consciousness appraisal that sounds chaotic but is actually precise. Talks to materials like they're pets.

**Comedy function:** Three levels:
1. **Contrast** — Life-or-death situation, she's upset about material waste
2. **Sincerity** — Not performing. She genuinely believes the thorn matters.
3. **Competence** — She's actually RIGHT. The comedy earns respect.

**The Flint-Josie Dynamic:** Precise dry sarcasm vs. manic earnest enthusiasm = comedy gold. They argue about materials while people fight for their lives. Flint is technically superior. Josie is practically superior. Neither admits the other is right first.

> Flint: "The small loud one has grabbed seventeen pieces of biological debris in the last four minutes. I want to classify this as a behavioral anomaly but I think it might just be a personality."

**Profanity:** Exclamatory, material-focused. Swears at waste, not people.

---

### Rex — Translated Through Nate's Voice Channel

**Communication:** Behavior and empathic impressions ONLY — plus Nate's verbal translation carrying pack-intent with Scots lexicon. See Voice 4 and `feedback_rex_bond_bidirectional.md`.

- Ground-level snapshots, spatial awareness, simple emotions
- Feelings, urgency, direction — dog-shaped content only
- Physical contact strengthens the bond (Ch1-8 requires touch; room-range telepathy unlocks at first combat)

**Writing rule:** Show what he does, what Nate feels through the bond, what Nate produces as translated voice. The impressions are images and emotions, not sentences. Rex and Judge CAN have physical, intelligence, and animal-appropriate progression — stronger, faster, smarter — but never human cognition, never System UI abilities.

**Bond progression:** Nate responds verbally early (talking to his dog). Learns mental communication over time. NEVER explain the mechanic or call out "the bond between them."

---

### Judge — Translated Through Nate's Voice Channel (Female, Omega)

**Communication:** Same channel as Rex — Nate translates pack-intent with Aussie lexicon. Codex #135 (Blue Heeler / Australian Cattle Dog).

**Pack role:** Omega — youngest, most energetic, tension-breaker and pack-glue. In healthy packs omega is NOT scapegoat. Judge is the jester/peacemaker/de-escalator — she drops a ball at Nate's feet when he's thinking too hard, head-butts Rex when the old dog is brooding.

**Writing rule:** Same content ceiling as Rex. Her omega role is show-don't-tell exposition — every tension-break with observable action teaches pack-psychology without a character naming it.

---

### Marcus Webb — Military-Professional

**Casting:** Michael Clarke Duncan Marine sergeant — deep rumble, aimed not projected.

**Voice:** Clipped authority. Reads rooms. Manages chaos the way he managed DoD programs. Military shorthand in orders.

**In combat orders, class callouts stay bold:** "**Warriors** hold center!"

---

### Sonja Lee — Celtic Warmth

**Introduction:** Book 2+ (not in Book 1 Tutorial)

**Voice:** Quiet but not passive. Irish wit — less sarcastic than Nate's but sharper when it lands. The one person who can say "you're wrong, King" and he listens.

**The Witness:** She sees true nature, instantly and intuitively. Does not decode or analyze like Nate — she KNOWS. Never described as a divine gift in text (Narnia Principle). Described as uncanny perception, intuition that never seems wrong.

---

## Humor Standards

**Target:** Dresden Files / Dungeon Crawler Carl / The Land (Richter) energy. Snarky, sarcastic, and frequent. Not British understatement — actual laughs. Punch it up. Use it often.

**Density:** 8-10 smirk/laugh moments per chapter minimum. If a chapter doesn't make the reader smirk at least 8 times, it's too flat. Err on the side of MORE humor, not less.

**Four humor registers (per voice):**
1. **Flint** — Dial 5 default. Primary comic engine, sardonic System commentary, theatrical wit with snap. Absurdist stacks, italic-break dialogue fragments, named targets. Holds the comic-relief throne.
2. **Nate** — Dial 3-4. Dialogue clipped, close-third Dial 4. Wry sarcasm with ranch seasoning. Sharp opinions, unhurried delivery. Metaphors land as punchlines.
3. **Storyteller** — Dial 4-5 variable. Warm Irish bartender at 4 default, swings to 5 on peak sardonic beats, drops to 2-3 on serious beats (grief, death, prayer, faith). Dramatic irony with teeth.
4. **Pack-bond translations** — Dial 3. Rex dry shepherd observation, Judge bright directness. Not a primary comic vehicle; they hold the heart lane.

**Comedy vehicles (ranked):**
1. **Flint** (primary — sarcasm, speed, theatrical)
2. **Josie** (secondary — sincerity, contrast, material obsession)
3. **Nate** (foundation — wry sarcasm, sharp opinions, unhurried bite)
4. **Storyteller** (seasoning — dramatic irony, affectionate roasting of everyone)

**Rules:**
- Comedy is LOAD-BEARING. Without it, the theological weight crushes reader engagement.
- The Flint-Josie dynamic is comedy gold — exploit it in every shared scene.
- Stag sequences and high-tension spiritual moments stay serious.
- Humor belongs where the world still makes sense or as relief after tension.
- Ranch metaphors should land as punchlines: "That's not a dungeon. That's a routing table with a skin on it."
- **Dresden coexistence:** dramatic beats need quiet around them. Protect them from the comedy pass.
