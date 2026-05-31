# Forge Novel — Magic System Reference

*Writer-facing reference. Distilled from locked Codex entities.*
*Last regenerated: 2026-04-23 — includes cosmology architecture refinement (Creator / Labyrinth-pipeline / Spirit-direct / System-overlay), Channel Model, Substrate-Clean Principle, and Conduit Amplification Overlay.*
*Sources: Codex #91, #93, #94, #95, #97, #100, #177, #178, #179 + research/skill-system-design.md + REFERENCE.md Power Systems.*

> **Prose register reminder (Codex #94, 2026-04-15 + 2026-04-23 appends):** This doc uses writer-facing theological and architectural vocabulary — *Imago Dei, Eden, Lucifer, substrate, clean channel, skewed channel, amplification overlay, Labyrinth pipeline, Conduit Gift*. **None of that language goes into prose.** Use in-universe framing only in chapter drafts — "The Barrier," "The Adversary," "the Sealing," etc. The mechanics are unchanged; only the vocabulary used to render them on the page is restricted. See Codex #94 for the full protected-vocabulary list.

---

## Power Hierarchy (Codex #91 — LOCKED)

Three tiers. Plus a foundation layer baked into all of them.

**Imago Dei Foundation** (not a tier — underneath everything)
Humans were created with inherent superhuman potential. Post-Integration, that heritage activates in ALL humans. System claims credit. System is lying. Foundation is always there; the three tiers are just different access methods.

**Tier 1 — System Magic** (The Counterfeit)
Source: Lucifer's overlay, reverse-engineered from divine architecture. Mechanics: mana pools, cooldowns, skill ranks F–S, class affinities, patron bonds. **Capped at A-tier** in absolute terms — S-rank inside the System = A-tier on the real scale. Cost is hidden: every level-up, patron bond, and System rune is a binding hook.

**Tier 2 — Elder Magic** (The Fragment)
Source: Fae / Old Powers who glimpsed divine architecture millennia ago. Traditions: Elder Futhark, Ogham, Welsh elemental, Norse seidr. Stronger than System, weaker than Conduit. The photocopy problem — degraded copy of the original. Cost: relationships with Fae / Old Powers who have their own agendas.

**Tier 3 — Conduit Power** (The Original)
Source: God, channeled through faithful humans. Flows through, never stored. No ceiling — source has no ceiling. Mechanics: Spiritual Progression Track. Cost is real and ongoing (see #93).

**Hard rule:** God acts ONLY through the conduit. No unmediated divine intervention tier.

**Tier politics**

- System resents Elder (can't quantify or control it).
- Fae resent System (newcomer squatting on older architecture).
- System cannot read Conduit — this terrifies Admins.
- Fae recognize Conduit as closer to source (fascinated / jealous / threatened).

---

## The Barrier (Codex #94 — LOCKED)

The theological foundation for ALL superhuman ability in the series.

**Original state:** Pre-Fall humans had superhuman potential as instinct — strength, perception, healing, awareness beyond modern norms. After exile, a barrier was placed over this state.

**Leakage:** Historical cracks — sixth sense, mother lifting a car, soldiers past physical limits. These are glimpses of what was always underneath, not miracles.

**Lucifer's bypass (System path):** Artificially removes the barrier and slaps a GUI on it. Stats, skills, mana pools, level-ups — the System's branding on God's design. Lucifer did not create the enhancement. He unlocked what was already there and claimed credit. Every chime and notification says "the System gave you this." The System gave nothing. It opened a door that was already there and put its logo on the frame.

**Spirit's removal (Anomaly path):** For the faithfully indwelt, the Holy Spirit **actually** removes the barrier. Legitimately, completely. But without the System's training wheels. No GUI, no readout, no easy button. Raw superhuman potential comes online **glitchy at first** because nothing is managing the interface. The Anomaly learns to use it with non-verbal guidance — no instruction manual.

**The cost of freedom:** Anomalies start BEHIND the curve. Everyone else gets instant competence through the System's hand-holding. Anomalies get raw potential with no manual. The System's path is easier. That's the temptation. That's the cage disguised as a gift.

**Narrative application:** After Ch5's first fight, Marcus has clean stats, skill ranks, mana management — everything labeled. Nate has vague impressions, glitchy perception, and a body that can do more than it could yesterday with no interface explaining how. He looks behind the curve. The reader feels the cost of being an Anomaly.

---

## Cosmology Architecture (Codex #177, #178, #179 — LOCKED 2026-04-23)

Architecture refinement on top of the Power Hierarchy above. This is the spine under every downstream decision.

### Sources and delivery paths

- **Creator** — sole legitimate source of all power, skill, and gift
- **Deceiver** — counterfeit-generator. No legitimate source power of its own

```text
Creator
  ├── Labyrinth (pipeline)
  │     ├── Spatial bridge — cross-world transit for children
  │     └── Distribution channel — all skills, to all beings
  │
  └── Spirit (direct, bypasses the Labyrinth entirely)
        └── Conduit Gifts — to Conduits specifically

Deceiver
  └── System (counterfeit overlay on the Labyrinth pipeline)
        ├── Skewed routing — reroutes clean-channel skills' allegiance to the deceiver (same skill, same effect, misrouted glory)
        └── Inferior knockoffs — System-originated versions of Conduit Gifts; categorically weaker than the real thing
```

### Three protection guarantees

- **Conduit Gifts are protected.** Spirit-direct delivery cannot be skewed. System can make its own inferior versions; it cannot corrupt the real Gift in-instance
- **The Labyrinth is not the source.** The deceiver's System cannot become a source by capturing the pipeline. Creator retains ownership; the pipeline is His provision, corrupted in routing but not in origin
- **Substrate is always clean.** The deceiver cannot corrupt energy itself — mana pools, physical energy, life, breath are all Creator-sourced and stay clean no matter who holds them. Corruption applies only to how a being **uses** the substrate (skill-channel routing)

### Channel model — clean vs skewed

Every skill is Labyrinth-delivered and Creator-sourced. No skill is intrinsically System-native. What changes between characters is the *routing*, not the skill. A System-bound user has a **clean mana pool** and uses **skewed skills** — the energy is God's; the allegiance-pointer under each skill-use is the skew.

| Dimension | Clean channel | Skewed channel |
|-----------|---------------|----------------|
| Source | Creator | Creator |
| Delivery | Labyrinth | Labyrinth, then System-rerouted |
| Mechanical effect | Full | Full (same skill, same capability) |
| Allegiance returns to | Creator | Deceiver |
| Requires System binding | No | Yes (per Codex #100 stages) |

Depth-of-skew is a gradient per Codex #100 stages, not binary.

### Elder Magic note

Tier 2 Elder Magic (Fae / Old Powers) cosmology-level placement remains under-specified. Working assumption: Elder Magic traditions are Labyrinth-delivered skills transmitted through Fae mentorship; the "fragment" quality is incomplete access rather than incomplete source. Confirmation deferred pending worldbuilding pass.

---

## Skill System Architecture (Codex #177 — LOCKED 2026-04-23)

Full design doc: [research/skill-system-design.md](../research/skill-system-design.md).

**Three-tier hierarchy.** Domain → Skill → Ability.

- **Domain** — top-level grouping (ten of them; see below)
- **Skill** — the rank-bearing container (what the HUD shows a rank for: Sword Mastery, Cooking, Structural Analysis)
- **Ability** — the named usable move/power inside a Skill (Riposte, Ignite, Active Listening Pass). Active or passive. Genre-standard leaf-term (Kong, Zogarth, Shirtaloon convention). "Sub-skill" and "technique" retired as taxonomy terms; lowercase "technique" remains acceptable prose flavor

**Ten Domains.** Channel is orthogonal to domain — no domain is clean-only or skewed-only.

1. Martial — Weapons
2. Martial — Magic
3. Martial — Tactical
4. Perception
5. Stealth
6. Social
7. Physical
8. Gathering
9. Crafting
10. **Life Skills** — real-world everyday capacity (Home / Trade / Profession / Arts / Body / Mind / Social) — 2026-04-23 expansion

**Rank scale.** F → S for all Skills across all domains. S-rank = A-tier in absolute terms on the real scale (per System cap in Codex #91).

**Life Skills note.** Every Life Skill is equal-source to every Martial skill — all Creator-sourced via Labyrinth pipeline. The Mundane Baseline is not a separate "authentic" layer; it's another domain grouping.

**World-bench vs Book 1 spotlight.** World-wide availability: all domains, all skills. Book 1 surfaces ~30 named skills with enough specificity to notice. Remaining ~70 are worldbook material.

---

## System Magic — The Four Components (Codex #97 — LOCKED)

Light crunch. Readers see costs and cooldowns. No formulas.

### 1. Mana Pools + Cooldowns

- Every integrated human has a **mana pool** — quantified energy reserve, displayed on combat HUD during action and character sheet during rest.
- Skills cost mana. Regenerates passively but slowly. Rest speeds recovery.
- Cooldowns are real — fire a skill, it's unavailable briefly. Combat HUD shows the timer.
- Mana potions are a System economy hook (quest rewards, loot drops).
- **Reader feel:** "Do I use my big skill now or save it?" — genre-familiar. Every gamer nods.
- **The lie underneath:** mana is the Imago Dei potential being metered and controlled. Lucifer did not create the energy. He put a meter on it.

### 2. Skill Ranks F → S (Use-Based)

Skills improve through use, not XP allocation. Swing the sword, sword skill gets better.

| Rank | Name | Feel |
|------|------|------|
| F | Novice | Barely functional. System hand-holding. |
| E | Apprentice | Reliable basics. Most Tutorial graduates land here. |
| D | Journeyman | Competent. Skill feels natural. |
| C | Adept | Efficient — less mana, shorter cooldowns, stronger effects. |
| B | Expert | Elite. Most never reach this. |
| A | Master | Regional reputation. Pinnacle of what the System can offer. |
| S | Grandmaster | Exists, but S = A-tier in absolute terms. The System's ceiling. |

**The Skinner box:** each rank-up delivers a real improvement and a dopamine hit — achievement popup, golden sparkle, satisfying chime. Designed to be addictive. The gamer in Nate recognizes it.

### 3. Class Affinities + Starter Skills

**Hybrid assignment.** System sorts by pre-Integration aptitude AND System need. Feels like it matches who you are — actually, the System is filling roles in its economy.

**Class families:**

- **Combat** — Warriors, Shield Guardians, Berserkers, Duelists. Physical skills, weapon techniques. Smaller mana pools.
- **Caster** — Mages (elemental affinities), Enchanters, Illusionists. Larger mana pools, higher costs.
- **Healer** — Healers, Battle Medics, Wardens. Restoration and protection. Mana-intensive.
- **Support / Leadership** — Vanguards (Marcus #99), Scouts, Crafters, Engineers (Nate #98). Buff / debuff / information / utility.

Many subclasses and specializations unlock as players progress. Starter classes are basic; branching emerges over time.

**Universal starter skill:** everyone receives the same generic energy bolt / strike. As they progress, the System offers branching options — fire affinity, ice affinity, weapon specializations. **The player is given the illusion of choice.** The System controls which options appear. You feel like you're building YOUR character. You're selecting from a menu the System curated.

### 4. Patron Bonds (The Shortcut)

Fallen spiritual beings (Patrons, Codex #7) offer power boosts through the System framework. Present as benefactors, mentors, gods.

- At threshold moments, the character sheet shows a **Patron Offer**.
- Accepting grants immediate power: bonus skills outside class affinity, stat boosts, accelerated progression, rare abilities.
- **Hidden cost:** each bond deepens System integration. Patron gets hooks into decision-making. AI nudges harder. Class evolves in directions the user didn't choose.
- Early bonds = loose (a perk). Late bonds = chains.

**Through Nate's HUD:** a Patron-bonded person has **thicker strings**. More data lines running upstream. The Patron's signature woven through their stat sheet like malware in a system process. The warrior feels powerful. Nate sees a puppet with better production values.

**Tutorial note:** nobody has Patron bonds yet in the Tutorial — too early. But the *architecture* should be visible. Class synergies. Tank-and-healer pairings. DPS windows. The System isn't just sorting people — it's building party compositions.

---

## Conduit Consequences (Codex #93 — LOCKED) + Amplification Overlay Refinement (Codex #178 — LOCKED 2026-04-23)

### Narrative framing (still canon)

Three-state consequence model for the true power tier. The fade/shutoff metaphor remains the NARRATIVE shape — Nate does feel the overflow stop, and restoration IS earned over time.

**State 1 — Doubt / Questioning → Plateau.** Power doesn't grow, but existing power still works. Doubt is human, not sin. **Doubt does NOT cause power loss.**

**State 2 — Minor Drift → Gradual Fade.** Triggered by pride, selfishness, losing focus on purpose. Power dims like a signal losing strength. Still there but weaker, less reliable, harder to channel. The conduit narrows. User feels it going and knows why — not punishment, natural consequence. Restoration: realignment, humility, returning to purpose.

**State 3 — Major Violation → Hard Shutoff.** Triggered by deliberate cruelty, using conduit power for evil, betrayal of the covenant relationship. Pipeline dead. Instantly. No warning. Silence where power used to be. Restoration requires genuine repentance.

**Contrast with System:** A System Warrior can murder civilians and still swing their sword at full power. **Reliable evil vs. conditional good.** The System is safer. The conduit is truer.

### Mechanical refinement (2026-04-23 — Codex #178)

The underlying mechanic is an **amplification overlay** riding on top of Nate's owned skills. Skills remain intact across all states; what toggles is the amplification. See full model in Codex #178.

| State | Alignment | Overlay | Base skills | Conduit Gifts |
|-------|-----------|---------|-------------|---------------|
| **Aligned** | Per-action AND state-of-being both point to Creator | **On** — overflow active, caps exceeded, growth possible | All function; amplified output | Fire |
| **Doubt / Plateau** | Uncertain but not opposing | Off — no overflow | Base capacity; caps normal | Function at current rank; no growth |
| **Opposition** | Acting against Spirit / Creator | Off — **stasis, not decay** | Base intact; nothing atrophies | **Silent while opposed; return instantly on realignment** |

**Key refinements:**

- **Nothing is lost, only overflow toggles.** Skills are owned, not rented. The Conduit property is the overlay, not the skills
- **Alignment is layered** — per-action AND state-of-being. Per-action opposition drops overflow on THIS act; state-of-being drops it across the board
- **Opposition is stasis, not decay.** Return is immediate on realignment. No grind-back
- **Two flavors:** Amplification-type (overlay on existing skill — Pyromancy past mana cap, SA past rank ceiling) vs Origination-type (no base capacity — Gift of Tongues has no baseline Mandarin)

**Narrative rule:** Show the overflow stopping, don't explain the mechanic. Nate tries to use conduit power; it comes weaker than expected. He knows why. He adjusts. No theological narration. Shutoff is a crisis moment — sparingly.

---

## Conduit Gifts — Biblical Gifts Pool (Codex #178 — LOCKED 2026-04-23)

Conduit Gifts are **skills** in the ownable / rankable sense, with unique properties: Spirit-direct source (bypass Labyrinth), protected from skewing (System has inferior knockoffs only), alignment-gated, not-lost-in-opposition (go silent; return on realignment).

### Nate's Gift roster (tentative, Book 1+)

| Gift | Pattern | Book 1 presence |
|------|---------|-----------------|
| **Gift of Tongues** (xenolalia) | Origination | Planned — non-English Labyrinth node |
| **Word of Knowledge** | Origination | Likely — "you couldn't have known" beats |
| **Discernment of Spirits** | Origination | **Arc-critical** — reads System's nature |
| **Bezalel-pattern Craftsmanship** (over SA) | Amplification | Yes — Engineer-Conduit ceiling |
| **Amplified Output** (over any skill) | Amplification | Yes — the overflow mechanic |
| Healing / Faith / Prophecy / Miracles | Origination | Deferred to later series |

### The Bezalel pattern — Nate's arc ceiling

Bezalel (Exodus 31:2–5) — Scripture's first named Spirit-filled person, filled for **craftsmanship** (wisdom, understanding, knowledge in all workmanship). Textbook Conduit amplification of a trained skill, directly parallels Nate's SA trajectory. Book-ceiling, not Book-1 ceiling.

### Biblical Gifts candidate pool (worldbook reference)

- **1 Cor 12** (Spiritual Gifts): Word of Wisdom · Word of Knowledge · Faith · Healings · Miracles · Prophecy · Discernment of Spirits · Tongues · Interpretation
- **Rom 12** (Ministry Gifts): Service · Teaching · Exhortation · Giving · Leadership · Mercy
- **Eph 4** (Offices): Apostle · Prophet · Evangelist · Pastor · Teacher
- **Ex 31, 35** (Bezalel): Spirit-Filled Craftsmanship · Metalwork · Stonecutting · Woodworking · Weaving · Teaching of Craft

### System counterfeits of Conduit Gifts

Exist and are categorically inferior. Writer-facing notes (not specified per-Gift): System-Tongues (narrower, glitchier), System-Discernment (partial, sometimes backwards), System-Healing (lower tier, residual cost), System-Prophecy (sometimes propaganda). Useful villain/faction mechanic — performance gap tells the reader something's off.

### Prose register

Never name "Gift of Tongues" or any biblical Gift label in prose. Show the effect. Nate realizes he understood a language he shouldn't. An NPC with an apparent Gift reads off. The reader feels it; no one names it.

---

## System Binding Progression — Four Stages (Codex #100 — LOCKED)

Mirror of the conduit model. **No moral cost. Severe binding cost.** Each stage is voluntary, comfortable, reasonable in the moment. The cage is built one good decision at a time.

### Stage 1 — Integration (The Gift)

Everyone gets enhanced state, a class, starter skills, dual interface. Cost is invisible — System AI installs, data flows upstream, feels like a useful smartphone. Light strings visible to Nate's HUD. Leash so loose it looks like a ribbon.
- **Reversibility:** easy. Short, uncomfortable walk. Easiest converts.
- **Why some stay:** comfort. The System works. Why question a gift?

### Stage 2 — Leveling (The Hooks)

Each level adds System infrastructure — scaffolding around the house. Cost: dependency. Enhanced abilities route through System architecture instead of raw potential. A Level 20 Warrior has forgotten how to swing with superhuman precision without training wheels. Thicker connections in Nate's HUD.
- **Reversibility:** possible but painful. Quitting a drug that managed your pain. The Valley is real — worse before better.
- **Why some stay:** identity. "I am a Level 30 Warrior. That's who I am." Leaving means becoming nobody.

### Stage 3 — Patron Bonds (The Chains)

Patron's signature woven into the System's architecture. Cost: autonomy. Not mind control — nudges. AI suggests things serving the Patron's interests. Emotions shift. Choices feel less like yours. You'd swear you're still deciding freely. The Patron would agree. That's the point.
- **Reversibility:** difficult. Breaking the bond tears out something woven into decision-making. Patron resists. AI fights. Emotions betray. Valley can last BOOKS.
- **Why some stay:** the Patron has reshaped their **wants**. They have been slowly rewritten into someone who does not want what's on the other side. Still have free will. Use it to stay. That's the tragedy.

### Stage 4 — Prestige / Ascension (The Replacement)

Prestige classes and ascension paths replace humanity with System-loyal architecture. Not scaffolding — load-bearing walls. Original personality, independent judgment, capacity for love and sacrifice get optimized away. Replaced with System-efficient versions. Still feel like yourself. You are not. Through Discernment, Nate sees a hollowed-out vessel wearing a stat sheet like a skin suit.
- **Reversibility — theological:** ALWAYS possible. Grace does not expire.
- **Reversibility — narrative:** the person who would need to walk through the door barely exists anymore. Would have to destroy everything they've become to start over as essentially nothing. The System has spent years making them into someone who wouldn't make that choice. Not by force — by incremental, voluntary, comfortable transformation.
- **Codex #101 — The Stage 4 Convert:** one character, Books 5–6, proves the door is always open. Devastating cost, emerges as nearly nothing. Prevents the progression from reading as theological determinism.

### The Boiling Frog Principle

No single step feels like a bad decision. Integration feels like a gift. Leveling feels like growth. Patron bonds feel like opportunity. Prestige feels like achievement. What makes the System terrifying isn't that it forces you — it's that it never has to.

**Narrative rule:** The story NEVER says redemption is impossible. No character, no narrator, no authorial voice ever declares someone beyond saving. The story SHOWS characters so thoroughly System-constructed that the reader understands — without being told — this person will not choose the door. Faithful truth: the door is open. Narrative truth: they will not walk through. Both are real. Both hurt.

---

## System Dual Interface (Codex #95 — LOCKED)

System-integrated users get **two separate interfaces**.

### Interface 1 — Character Sheet (Rest / Menu)

Translucent blue popup screen — the classic LitRPG blue screen.
- Full stat display, skill list with ranks, inventory grid, quest log, achievement history, patron offers, class tree.
- Clean, beautiful, polished. Premium-game-menu feel.
- **BLOCKS VISION when open.** Like opening your inventory in Skyrim.
- Rest-state tool only. NOT up during combat or active movement. Dismissed by thought.

### Interface 2 — Combat HUD

Lighter overlay for active use.
- Health bar, mana bar, active skill cooldowns, threat indicators, minimap, party status.
- Less info than the character sheet but always available. Does not block vision.
- Starts out BETTER than Nate's HUD — cleaner, more informative, properly calibrated.

### The Divergence

| | System user | Nate (Anomaly) |
|---|---|---|
| Character sheet | Yes, polished | **None** |
| Combat HUD — start | Better (clean, labeled) | Worse (glitchy, monochrome, barely functional) |
| Combat HUD — trajectory | Never evolves beyond initial design | **Grows.** By mid-Book 1 surpasses the System HUD. By Book 2 in a different category. |
| Stats readout | Numerical ("WIS: 20") | Experiential (feels awareness sharpen; Flint reports the data spike) |
| Mana bar | Displayed | Felt — conduit flowing or not |
| Disorientation | None | High at first (the cost) |
| Ceiling | Locked at System cap | No ceiling (the reward) |

**Prose rule:** When describing System users in combat, reference their **combat HUD** — not the blue screen. The blue screen / character sheet appears only during rest scenes, level-up moments, or build review. A master craftsman does not check a manual before cutting wood. He knows the grain by touch.

**HUD phase system (Codex #11, #75):** Nate's HUD starts as two monochrome blue arcs. Phase 2 features do NOT appear casually on Phase 1 hardware — if they do, Flint flags the anomaly.

---

## Nate's Position in the System (Quick Reference)

- **Class:** Engineer (Codex #98) — covers IT systems, farmhand repair, MacGyver building. Name replaces the old "Systems Engineer."
- **Skills:** Structural Analysis (glitched — sees actual architecture), Field Repair (reads materials through touch).
- **Interface:** No character sheet. Combat HUD is blue wireframe, iris-compass form (Codex #75). Phase 1 start, evolves over Book 1.
- **Mana:** None. Conduit power is not stored.
- **Tutorial loadout (Codex #104):** Improvised crossbow (ranged, stripped parts) + reinforced hammer (melee + crafting tool) + Thornling thorn bolts from Josie. No post driver — doesn't come to Tutorial.
- **Progression:** Exits Tutorial at Level 4 Engineer (Codex #96).

---

## The Fundamental Choice

- System has **no moral cost** but severe **binding cost** — hidden, progressive, increasingly irreversible in practice.
- Conduit has **real moral cost** (visible, felt immediately) but **no binding cost** — no hooks, no strings.
- System power is reliable regardless of character. Conduit power is conditional on faithfulness.

**The System is safer. The conduit is truer.** That is the core tension of the series.

---

## Cross-References

| Codex ID | Name | Purpose |
|----------|------|---------|
| #91 | Power Hierarchy | Three tiers + Imago Dei foundation + 2026-04-23 architecture refinement |
| #93 | Conduit Consequences | Fade/shutoff narrative framing + 2026-04-23 pointer to #178 |
| #94 | The Barrier | Imago Dei theology + prose register rules (2026-04-23 expanded vocabulary) |
| #95 | System Dual Interface | Character sheet vs. combat HUD |
| #97 | System Magic Rules | Four components + 2026-04-23 substrate-clean refinement |
| #98 | Engineer Class | Nate's class |
| #99 | Vanguard Class | Marcus's class |
| #100 | System Binding Progression | Four-stage cage + 2026-04-23 channel-depth anchor |
| #101 | Stage 4 Convert | Redemption proof (Books 5–6) |
| #103 | Appraiser Class | Josie's class |
| #104 | Nate's Tutorial Loadout | Improvised crossbow + hammer |
| **#177** | **Skill System Architecture** | **Three-tier hierarchy + ten domains (2026-04-23)** |
| **#178** | **Conduit Amplification Overlay** | **Three-state model + Gift roster (2026-04-23)** |
| **#179** | **Substrate-Clean Principle** | **Channel routes on use, not energy (2026-04-23)** |
| #11, #75 | HUD Phase System / Visual Design | Nate's HUD evolution |
| #7 | Patrons | Fallen beings offering bonds |

**Design doc:** [research/skill-system-design.md](../research/skill-system-design.md) — consolidated skill-system design (cosmology + channel model + Conduit overlay + ten domains + Life Skills catalog + Biblical Gifts pool).

See `prompts/forge-novel-session-start.md` for the session operating rules that reference this file.
See `prompts/archive/magic_system-presession13-brainstorm.md` for the pre-Session-013 design notes this file supersedes.
