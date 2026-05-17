# Forge Novel — Writing Rules & Editorial Guide

*Companion to REFERENCE.md. REFERENCE.md is the **what** (worldbuilding); this is the **how** (voice, prose, theology-in-craft, audiobook production).*

*Last consolidated 2026-05-01 from local memory. Authority over older rules where they conflict.*

---

## Master Tiebreaker

**Audiobook is the primary medium.** When page-sophistication conflicts with audio-flow, pick audio-flow every time. The series is being produced full-cast in ElevenLabs Text-to-Dialogue, and the listening experience is the deliverable.

Practical implications throughout this document, but the core: punctuation edits on already-TTS'd chapters (fragment joins, em-dashes added) are **stuttering fixes for Brigid (the TTS narrator), not prose regressions**. Don't revert them silently — ask before reverting.

---

## Voice Cast & Audiobook Routing

### Full-Cast Voice System

| Voice | Character | TTS Model Notes |
|-------|-----------|-----------------|
| **Storyteller — omniscient register** (Brigid, Irish-warmth female) | Narrator in opens, closes, interludes, dramatic irony | Slow/literary. ElevenLabs `6962rZHcjwkuvYx439zm`, v3, stability 0.50, style 0.15, similarity 0.75, **speed 0.85** |
| **Storyteller — narrator register** (Brigid, same actor) | Narrator for in-scene description, physical zoom into Nate, action rendering, tight-third POV prose | Dynamic/close workhorse. Same voice ID, stability 0.30 (wider range), style 0.35, **speed 1.05** (locked after iteration: 0.85 → 0.92 → 1.0 → 1.05) |
| **Nate (Sam Elliott model)** | Nathan Hall | Quoted dialogue + italic direct thought ONLY. Stability 0.50, style 0.10, similarity 0.75, speed 0.90 |
| **Flint (Bob the Skull / James Marsters)** | F.L.I.N.T. | All Flint dialogue and HUD-routed reports |
| **Rex (Scots accent, beta-pack register)** | Rex (Border Collie) | Used when Nate translates Rex's empathic impressions to internal voice |
| **Judge (Australian accent, omega-pack register, female)** | Judge (Blue Heeler) | Used when Nate translates Judge's empathic impressions |

### Routing Rules

- **Storyteller is the default.** Use Storyteller voice for narration, description, internal close-third Nate-POV, scene-setters, transitions — almost everything.
- **Nate voice is reserved.** Quoted dialogue and italicized direct thoughts only. Do not route prose narration through Nate's voice even when the prose is in his POV.
- **Pack-bond voices (Rex, Judge)** — only used when Nate is *translating* their impressions to inner voice. When the dogs act without translation, the Storyteller narrates them.
- **Storyteller frequency** — woven throughout each chapter, not bookended. The "3-4 per chapter" count is RETIRED after the Narrator+Camera collapse.

### Omniscient-Register Prose Voice — Hiberno-English (Locked 2026-05-01)

The Storyteller's **omniscient register** (chapter opens, closes, interludes, dramatic irony, retrospective wisdom) is written in **Hiberno-English** to match Brigid's Irish-warmth voice. The narrator register stays plain literary English. Same actor, same voice ID — different prose register on the page.

**Why on the page**, not just in TTS: the Hiberno-English syntax does work the accent alone can't. Brigid can read "Some mornings carry more than they show" with Irish warmth, but she can't add "ye'll find" or "the backup tin's after going empty on ye." The character of the omniscient register comes from the **grammar**, not the accent. The accent is the cherry on top.

**Approved Hiberno-English markers — use freely in omniscient passages:**

- **After-perfective construction** — "the tin's after going empty," "normal's after turning into a country..." This is the most distinctively Hiberno-English grammar there is. One or two per omniscient passage tags her hard.
- **Direct address** — "ye'll find," "isn't it, love?," "mind." Storyteller-as-bartender scaffolding. A pub storyteller leans on her listener.
- **"Yer man" / "yer one"** — universal Irish reference for a male/female stranger or person-just-mentioned. Drops register from narrator to barstool.
- **Conversational throat-clearings** — "sure," "now," "ah," "mind," "altogether." Cluster these where she's *talking* (the wry openings); keep them off the most musical sentences (the river-flood line, the steel-sky paragraph).
- **Hiberno spellings** — "tyre" not "tire," "realisation" not "realization," "colour" not "color." Subtle, but plants her on the right side of the Atlantic.
- **Catholic-flavoured similes** — "patient as a priest at confession," "quiet as a chapel between Masses." Better than literary adjectives. Fits her instinctive frame of reference.

**Hard bans inside the omniscient register too** (theology + audience):

- **NO "Jaysus," "feck," "shite,"** or other Catholic-Irish profanity. Shifts register toward comic/working-class and breaks the lyrical ceiling.
- **NO "God help us," "Christ Almighty," "Lord above,"** etc. — Lord's-name-in-vain ban (rule #3 in Hard Bans) applies inside the omniscient register too. Substitutes that work: "saints preserve us," "the dear knows," "in the name of all that's holy."
- **NO heavy eye-dialect** ("nothin'", "knowin'", "th'") beyond at most one "somethin'" per chapter. Eye-dialect tires across a chapter; her brogue lives in the bones of the sentence.
- **No regional pinning** (Dublin / Cork / Galway / Belfast). She's a generic warm-Republic bartender. If a region gets locked later, the idiom can tighten — but the default is unmarked.

**Narrator register stays plain literary English.** When the Storyteller zooms into a scene — "He crouched beside the dying water pump..." — the Hiberno markers come off. No "yer man," no after-perfectives, no "love." The accent remains in the audio because it's the same voice actor; the page goes plain. This protects close-third Nate-POV from drifting into the Storyteller's voice.

**Editorial test** when unsure which register a passage is in: ask "Is this the Storyteller telling us about the scene, or is this the Storyteller showing us the scene?" Telling = omniscient = Hiberno. Showing = narrator = plain.

### Punctuation as Audio Direction

Punctuation in TTS'd chapters does double duty as audio direction. When fixing a Brigid stutter:

- **Fragment joins** — gluing two short sentences into one with a comma fixes a TTS pause that was breaking the line.
- **Em-dashes added** — replaces a comma where Brigid was stalling on a clause boundary.
- **Periods → commas** — used to flatten an overly-emphatic full stop.

These are **stuttering fixes**, not prose regressions. Never revert one without asking David.

### Callback / Echo Fragment Grounding

A fragment that echoes an earlier Storyteller line must be grounded in character action when used in audio.

**Why**: on the page, whitespace and indent distinguish an interior echo from an exterior repetition. In audio, whitespace doesn't exist. The action becomes the grounding.

**Rule**: if a chapter calls back a Storyteller line as a fragment, attach a small character action ("Nate set the bolt down."), or route it through Nate's voice instead of the Storyteller's.

---

## Pack-Bond Communication

### The Bond is Bidirectional and Selective

- **Pack-bond is a pre-Veil relational faculty** (see REFERENCE.md → Two-Faculty Cosmology). It is NOT a System feature; the System cannot scan it.
- **Selective by calling** — only people with the animal-husbandry calling get it. It is not universal among Anomalies.
- **Bidirectional** — Rex/Judge send impressions to Nate; Nate learns to send impressions back (Books 2+).
- **Flint is blind to it** — Flint cannot read pack-bond traffic. He can SEE the dogs reacting but does not get the empathic channel. This is a recurring source of Flint frustration.
- **Two-channel translation** — Nate translates Rex (Scots / beta) and Judge (Aussie / omega / female) when routing them through audiobook voice.

### Dog Body Language Rules

Real working-dog behaviors only. Hard bans:

- **Never "press their bodies flat"** — not a real working-dog behavior.
- **Never anthropomorphize through human emotional postures** — use real dog tells.

Approved working-dog behaviors:

- **Head-push** — Rex/Judge driving an object or a person with the top of the skull.
- **Plant** — settling weight low and refusing to move; communicates a hard stop.
- **Sentry** — head up, ears forward, weight balanced for a fast pivot.
- **Stalking-pressure** — Rex's herding mode, low and slow, eye locked.
- **Active harassment** — Rex's adapted Tutorial mode against creatures with no flight instinct (darting lunges, nipping legs, bump-and-break).

---

## POV Discipline

### Tight-Third on Nate

- **Nate can only narrate what he can see, hear, sense, or be told.** No omniscient leaks into Nate-POV scenes.
- **System data gets routed through Flint.** If Nate needs to know a number, Flint surfaces it (or the HUD does, and Nate reads it).
- **Show effects, not UI.** A cooldown isn't "Nate's Power Strike enters a 3-second cooldown" — it's the bolt landing, the recoil, and the next half-second where Nate's body knows the swing isn't there yet.
- **Storyteller pullaways** to other named characters are allowed and encouraged, but as discrete short sections — don't smear them into Nate's POV.

### No Lens Labels in Prose

The Four-Lens Model (Codex #92 — Ranch / Engineering / Gamer / Christian) is a writing-guide concept, NOT prose furniture. Hard bans:

- Never write "his engineering brain noticed..."
- Never write "the rancher in him saw..."
- Never write "his gamer instincts kicked in..."
- Never write "the believer in him whispered..."

Show the perspective through what gets noticed, what gets compared, what gets named. The lens is the camera, not a label held up to it.

### No Meta-Labeling of Tutorial Design

Don't label the Tutorial's pedagogical structure in the prose voice. Hard bans:

- "curriculum," "syllabus," "lesson plan," "pedagogy" used in narration.
- Statements like "this room was clearly teaching X."

Show the teaching through events. If Room 3 is teaching team coordination, show three failed attempts and one that works — don't tell the reader the room is teaching team coordination.

### No Internal Lens Style

When characters have unusual perception modes (Nate's SA, Sonja's Witness), **show through the writing itself, never announce it**. The lens is the camera, not the caption.

---

## Theology — Show, Don't Tell (The Narnia Principle)

This is **the most important rule** in the entire document.

### Faith Is Action, Not Internal Monologue

Christianity is shown through **what characters DO**, never through internal sermon. The Narnia model, not the altar call:

- A prayer is a kneeling, a hand on a fence post, a moment of stillness while the dogs settle. Not "Nate prayed silently and felt the Spirit's presence."
- A moral choice is the choice — the cost paid, the action taken. Not the deliberation explaining why.
- Faith-shaped instinct manifests as the choice itself (give up the gear, take the harder path) — never as "his faith told him to..."

### Prayer as Constant Conversational Communion

Show prayer through stillness, posture, the small habits of a man who lives in conversation with God. Never STATE that he is praying.

### The Imago Dei Term Ban

**Never use "Imago Dei" directly in prose.** Use generic references:

- "the way humans were made."
- "what was buried under the Fall."
- "the original design."

The term itself is theology-jargon and breaks the fantasy register.

### The Fantasy Register — Six Bans

Forge-novel sits in the fantasy register (Dresden / Narnia / Stargate target). Hard bans on theology-jargon that breaks register:

1. **"Repent"** — never in prose. Show the turning, not the word.
2. **"Eden"** — by name. "the original design," "the garden the world was supposed to be," etc.
3. **"Lucifer"** by name in early prose — Morningstar / MSG instead. The Isaiah-14 reveal is hidden brand-deep.
4. **"Sin"** in Christian-jargon usage — "drift," "the wrong door," "what he wasn't supposed to do" instead.
5. **"Salvation" / "saved"** — show the rescue, name it after.
6. **"The Holy Spirit"** in early Book 1 narration — "what was already there," "the One who got there first." (Allowed in late-series and in dialogue from believers explaining outright.)

### Lord's Name in Vain — Hard Ban

The forge-novel audience is 18+ and moderate profanity is acceptable, BUT:

- **NEVER take the Lord's name in vain in prose or character dialogue.**
- Don't oversaturate profanity either — it loses weight when overused.
- Show character grit through stronger images, harder verbs, sharper observations — not through bombing the page with f-bombs.

---

## System-Intent Register

### Tight Discipline for ALL Voices in Early Book 1

Through approximately Chapter 8, no voice (narrator, Nate, Flint, anyone) attributes intent / motive / design-logic / cosmic-purpose to the System. The System acts; characters respond. The interpretation comes later.

**Why**: the System-as-counterfeit reveal is the spine of the series. If characters call it out as deceptive in Chapter 2, the reveal has nothing to reveal.

### Allowed (System as AI with Guardrails)

The System IS an AI — normal AI-behavior verbs are allowed across all voices:

- **decides, infers, adapts, watches, responds, optimizes, prioritizes, selects, calculates, displays.**

### Not Allowed (Early Book 1 — Through Ch8)

- **Trap metaphors** — "the System was setting a trap," "the bait was..."
- **Adversary attribution** — "the System wanted Nate to..."
- **Refusal-disguised-as-instinct** — Nate "knew" the System was lying. He doesn't know yet. He feels wrong.
- **Transcendent verbs** — wills, intends, designs (in the cosmic sense), purposes.

### What Nate Can Have (Early Book 1)

**Pure somatic wrongness.** A bad-water feeling at the back of the throat. Skin crawl. The wrongness of a tool that's almost right but not. He doesn't *interpret* it — he just feels it and moves on.

### Flint Design-Intent Throttle

Early-Book-1 Flint has bounded awareness. He hedges all design-intent claims:

- "If the spec sheet I can read is any guide..."
- "Looks like the System's pulling X — but I'm reading from outside the building."
- "Could be design. Could be glitch. Filing both."

The throttle unlocks at a baptism-style dividing point in Flint's arc (precise chapter TBD — late Book 1 / early Book 2).

---

## Nate's Voice & Vocabulary

### Sam Elliott Model

Dry, observational, engineer-brained. Sam Elliott with a systems degree.

### Nate is High-Tech-Red-Neck

**Don't cap Nate's vocabulary at cowboy level.** He has decades of DoD systems engineering work. He knows the words for things — both ranch words and IT-infrastructure words. The voice is the *blend*, not the floor.

### Engineer Lens = IT Systems

Nate's engineer perception routes through **IT systems vocabulary**, not industrial / mechanical engineering:

- **Approved**: dashboards, status screens, telemetry, signal, packet, route, diagnostic, latency, throughput, the wrong process eating CPU, a service flapping, root cause.
- **Banned in prose**: pumps, valves, manifolds, hydraulic, pneumatic, gear ratios. (Mechanical-engineering vocabulary feels wrong on Nate's tongue.)
- **Writing-guide-only, NEVER in prose**: MBSE, NOC, Grafana, SCIF, IATT — these are reference frames for the writer, not words Nate would say.

### Tool Vocabulary — Flag for Review

When unsure of a ranch / farm / trades term, **flag it for David's review** rather than guessing. Specific failure modes:

- **"Baler tines"** not "baler teeth."
- **Material comparisons** — synthetic leather is NOT automatically weaker than hide; carbon fiber rope is NOT automatically stronger than manila. David has the trade-domain knowledge; ask before claiming.

### Ranch Counting Metaphor — Bounded Trigger

The "counting cattle through a gate" metaphor (used for Nate counting threats, supplies, bolts) only fires for one specific image:

- **Approved trigger**: a herd pushing through a single gate or gap. Multiple animals moving through a constraint.
- **NOT a trigger**: a chute (one-at-a-time), a stuck gate (nothing moving), a head-count in a pasture (no movement at all).

Don't reach for the metaphor when the image doesn't fit.

### SA Acronym Expansion

**Spell out "Structural Analysis" periodically** — don't rely on SA alone for the whole book. The acronym is fine after the first use in a scene, but a chapter that uses SA twenty times without ever spelling it out wears the reader out.

### Premature System Conclusions (Early Book 1)

Through approximately Chapter 8, Nate's System unease is **pure somatic wrongness only** — no trap metaphors, no adversary attribution, no refusals-disguised-as-instinct. (See System-Intent Register above for full rule.)

---

## Prose Discipline

### Every Line Must Earn Its Place

Every line must justify itself by doing one of:

1. **Plot** — moves the story forward.
2. **Character** — reveals or develops who someone is.
3. **World** — builds the setting in a way that pays off.
4. **Voice** — establishes or reinforces the narrator/character voice.
5. **Rhythm** — provides a beat, a pause, a breath the audio needs.

Cut on sight:

- **Restating** — saying the same thing twice in different words.
- **List redundancy** — three examples where two would carry it.
- **Epistemic reassurance** — "of course," "obviously," "as expected" leaking into narration where Nate isn't actually thinking that.

This is **Pass 1.5: Length Discipline** in the editor's-hat workflow.

### Numbers Are Atmosphere, Not Audit

Specific-sounding numbers in prose do **rhetorical work**, not audit-grade tracking. "Forty-three survivors crossed into Room 3" is a feel-of-precision device. Don't count survivors against a running tally — if Ch4 says forty-three and Ch7 says forty, that's a feature unless David has flagged the headcount as load-bearing.

The corollary: **don't do bookkeeping in your head while writing**. Atmosphere first.

### LitRPG Pacing — Forward Momentum

Chapters must maintain forward momentum. Avoid passive sequences without stakes or hooks:

- A scene of Nate cleaning gear is fine IF it's setting up the next fight, OR revealing character through habit, OR resolving something from the previous fight. A scene of Nate cleaning gear because it's downtime is a cut candidate.
- Every scene needs **stakes** (something to lose), a **hook** (a reason to read on), or **earned breath** (after a heavy scene, by editorial design).

### Interlude Style

Global interludes (omniscient-POV peeks at the wider world) are a **series-wide style**, not a one-off device. Use them periodically — they're part of the contract with the reader.

---

## System / Magic / Term Formatting

### Bold Only as Proper Nouns

**Bold System terms only when they are naming the thing** (functioning as a proper noun for a System feature):

- ✅ "**Structural Analysis** activated."
- ✅ "His **Engineer** class drew the line cleanly."
- ❌ "He used his **structural analysis** on the wall." (verb / generic — lowercase, no bold)
- ❌ "The **engineers** were arguing." (group / generic — lowercase, no bold)

The rule: bold ONLY when the term is naming the System feature. Group usage and action usage stay lowercase and plain.

### Blue Panels Are Internal

System HUD/screen panels are **private per-user** — invisible to outside observers. This applies ONLY to UI. Magic manifestations (Codex Magic Visibility Split — see REFERENCE.md) are visible.

### System Error Messages — Inline Italicized

Stylistic element retained from Codex #32:

> *ERROR: ALIGNMENT EXCEEDS MEASUREMENT RANGE.*
> *PROCESSING.*
> *RECONSTITUTION DENIED.*

All-caps, italicized, inline. No code blocks, no quote marks.

---

## Pop Culture & Humor

### Pop Culture in Prose (Opened Up 2026-04-19)

Pop-culture references are **OK** for the Storyteller and for Nate. Earlier guidance restricted these; opening up was a deliberate decision to keep the Dresden-energy alive.

**Still banned** — Star Wars / Jedi / Force terminology. Theology collision (Force is a counterfeit framing too close to System for comfort).

**Approved areas**: video games (Diablo, Skyrim, WoW, Destiny, XCOM), TV (Yellowstone, Stargate), tabletop (D&D), generic fantasy (Tolkien-derived), cattle/ranch culture references.

### Comedy Dial — Per-Voice Matrix

Target dial: **4–5, weighted toward 4**. (Dresden territory, just below DCC.)

| Voice | Comedy Notes |
|-------|--------------|
| Storyteller | Dry observational. Comedy lives in framing, not jokes. |
| Nate | Dry. Sam Elliott model. Lets things land without commentary. |
| Flint | High. Sarcasm, deflection, mockery. Bob the Skull energy. Carry most of the load. |
| Josie | High. Manic earnest enthusiasm. ("Are you just going to LEAVE that there?") |
| Marcus | Low-to-mid. Adult-in-the-room dry. |
| Rex / Judge | Situational. Judge especially — her opinions ARE the joke. |

### Dresden Coexistence Principle

**Comedy and dramatic beats coexist on the same page.** Dresden does this constantly — wisecrack, terror, wisecrack, grief. Don't sacrifice a drama beat to avoid clashing with a Flint quip; the clash IS the texture.

---

## Editorial Workflow Notes

### One-at-a-Time Decisions

When a pass surfaces multiple decisions for David to make, **never dump a flat list** of "answer these 8 questions in bulk." Use AskUserQuestion popups (or the equivalent) **one at a time**. David needs each decision in isolation, with full context, before moving to the next.

### Chapter Status — Current Locks

- **Ch1–8** UNLOCKED 2026-04-17 for re-pass under current rules.
- Ch9–10 drafted, awaiting first editorial pass.
- Re-pass priorities: System-intent discipline, Flint design-intent throttle, material-comparison sweep.

### Editor's Hat Pass Order

When invoked for a full editorial pass:

1. **Pass 1** — Continuity (timeline, character knowledge, prop tracking).
2. **Pass 1.5** — Length discipline (every-line-must-earn).
3. **Pass 2** — Voice (Storyteller / Nate / Flint / pack-bond routing).
4. **Pass 3** — Theology-show-don't-tell sweep.
5. **Pass 4** — Audiobook punctuation pass (Brigid stutter fixes).

---

## Genre Best-Practice Audit (2026-05-17)

Four action items from a cross-subgenre best-practice audit (High Fantasy,
LitRPG, Urban Fantasy, Shifter/animal-bond). The audit confirmed the manuscript
is already built against genre convention deliberately; these are the genuine
open items.

### Soft-Magic Discipline — Conduit Power

Conduit power is uncapped (Codex #91). Sanderson's First Law: the more a power
can resolve plot conflict, the more rigorously the reader must understand its
rules. The standing risk is Books 4–7, when conduit power scales and an
alignment-fuelled miracle becomes a tempting climax solution.

**Rule of thumb:** *Conduit power changes the protagonist; engineering and
earned skill change the outcome.* The Briarknight climax models it — "the
Engineer doesn't kill the boss, the Engineer makes the boss killable"
(Codex #107). Climaxes resolve on hard, reader-legible, earned mechanics;
conduit power shows up as who Nate becomes, not as the win condition.

### Guard the Sequel Beat

Urban-fantasy craft (Butcher's scene/sequel engine) builds reader bond in the
**sequel** — the reaction unit: emotion → reason/review → decision. LitRPG
forward-momentum pressure can starve it, especially in combat-dense Tutorial
chapters. The existing **"earned breath"** clause (see LitRPG Pacing above)
licenses the sequel beat — enforce it. After a heavy room, the cohort gets
emotion and a decision before the next door, not just a loot drop and a corridor.

### RoyalRoad / Serial-Release Question (Open Decision)

Chapter 1 carries zero System content — a trad-publish / audiobook-first opening,
not a RoyalRoad-serial opening (serial LitRPG readers expect a progression hook
in Ch1). This is fine for the current audiobook-first plan. **If serialization
on RoyalRoad is ever on the table, Ch1 needs a companion plan** — it is a
liability on that platform specifically. Decide consciously; do not drift into
serialization without revisiting the opening.

### Pack Terminology + Animal Cognition

- **Retire "alpha"** as a label. The pack *model* is correct (Genesis
  Stewardship, Codex #43 — family/stewardship, not dominance), but "alpha" is
  dated science (the Schenkel captive-wolf study, since debunked). Prefer "Nate
  is Rex's person / they are pack." Internal-doc cleanup; never let "alpha"
  reach prose.
- **Set a cognition rule before P3.** Rex/Judge anthropomorphism currently lives
  entirely in the Storyteller's comic framing — the dogs themselves only ever do
  real working-dog behaviors. That is consistent and safe. When the pack-bond
  progression reaches **P3 (full mental speech)**, actual words enter the dogs'
  heads and the cognition-consistency question becomes real. Lock a rule for how
  Rex/Judge *think* (vs. how the narrator jokes about them) before drafting P3.

---

## Quick-Reference: The Hard Bans

A consolidated list of "never do this in prose" rules:

1. Never use **"Imago Dei"** directly.
2. Never use **"Repent," "Eden,"** or **"Lucifer"** by name in early prose.
3. Never take the **Lord's name in vain.**
4. Never label the **lens** ("his engineer brain noticed...").
5. Never label the **Tutorial pedagogy** ("curriculum," "syllabus").
6. Never have characters **"press bodies flat"** (dogs or otherwise).
7. Never use **mechanical-engineering vocabulary** (pumps, valves) for Nate's engineer perception.
8. Never use **MBSE / NOC / Grafana / SCIF / IATT** in prose (writing-guide only).
9. Never use **Star Wars / Jedi / Force** terminology.
10. Never **count atmosphere numbers** as audit-grade headcount.
11. Never **dump multi-decision lists** for David — ask one at a time.
12. Never **revert audiobook punctuation fixes** without asking.
13. Never **attribute design-intent to the System** in early Book 1 (through Ch8).
14. Never use **"sub-skill"** — use Ability.
15. Never **bold System terms** in group / verb / generic usage.
