# Forge Novel — Skill-Mining Harvest: Fantasy-Writing Craft

> **Working build-resource (living doc).** Mines `mcpmarket.com/tools/skills`
> for reusable craft + engineering patterns to (a) sharpen forge-novel's own
> skills — `/forge-write`, `/editors-hat`, `tools/prose_lint.py` — and (b) seed
> a genre-agnostic **fantasy-fiction skill kit** for future projects.
>
> **IP posture — IDEAS & PATTERNS ONLY.** No verbatim text is lifted from any
> source skill. Every entry below is *my description of a mechanism*, to be
> **reimplemented in our own voice and rules**. Sources are credited as
> inspiration only. Most source repos are MIT, but we copy nothing regardless.

---

## Status

| Phase | State |
|---|---|
| Directory sweep (17 queries, 664 hits) | ✅ done |
| Triage (240 writing-relevant kept, 424 noise dropped) | ✅ done |
| Deep read (mcpmarket blocked → pivoted to GitHub source repos) | ✅ done |
| Deepening pass (Wave 2: 5 more GitHub systems + collections) | ✅ done |
| 2nd mcpmarket sweep (12 fresh queries, 206 new cards, no blocks) | ✅ done → **saturated** |
| Pattern library (**30 patterns**, 2 waves) | ✅ v2 |
| Action queue (9 grafts, tiered) | ✅ — awaiting David's pick |
| Idea ledger (14 items) | ✅ seed |

*Living doc. v2 complete + harvest saturated (see Coverage note). Next leverage
is building the Tier-1 grafts, not mining more.*

---

## How the mine was run

1. **Targeted sweeps, not enumeration.** The directory holds 600+ aggregated
   skills; I ran 17 fantasy-writing + engineering-pattern search queries and
   deduped by slug. 664 unique cards → 240 writing-relevant after keyword
   scoring → ~34 distinct *mechanisms* selected for deep `SKILL.md` reads.
2. **Dedup is essential.** The directory is full of mirrors. Example: a single
   "Fantasy World Building" skill surfaced as **7 cards** (two GitHub accounts
   mirroring one `ordinary-claude-skills` collection). The "Crucible" system
   shows up as **6 cards** (one repo, two forks). Card count ≠ skill count.
3. **Content is real, blurbs are not.** Marketplace descriptions are
   AI-generated summaries. The actual `SKILL.md` (verified by activating the
   on-page tab) is what's mined here.

---

## The landscape — what's actually out there

Across the writing-relevant results, the field clusters into six craft families
plus a thin band of reusable engineering patterns. **Key finding repeated from
the first eval: nothing is LitRPG-specific, and nothing addresses
audiobook-first / full-cast narration** — forge-novel's two defining
constraints are unserved by the entire market. The opportunity is ours.

| Family | Representative skills | What they offer us |
|---|---|---|
| **Drafting / prose** | Crucible Writer, Snowflake Chapter Writer, prose-writing, fiction-writer, creative-writing-craft | Scene-by-scene protocols, style-matching, self-check |
| **Structure / outline** | Crucible Planner+Outliner, character-arc-architect, story-bible-architect, storytelling-coach | Beat frameworks, convergence-point discipline, arc tracking |
| **Worldbuilding** | Fantasy World Building (×7 dup), character-world-architect | Magic/lore scaffolds (we're already past these) |
| **Voice / style** | analyze-prose-pinker-style, copy-editor-style-transformer, literary-style-revision, tailord-authentic-voice | Style fingerprinting, register transforms |
| **Editing / continuity QA** | narrative-continuity-checker/-tracking, fiction-character-quality-checker, story-critique, chicago-bureau-editorial-desk | Continuity diffing, multi-axis critique, editorial passes |
| **RPG / LitRPG / GM** | rpg-progression-design, d-d-character-progression, gm-craft, galgame-visual-novel | Progression-as-narrative, fail-forward, NPC motivation |
| **Eng. patterns** | creative-writing-skill-router, writer-memory, death-sourdough-continuity-manager | Skill routing, persistent memory, state machines |

---

## The style-source lens (the 17-book bank)

Every harvested idea is filtered through David's reference shelf
(`reference_litrpg_style_sources.md`). The bank splits in two, and generic
market skills serve the two halves very differently:

- **Voice / soul ancestors** — *Dresden Files, Jane Yellowrock, Iron Druid.*
  Dry wit under pressure, warm-observer prose, humor threaded through danger,
  the bonded-animal voice (Oberon → Rex). **Generic skills are weak here** —
  none capture *this* register. Voice stays our hand-built moat
  (`voice/exemplars.md`, the cast-routing rules). Harvested ideas help us
  *protect and measure* voice, not generate it.
- **Mechanics / pacing ancestors** — *Dresden's short-chapter momentum,
  Primal Hunter's analytical breakdowns, DCC's load-bearing comedy, Cradle's
  zero-interface display.* **Generic skills CAN help here** — structure,
  pacing scaffolds, progression-as-narrative, continuity tracking are
  genre-portable. This is where the mine pays off.

**Filter rule for every entry:** *Does this mechanism help us hit the
Dresden/Yellowrock voice, or the LitRPG pacing/structure? If neither, it's a
generic worldbuilding scaffold we've already surpassed — log and skip.*

---

## Pattern library — reusable mechanisms

Each pattern: **what it is → where it's proven → why it matters for us → how
WE'd build it (original) → target.** (Verbatim text never copied.) ★ = priority
graft. 21 patterns; deepen each as we actually build it.

### P1 · Three-skill pipeline: Plan → Outline → Draft
- **Proven in:** The Crucible Writing System (separate Planner, Outliner,
  Writer skills sharing project state).
- **Why it matters:** It's a near-exact mirror of our own split (Forge MCP
  outline/codex → `/forge-write` → `/editors-hat`). Independent validation
  that the architecture is right, and a reminder to keep the seams clean — each
  stage consumes the prior stage's artifact and nothing else.
- **How we'd build it:** We already have it. Action: make the hand-off
  artifacts explicit (outline beat → draft → editorial diff) so each skill has
  one well-defined input contract.
- **Target:** architecture sanity-check (no new build).

### P2 · "The Outline is Law" — anti-hallucination verification
- **Proven in:** Crucible Writer ("Never invent plot points, characters, or
  events not in the outline. If something seems missing, ASK — don't
  improvise.").
- **Why it matters:** This is *exactly* forge-novel's "if context is missing,
  stop and flag it — never invent structure" rule (CLAUDE.md operating
  contract) and the epistemic-state discipline. Worth hardening into an
  explicit pre-draft verification step.
- **How we'd build it:** A `/forge-write` pre-flight that diff-checks the beat
  against REFERENCE.md + epistemic-states.json and **halts with a question**
  (AskUserQuestion) rather than inventing. Reimplement in our voice.
- **Target:** `/forge-write`.

### P3 · Context-window discipline — load-only-current-scene, save constantly
- **Proven in:** Crucible Writer ("Context Window is Limited. Load only what's
  needed for the current scene. Save constantly. Progress must survive session
  breaks.").
- **Why it matters:** Long-form drafting drifts when the whole book is held in
  context. Our Forge MCP already externalizes state; this pattern argues for a
  disciplined *minimal* context load per beat + checkpoint-after-every-scene.
- **How we'd build it:** Formalize forge-write's context-loading protocol to
  pull only the current beat's Codex slice + epistemic state + relevant voice
  exemplar, and to commit/checkpoint the draft after each scene.
- **Target:** `/forge-write` loading protocol; reusable kit.

### P4 · Persistent Story Bible + Style Profile (state files)
- **Proven in:** Crucible (`story-bible.json`, `style-profile.json` per
  project); writer-memory (persistent memory pattern).
- **Why it matters:** Continuity across a 7-book series needs externalized,
  queryable state. We have the Codex (Forge MCP) and epistemic JSON; the gap is
  a **style fingerprint** artifact distilled from `voice/exemplars.md`.
- **How we'd build it:** A `style-profile` derived from our exemplars (per-voice
  rhythm, diction bans, register markers) that the linter and the writer both
  read. Original schema, our voices.
- **Target:** reusable kit + `prose_lint.py` / `/forge-write`.

### P5 · Bi-chapter multi-agent review panel (voice / continuity / outline / timeline / prose)
- **Proven in:** Crucible Writer (five specialized review agents run every two
  chapters).
- **Why it matters:** This is the single best graft target. It's a clean
  formalization of our editorial passes and a **natural Workflow fan-out** —
  one agent per dimension, adversarial verify, synthesize. Maps onto
  `/editors-hat`'s existing pass structure.
- **How we'd build it:** An `/editors-hat` mode (or a Workflow) that fans out
  per-dimension reviewers tuned to OUR rules — voice (cast routing, Hiberno
  register), continuity (Codex + epistemic), outline-fidelity, timeline,
  prose (prose_lint + craft). Each returns structured findings; synthesize.
- **Target:** `/editors-hat`; reusable kit.

### P6 · Multi-axis chapter self-check (scored dimensions)
- **Proven in:** Snowflake Chapter Writer (5 axes: conflict intensity,
  emotional density, reader anticipation, pacing control, hook design — each
  scored independently for diagnostic feedback).
- **Why it matters:** Extends `prose_lint.py` from *AI-tell detection* (what it
  does now, deterministically) into *craft scoring* (an LLM-judged pass).
  Complements, not replaces — keep prose_lint zero-token; add a scored pass as
  a separate optional gate.
- **How we'd build it:** Our own axis set tuned to forge-novel: **momentum**
  (LitRPG forward-pull), **comedy-dial calibration**, **voice fidelity**,
  **stakes/hook**, **show-don't-tell on faith**. Scored 1-5 with reasons.
- **Target:** new scored-review step in `/editors-hat`; reusable kit.

### P7 · Style-capture / "match the sample" voice engine
- **Proven in:** Crucible (style-capture engine), tailord-authentic-voice,
  copy-editor-style-transformer, analyze-prose-pinker-style.
- **Why it matters:** Generic skills *generate* generic voice — but the
  *capture-and-hold* discipline ("learn the author's voice early, match it
  relentlessly, when in doubt match the sample") is exactly how we should be
  driving from `voice/exemplars.md`.
- **How we'd build it:** Make exemplar-matching an explicit forge-write step:
  before drafting voice X, load that voice's exemplar and hold it as the
  target. (We do this informally; formalize it.)
- **Target:** `/forge-write`.

### P8 · Promise/payoff ledger ("Mercy Engine")
- **Proven in:** Crucible Planner (tracks compassionate acts that must pay off
  at climax).
- **Why it matters:** A setup→payoff tracker generalizes our
  `revelation-schedule.json`. Every planted promise (a foreshadow, a Chekhov's
  gun, a mercy) gets a payoff slot; the editor flags unpaid promises.
- **How we'd build it:** Extend revelation tracking into a general
  promises/payoffs table; an `/editors-hat` check greps for planted-but-unpaid
  threads across chapters.
- **Target:** `/editors-hat`; epistemic/revelation JSON.

### P9 · Genre-conventions-as-reference skill
- **Proven in:** romance-novel-writing-conventions (codifies a genre's beats,
  tropes, and reader expectations as a checkable reference).
- **Why it matters:** This is the template for a **distilled LitRPG-conventions
  reference** mined from the 17-book bank — the reader-expectation contract our
  audience brings (system panels, progression payoff, tutorial logic, stat
  reveals) that the writer checks against.
- **How we'd build it:** A `litrpg-conventions.md` reference (ours, from the
  booklist) the writer and editor consult — distinct from REFERENCE.md (canon)
  and WRITING_RULES.md (craft). Genre-contract layer.
- **Target:** new reference doc; reusable kit (swap the conventions file per
  genre).

### P10 · AskUserQuestion-driven interactive elicitation
- **Proven in:** Crucible (mandates the AskUserQuestion tool for *all* author
  questions — max 4 options, reference story elements by name, never plain-text
  A/B/C).
- **Why it matters:** Direct validation of David's **one-decision-at-a-time**
  preference and a concrete UX rule we should bake into both skills: structured
  popups referencing named entities, not prose menus.
- **How we'd build it:** Codify in `/forge-write` and `/editors-hat`: any
  author-facing choice uses AskUserQuestion with options naming the actual
  Codex entities / characters in play.
- **Target:** both skills (UX standard).

### P11 · Orchestrator / router skill ("muse")
- **Proven in:** `haowjy/creative-writing-skills` (a top-level "muse" skill
  routes work into three phases — Explore & Plan, Draft & Revise, Maintain —
  dispatching to the right sub-skill).
- **Why it matters:** A single front-door that reads intent and routes to
  brainstorm / outline / draft / revise / chronicle. We have two skills today;
  a thin router could unify them and pick the phase automatically.
- **How we'd build it:** A `/forge` dispatcher that detects "am I planning,
  drafting, or editing?" and invokes the right skill with the right context
  load. Optional convenience layer; low priority.
- **Target:** reusable kit (skill architecture).

### P12 · Reader-experience critic rubric (4 channels)
- **Proven in:** `creative-writing-skills` Critic — scores drafts on four
  *reader-experience* channels: **transportation** (immersion), **aesthetic
  quality**, **social simulation** (character believability), **flow**
  (pacing/rhythm).
- **Why it matters:** A second, complementary rubric to Snowflake's craft axes
  (P6). This one measures the *reader's felt experience* — closer to what
  audiobook listeners actually feel. Pairs naturally with our audio-first lens.
- **How we'd build it:** Add these as named lenses in the review panel,
  reworded for our audiobook frame (e.g., transportation = "does the listener
  stay in the scene"; flow = "does Brigid stutter / where does momentum sag").
- **Target:** `/editors-hat` review panel (feeds P5).

### P13 · Chronicler — auto-extract canon from approved chapters ★
- **Proven in:** `creative-writing-skills` Chronicler (extracts facts from
  *completed* chapters into a `kb/` of canon, characters, world, timeline).
- **Why it matters:** **Top-tier graft.** After David approves a chapter, an
  agent mines it for new canon (entities, relationships, timeline events) and
  proposes **Forge MCP Codex** updates — instead of manual Codex upkeep. Keeps
  the 153-entity Codex current as the book grows, and catches drift early.
- **How we'd build it:** A post-approval `/editors-hat` step (or Workflow) that
  diffs the approved chapter against the Codex and emits *proposed* codex
  create/update calls for David to confirm (never auto-writes canon).
- **Target:** new post-approval step; Forge MCP integration.

### P14 · Style-creator — voice fingerprint from samples ★
- **Proven in:** `creative-writing-skills` Style-creator (analyzes prose
  samples → reusable voice reference files); Crucible style-capture.
- **Why it matters:** Turns `voice/exemplars.md` into a structured, queryable
  **fingerprint per voice** (Storyteller, Nate, Flint, Rex, Judge) — diction
  markers, rhythm, register, bans — that both `prose_lint` and `/forge-write`
  read as the target to match.
- **How we'd build it:** Generate a `voice/fingerprints/<voice>.json` from the
  exemplar bank; forge-write loads the active voice's fingerprint before
  drafting; prose_lint scores deviation. Our schema, our voices.
- **Target:** reusable kit + `prose_lint.py` + `/forge-write`.

### P15 · Character-sim — interrogate a character in-voice before drafting
- **Proven in:** `creative-writing-skills` Character-sim (in-character dialogue
  for relationship testing and discovery).
- **Why it matters:** Before drafting a hard Nate/Flint/Josie beat, "talk to"
  the character in voice to discover how they'd actually react — a discovery
  tool, not prose. Useful for nailing voice and motivation.
- **How we'd build it:** A forge-write sub-mode that role-plays a Codex
  character (loaded sheet + voice fingerprint) for a few turns to pressure-test
  a beat. Output informs the draft; never ships as prose.
- **Target:** `/forge-write` discovery mode.

### P16 · Three-layer context hierarchy (Standards → Novel → Book) ★
- **Proven in:** `forsonny/book-os` (Standards = global reusable craft; Novel =
  project vision/voice; Manuscripts = per-book outline/characters/scene tasks —
  *progressive context accumulation*).
- **Why it matters:** **This is the organizing principle for David's "both
  forge-novel + reusable kit" goal.** Standards = the genre-agnostic kit;
  Novel = forge-novel canon (REFERENCE/WRITING_RULES/Codex); Book = per-volume
  state. Each layer narrows the one above. Clean separation, portable kit.
- **How we'd build it:** Frame the reusable kit as "Standards," keep
  forge-novel's canon as the "Novel" layer, and per-book state (epistemic,
  revelation, drafts) as the "Book" layer. Future projects swap the Novel layer.
- **Target:** the whole effort's architecture.

### P17 · Gated editorial pipeline with bounded revision loops ★
- **Proven in:** `ThomasHoussin/Claude-Book` (Planner → Writer →
  Perplexity-Improver → Style-Linter → Character-Reviewer → Continuity-Reviewer
  → State-Updater; each is a **gate** that must pass, with up to 3 revision
  loops before escalating).
- **Why it matters:** The most concrete multi-agent editorial pipeline in the
  field — richer than Crucible's review (P5). The **gating + bounded retry** is
  the key idea: a failed dimension triggers targeted revision, not a full
  redo, and caps loops so it can't spin.
- **How we'd build it:** Structure `/editors-hat` as ordered gates mapped to
  OUR passes (voice/cast-routing → continuity/Codex → outline-fidelity →
  timeline → prose_lint → audio-flow). Bounded auto-revision per gate, then
  hand to David. Natural Workflow.
- **Target:** `/editors-hat` (combine with P5/P12).

### P18 · Perplexity gate (local model on Nova/Ollama) ★
- **Proven in:** `Claude-Book` Perplexity-Improver (local GPU model flags
  low-perplexity = too-predictable/formulaic sentences, rewrites for variation).
- **Why it matters:** Directly matches the **"perplexity gate" already named as
  a forge-write future phase**, and David has **Ollama on Nova** to run it
  zero-cost. Complements `prose_lint` (which catches *known* AI tells
  deterministically) by catching *statistically* generic sentences the
  blocklist misses. Burstiness is already a prose_lint signal — perplexity is
  its probabilistic cousin.
- **How we'd build it:** A `prose_lint` companion that scores sentence
  perplexity via a local Ollama model on Nova, flags the flattest sentences for
  human attention. **Report-only** (never auto-rewrite — our em-dash/audio
  rule). Optional, opt-in.
- **Target:** `tools/` (prose_lint companion); Nova/Ollama.
- **BUILT 2026-05-30** as `tools/prose_predictability.py` (validated, ruff-clean).
  Verified findings: Ollama 0.17.x exposes logprobs for **generated tokens only**
  (no prompt/echo logprobs); `raw: true` is required or instruct models *comment
  on* the prose instead of continuing it; `top_logprobs` caps at **20**. The cheap
  one-call-per-sentence "agreement scan" was built and tested first and **did not
  discriminate** flat from distinctive prose — replaced by **teacher-forced
  perplexity** (one call/word). Discrimination confirmed: planted clichés ppl
  10-31 vs forge-novel prose 800-2300 (~25-230×). Cost makes it a **spot-checker**
  (bounded `--max-sentences`), not a bulk scanner. See `tools/README.md`.

### P19 · Bible (read-only) / State (versioned) / Timeline (append-only)
- **Proven in:** `Claude-Book` file architecture (immutable style anchors vs.
  per-chapter versioned state vs. append-only event log).
- **Why it matters:** A discipline for series continuity: canon/style is
  read-only during drafting; narrative state is versioned per chapter; the
  timeline is append-only and immutable. We have pieces (git versions drafts,
  Codex holds canon); the **append-only timeline/history** is the gap.
- **How we'd build it:** An append-only `timeline.md` (or Forge MCP timeline)
  of in-world events per chapter, never edited — the continuity checker diffs
  against it.
- **Target:** reusable kit; continuity tooling.

### P20 · Progression-state extraction to JSON, validated chapter-over-chapter ★
- **Proven in:** `rpg-progression-design` (mcpmarket) — "automated progression
  engineer": reads narrative chapters, extracts character levels, skill
  acquisitions, attribute changes, and talent specializations into structured
  JSON, enforcing mechanical consistency and power-scaling across the story.
- **Why it matters:** **The single most LitRPG-relevant mechanism in the entire
  field, and nobody else is doing it.** For a 7-book LitRPG, Nate's
  progression (skills, abilities, ranks, stat reveals) must stay mechanically
  consistent across hundreds of chapters. This extracts a ground-truth
  progression ledger from the prose and flags contradictions (a skill used in
  Ch12 that Nate doesn't unlock until Ch15).
- **How we'd build it:** A `progression-state.json` per book, populated by an
  agent reading approved chapters (ties to P13 Chronicler), validated against
  `skill-system-design.md` and the epistemic schedule. Flags mechanical drift.
- **Target:** new tool + Forge MCP; the LitRPG-specific differentiator.

### P21 · Standing-rules-as-files (feedback loaded at session start)
- **Proven in:** `humbrol2/claude-rpg-skill` (player corrections become
  permanent `feedback_*.md` files auto-loaded each session to prevent repeat
  mistakes).
- **Why it matters:** This is **exactly forge-novel's memory system** already
  (the `feedback_*` memory namespace). Independent convergence — validates the
  approach. Nothing to build; note the alignment.
- **Target:** none (already implemented via memory).

---

### Wave 2 — deepening pass (GitHub source repos)

### P22 · Anchored constraints — decisions the editor must NOT "improve" ★
- **Proven in:** `howells/fiction` (`## ⚓ Anchored` marks immutable story
  decisions; review agents treat them as non-negotiable, protecting author
  intent against well-meaning AI "fixes").
- **Why it matters:** **Directly solves a known forge-novel pain.** Our
  audiobook punctuation fixes (fragment joins, deliberate em-dashes) and locked
  canon get "corrected" by editor passes — there's literally a memory telling us
  to *ask before reverting them*. An anchored-marker makes the editor leave them
  alone by construction.
- **How we'd build it:** A lightweight inline marker (or a sidecar list) for
  anchored lines/decisions; `/editors-hat` and prose_lint treat anchored spans
  as read-only — flag, never auto-touch. Covers audio fixes, hard-bans, locked
  canon.
- **Target:** `/editors-hat`, `prose_lint.py` (the audio-flow safeguard).

### P23 · Persona-based critique panel (audience-matched lenses) ★
- **Proven in:** `howells/fiction` (four named literary critics — Wood / King /
  Le Guin / Gay — give orthogonal feedback, not generic notes).
- **Why it matters:** Upgrades the G1 review channels from abstract dimensions
  to **our actual audience**: a *Dresden/Butcher reader* (wit-under-pressure,
  momentum), a *Sanderson-mechanics reader* (progression payoff), an *audiobook
  listener* (does it land in the ear), a *faith-fiction reader* (show-don't-tell
  on theme). Each lens catches what the others miss.
- **How we'd build it:** Define ~4 reader-personas from the 17-book bank + our
  constraints; run them as parallel reviewers in the G1 pipeline. Synthesize.
- **Target:** `/editors-hat` review panel (feeds G1).

### P24 · Parallel reader-extraction for whole-book review ★
- **Proven in:** `howells/fiction` (for 50k+ words, skim/careful "reader" agents
  extract summaries+quotes in parallel, parent synthesizes — ~3-4× faster,
  avoids token-crushing context).
- **Why it matters:** Series-level continuity/critique can't fit a whole book in
  one context. This is the scaling pattern: map (per-chapter extractors) →
  reduce (synthesis). A natural Workflow.
- **How we'd build it:** A Workflow that fans per-chapter extractor agents
  (summary + open threads + canon touched), then a synthesis pass for
  cross-book continuity and arc audit. Pairs with P13 Chronicler.
- **Target:** series-continuity Workflow; reusable kit.

### P25 · Scene-economy rule ("every scene earns its place")
- **Proven in:** `howells/fiction` (scene must do ≥2 things; scene-analyzer
  diagnoses failures). Echoed by greyhaven's "every sentence purposeful."
- **Why it matters:** Concrete, checkable craft gate — the operational form of
  our **"prose must earn its place"** rule (Pass 1.5 Length Discipline).
- **How we'd build it:** An `/editors-hat` scene pass: for each scene, name the
  ≥2 jobs it does (plot/character/world/voice/setup); flag single-purpose
  scenes for cut-or-merge.
- **Target:** `/editors-hat`.

### P26 · Voice-fingerprint schema (SOUL / STYLE-GUIDE / VOICE-PROFILE) ★
- **Proven in:** AuthorClaw (three-file identity: **SOUL** = voice-as-sacred,
  **STYLE-GUIDE** = POV/tense/dialogue-tags/forbidden-words, **VOICE-PROFILE** =
  47 learned markers incl. sentence rhythm, vocabulary, punctuation, *humor
  style*; every output passes through all three).
- **Why it matters:** Concretizes P14 with a **real schema**. The "humor style"
  marker is gold for us (per-voice comedy dial). Splits cleanly: SOUL/STYLE map
  to WRITING_RULES; VOICE-PROFILE = the per-voice fingerprint to generate from
  `voice/exemplars.md`.
- **How we'd build it:** `voice/fingerprints/<voice>.json` carrying ~rhythm,
  diction, punctuation, register, comedy-dial, bans — one per cast voice
  (Storyteller, Nate, Flint, Rex, Judge). Writer targets it; linter scores it.
- **Target:** reusable kit + `prose_lint.py` + `/forge-write` (the P14 build).

### P27 · Ordered revision passes + numeric acceptance gates
- **Proven in:** greyhaven creative-writing (5 sequential passes: structure →
  clarity → voice → trim → polish; SVQ score ≥7.0 = publish-ready;
  disagreement rule: "if one agent flags critical, it is critical").
- **Why it matters:** We already have an editorial pass *order* in WRITING_RULES;
  this adds **numeric gates** (don't advance until the pass clears a threshold)
  and a clean **escalation rule** for the review panel. Tightens G1.
- **How we'd build it:** Each G1 gate emits a 1-5 (or 1-10) score + reasons;
  bounded auto-revision until threshold or loop-cap; any "critical" finding
  blocks regardless of average.
- **Target:** `/editors-hat` (G1 gating logic).

### P28 · Model-by-complexity / free-first routing
- **Proven in:** `howells/fiction` (opus = prose/critique, sonnet = analysis,
  haiku = extraction); AuthorClaw (brainstorm/draft on free/local models, paid
  for nuanced revision).
- **Why it matters:** Cost discipline for the Workflows. Cheap/local passes
  (extraction, lint-adjacent, perplexity) → **Nova/Ollama**; reserve Opus for
  prose and hard critique. Real savings on a 7-book run.
- **How we'd build it:** In the G1/G2 Workflows, set per-agent model by task
  weight; route extraction + perplexity to Nova/Ollama.
- **Target:** Workflow model-routing convention.

### P29 · Canon registry + relationship graph (validate before add)
- **Proven in:** `danjdewhurst/story-skills` (`_index.md` registries, kebab-case
  IDs, bidirectional relationships → queryable knowledge graph; validate refs
  before adding a character/thread).
- **Why it matters:** Our **Forge MCP Codex already is** a relationship graph —
  this validates the design and argues for a *validate-before-add* step (no
  orphan refs, no duplicate entities) when the Chronicler (G2) proposes
  additions.
- **How we'd build it:** Have G2's Chronicler check proposed entities against
  the Codex graph (dedupe, resolve aliases) before surfacing them to David.
- **Target:** G2 Chronicler / Forge MCP integration.

### P30 · Skill-authoring conventions (for packaging the kit) ★
- **Proven in:** `anthropics/skills` official patterns — progressive disclosure
  (purpose → examples → guidelines), self-contained folders bundling reference
  files/templates/checklists/scripts, frontmatter (`name` + when-to-use
  `description`), a terminology section, validation checklists.
- **Why it matters:** This is the **META pattern for the reusable kit** (P16
  Standards layer): how to structure our skills so they're portable, legible,
  and reliably invoked. Our skills are good; this is a packaging checklist to
  level them up and make the kit cleanly extractable.
- **How we'd build it:** When we package the Standards/kit, follow these
  conventions — bundled reference files, a craft-terminology glossary,
  checklists, and tight when-to-use descriptions.
- **Target:** reusable-kit packaging standard.

---

## Idea ledger

Granular one-liners not (yet) promoted to a full pattern. Extend opportunistically
as we build.

| # | Idea | Source family | Style-lens | Candidate target |
|---|---|---|---|---|
| 1 | Separate "concept-validation" gate before outlining | Snowflake step 1 | mechanics | reusable kit |
| 2 | "Humanization" de-slop pass post-draft | Snowflake step 11 | voice | prose_lint adjacent |
| 3 | Recap/"Previously On" generation from chapters | story-narrative-summary, RPG-session-summarizer | mechanics | new util |
| 4 | Progression-as-narrative beats (level-up as story turn) | rpg-progression-design | mechanics | `/forge-write` LitRPG |
| 5 | Fail-forward / "succeed at a cost" beat templates | gm-craft | mechanics | reusable kit |
| 6 | Synopsis generator (short/medium/long) from manuscript | fiction | mechanics | new util |
| 7 | Plot-structure template menu (3-act / hero / save-the-cat / kishōtenketsu) | story-skills | mechanics | outline/`/forge-write` |
| 8 | Hook / transition / ending pattern taxonomies | greyhaven | mechanics | craft reference |
| 9 | Beta-reader simulation (predict reader reactions) | AuthorClaw | mechanics | `/editors-hat` mode |
| 10 | Discovery-draft with TODO placeholders (keep momentum, no stalling) | greyhaven | mechanics | `/forge-write` |
| 11 | Developmental → line → copy edit hierarchy (named tiers) | AuthorClaw | mechanics | `/editors-hat` framing |
| 12 | "Forgotten elements" reminder — surface dropped / unpaid threads | forgotten-elements-reminder (sweep 2) | mechanics | reinforces P8 |
| 13 | Causality/plot-logic analyzer (does effect follow cause across chapters) | l-space causality analyzer (sweep 2) | mechanics | G1 continuity gate |
| 14 | Granular craft micro-tools: opening-sentence generator, pacing optimizer | pacing/tension skills (sweep 2) | mechanics | `/forge-write` sub-abilities |

---

## Action queue — recommended build order

The mine is rich; the discipline is picking the few highest-leverage grafts.
Ranked by **value × fit × effort**, framed for our audiobook-first, LitRPG,
David-steers-Claude-drafts setup.

### Tier 1 — build these (highest leverage)
- **G1 · Editorial pipeline as a Workflow** (P17 + P5 + P12 + P6). One
  `/editors-hat` fan-out: ordered gates (voice/cast-routing → continuity/Codex →
  outline-fidelity → timeline → prose_lint → **audio-flow**) with bounded
  revision loops, each gate a sub-agent tuned to OUR rules. Folds in the
  reader-experience channels (P12) and craft axes (P6). *Biggest single win.*
- **G2 · Chronicler → Codex auto-population** (P13 + P20). After David approves
  a chapter, an agent proposes Forge MCP Codex updates **and** updates a
  `progression-state.json` (the LitRPG ledger), flagging mechanical/continuity
  drift. Proposes only — David confirms. *Solves a real 7-book scaling problem.*
- **G3 · Perplexity gate on Nova/Ollama** (P18). A report-only `prose_lint`
  companion scoring sentence perplexity via local Ollama. Closes the
  already-planned "perplexity gate" phase at zero token cost.

### Tier 2 — strong, do after Tier 1
- **G4 · Voice fingerprints from exemplars** (P14). `voice/fingerprints/<voice>.json`
  that forge-write targets and prose_lint scores against.
- **G5 · Outline-is-law pre-flight** (P2 + P3). forge-write halts-and-asks on
  missing context instead of inventing; minimal current-beat context load.
- **G6 · LitRPG-conventions reference** (P9). Distill the reader-expectation
  contract from the 17-book bank into a checkable reference.

### Tier 3 — architecture + reusable kit
- **G7 · Three-layer split** (P16) as the kit's organizing principle: Standards
  (portable craft) / Novel (forge-novel canon) / Book (per-volume state).
- **G8 · Append-only timeline** (P19) for continuity diffing.
- **G9 · Character-sim discovery mode** (P15); **promise/payoff ledger** (P8);
  **recap generation** (ledger idea #3).

### Explicitly NOT pursuing
- Generic worldbuilding scaffolds (we're past them — REFERENCE.md + 153 Codex
  entities). Chinese-web-novel export targets. EPUB generation (audio is the
  deliverable, not ebooks). Standing-rules system (P21 — already have it).

---

## Source index

Skills/systems examined. **Credited as inspiration only; no text reproduced.**
Note: mcpmarket is largely a *thin catalog* over GitHub repos — the richest
mechanisms live in the source repos below, which is where the deep read went.

**Multi-skill systems (highest-value sources)**
- **Crucible Writing System** — `forsonny/the-crucible-writing-system-for-claude`
  (26★) + `pasteurmonga` fork. Planner + Outliner + Writer; 36-beat;
  Story Bible; 5-agent bi-chapter review; Mercy Engine. → P1,P2,P3,P4,P5,P7,P8,P10.
- **Creative Writing Skills ("muse")** — `haowjy/creative-writing-skills`.
  Muse router; brainstormer/character-sim/outliner/writer/revision-writer/
  critic/chronicler/style-creator; `kb/` knowledge base; 4-channel critic.
  → P11,P12,P13,P14,P15.
- **Novel-OS** — `forsonny/book-os`. Three-layer context (Standards/Novel/
  Manuscripts); progressive context accumulation; command-driven workflow.
  → P16.
- **Claude-Book** — `ThomasHoussin/Claude-Book`. Gated pipeline w/ bounded
  revision loops; **perplexity-improver** (local GPU model); Bible/State/
  Timeline separation. → P17,P18,P19.

**Single skills / references**
- **Snowflake Fiction** — `hestudy/snowflake-fiction` (2★). 5-axis self-check;
  12-step method. Chinese docs + Chinese-web-novel export. → P6.
- **RPG Progression Design** — mcpmarket (progression-state-to-JSON extraction).
  → P20 (the LitRPG-critical idea; logged from description).
- **claude-rpg-skill** — `humbrol2/claude-rpg-skill`. Canon-as-files; append-only
  ledger; feedback-as-standing-rules. → P19,P21.
- **GM Craft** — `rjroy/adventure-engine-corvran`. Fail-forward, NPC motivation.
- **Fantasy World Building** — `ordinary-claude-skills` aggregator (mirrored ×7).
  Generic; we're past it.
- **romance-novel-writing-conventions** — genre-conventions-as-reference. → P9.

**Raw scrape artifacts:** `tmp/mcpscrape/` (sweep_results.json = 664 hits;
triage_kept.json = 240 scored; details/ = original 21 blurbs). *Disposable.*

---

## Coverage & saturation

Two sweeps, 29 search queries total, ~870 cards seen. **The field is now mined
out for distinct mechanisms.** Sweep 1 (17 queries) → the six craft families +
the Crucible/Snowflake systems. Wave 2 (5 GitHub systems) → the real depth
(anchored constraints, persona critics, fingerprint schema, parallel
extraction, model routing, authoring conventions). Sweep 2 (12 fresh
craft-angle queries, 206 new cards) → **only variants and cross-domain noise**
(design systems, UX, code review) plus granular micro-tools that map onto
patterns we already hold. No new major mechanism surfaced.

**Conclusion:** 30 patterns + 14 ideas is a saturated harvest. Further sweeping
yields clones, not capabilities. The leverage is now in *building* the Tier-1
grafts, not mining more.

---

## Note on method (for the next session)

mcpmarket.com **rate-limits / IP-blocks** aggressive scraping (tripped after
~17 rapid queries + scrolling; escalated to blocking the homepage). The working
approach: **gentle single-page pacing** (no scroll, ~9s gaps, warm-up homepage
hit, 120s cooldown) survives fine — sweep 2 ran 12 queries with zero blocks.
For deep content, **go to the GitHub source repos** (no shared rate limit, and
richer — mcpmarket is a thin catalog over them). The Playwright harness lives in
`tmp/mcpscrape/`; reuse `gentle_sweep2.mjs` as the polite template.
