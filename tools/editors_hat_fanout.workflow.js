export const meta = {
  name: 'editors-hat-fanout',
  description: 'G1 (complete, Steps 1-5) — anchored-constraints map, parallel rule reviewers + persona critics (honoring the map), comedy punch-up with bounded self-check, model-tiered (Opus/Sonnet/Haiku) for cost, then synthesis into the Pass 6 + Reader-experience + Anchored tables. Detection only; no prose is edited.',
  phases: [
    { title: 'Prep', detail: '0a deterministic linter + anchored-constraints map (do-not-touch)' },
    { title: 'Detect', detail: '8 rule reviewers (0b, 1, 2, 3×4 lenses, 5) + 4 persona critics (Dresden / audiobook / faith / LitRPG)' },
    { title: 'Comedy', detail: 'Pass 4 punch-up proposals + bounded self-check (≤1 revision)' },
    { title: 'Synthesis', detail: 'merge + dedupe (honoring anchors) → Pass 6 + Reader-experience + Anchored tables' },
  ],
}

// ---------------------------------------------------------------------------
// G1 Step-1 MVP. Run via the Workflow tool:
//   Workflow({ scriptPath: 'tools/editors_hat_fanout.workflow.js',
//              args: { chapter: 'ch04',
//                      file: 'drafts/ch04-...-draft01.md',
//                      adjacent: ['drafts/ch03-...-draft01.md','drafts/ch05-...-draft01.md'] } })
// Running spawns ~10 subagents — needs the harness "workflow" opt-in.
// MVP scope: detection + synthesis ONLY. No personas / anchored-map / comedy /
// Nova routing yet (those are Steps 2-5 in research/g1-editorial-pipeline-plan.md).
// The editorial RULES are not restated here — every reviewer loads them live
// from .claude/skills/editors-hat/SKILL.md.
// ---------------------------------------------------------------------------

const SKILL = '.claude/skills/editors-hat/SKILL.md'
const LINTER = 'c:/Workbench/dev/forge-novel/tools/prose_lint.py'

const a = (typeof args === 'string') ? { file: args } : (args || {})
const chapter = a.chapter || (a.file ? a.file : 'the target chapter')
const fileHint = a.file
  ? `The draft file is: ${a.file}`
  : `No explicit path given — find the draft under drafts/ matching ${chapter} (pattern chNN-*-draft01.md).`
const adjacent = Array.isArray(a.adjacent) ? a.adjacent : []
const adjLine = adjacent.length
  ? `For continuity, you may also read the adjacent chapters: ${adjacent.join(', ')}.`
  : `If you need adjacent chapters for continuity, glob drafts/ for the chapter before and after.`

// Uniform finding shape across linter + every reviewer.
const FINDINGS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          category: { type: 'string', description: 'short rule/pass name, e.g. "POV discipline", "em-dash density"' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor', 'info'] },
          location: { type: 'string', description: 'line number(s) or quoted anchor text' },
          issue: { type: 'string', description: 'what is wrong, concise' },
          suggested_fix: { type: 'string', description: 'proposed prose fix or action (do NOT apply it)' },
        },
        required: ['category', 'severity', 'location', 'issue'],
      },
    },
  },
  required: ['findings'],
}

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    report_markdown: { type: 'string', description: 'the Pass 6 table: | Category | Chapter | Issue | Severity | Location | Source |' },
    scores: { type: 'object', additionalProperties: { type: 'number' }, description: 'optional 1-5 per dimension' },
    critical_count: { type: 'number' },
    summary: { type: 'string' },
  },
  required: ['report_markdown', 'summary'],
}

// Step 3 — anchored-constraints map [P22]. Built in Phase A, BEFORE reviewers run.
const ANCHORED_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    audiobook_locked: { type: 'boolean' },
    anchors: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          location: { type: 'string', description: 'line number(s), "global", or quoted anchor text' },
          type: { type: 'string', enum: ['emdash-locked', 'audio-punctuation', 'protected-beat', 'withheld-reveal'] },
          reason: { type: 'string', description: 'why it is deliberate / what must not be done to it' },
        },
        required: ['location', 'type', 'reason'],
      },
    },
    summary: { type: 'string' },
  },
  required: ['anchors', 'summary'],
}

// Step 4 — bounded re-check on comedy proposals [P27].
const COMEDY_CHECK_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    ok: { type: 'boolean' },
    problems: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          location: { type: 'string' },
          problem: { type: 'string' },
        },
        required: ['location', 'problem'],
      },
    },
  },
  required: ['ok', 'problems'],
}

const reviewBase = `You are an editorial reviewer for the forge-novel ghostwriting project (Book 1 of a Christian LitRPG; the audiobook is the primary deliverable).
${fileHint}
${adjLine}
First, load the editorial rules from ${SKILL} and read the chapter. Apply ONLY your assigned pass/lens below — do not duplicate other passes.
DETECT ONLY: catalog findings; do NOT edit prose and do NOT rewrite the file. A suggested fix is fine, but it is a proposal for David, not an edit.
Where a finding is measurable, reuse the linter's exact line numbers (provided) instead of recounting.`

// The Detect fan-out. Pass 3 is split into 4 lenses (its densest pass today).
const LENSES = [
  { key: '0b-slop', title: 'Pass 0b — judgement slop (reading-comprehension tells the linter cannot measure)',
    instruction: 'Cover ONLY: over-explain/restating-the-shown, too-polished dialogue (want >=1 imperfect line/scene), scene-vs-summary balance (>=70% in-scene), stability trap (conflicts resolving too cleanly), predictable emotional arcs, repetitive chapter endings vs adjacent chapters. Do not repeat any word-level/structural tell the linter already found.' },
  { key: '1-length', title: 'Pass 1 — length discipline (prose must earn its place)',
    instruction: 'Mark paragraphs KEEP / TRIM / CUT per the earn-its-place test. For CUT, name the failure mode (restating-shown / list-redundancy / epistemic-reassurance / voice-redundancy / hedge / physical-detail-no-return). Counterweight: Dial 4-5 voice density is load-bearing, not fluff — cut what is flat, keep what is voicey.' },
  { key: '2-continuity', title: 'Pass 2 — continuity & flow',
    instruction: 'Check against adjacent chapters for duplicated scenes, contradictions, timeline issues, callback consistency (pump, mockingbird, Congressman, etc.), and carry-over of character positions/inventory. Flag any scene written twice (esp. at chapter boundaries).' },
  { key: '3a-theology', title: 'Pass 3 lens A — theology / cosmology / true-names',
    instruction: 'Check ONLY: unified-source theology (System = rebranded framework, never neutral tech; energy/substrate never "dirty"; permission not protection), Conduit amplification shown via effect only, skill-system taxonomy ("sub-skill" banned; biblical Gift names writer-facing only), and true-names vs false-labels (System labels, never names; "true name" term banned in Book 1; rancher-authentic faculty common-names). Never let cosmology vocabulary leak into prose.' },
  { key: '3b-pov-voice', title: 'Pass 3 lens B — POV discipline & voice routing',
    instruction: 'Check ONLY: no lens labels ("the [gamer/engineer/ranch/Christian] in him"), POV discipline (Nate narrates only what he senses; System data routed through Flint/Storyteller; show effects not UI), Rex/Judge pack-bond delivery (impressions not explanations; Scots/Aussie lexicon in Nate channel; Flint never hears the bond), Storyteller weave (no dead-middle stretch; correct Hiberno vs plain register), bold-on-System-terms, and SA spell-out cadence.' },
  { key: '3c-language', title: 'Pass 3 lens C — language rating & nickname discipline',
    instruction: 'Check ONLY: Lord\'s-name-in-vain (ABSOLUTE, every voice incl. villains and Storyteller-Hiberno — substitute from the Morningstar/System/Pit palette), Nate spoken-profanity cap (3-5 per ~5k words; dialogue + audible only, NOT interior/italic thought; prorate for short chapters), and nickname discipline (grep King/Sarge/Boss/Pretty etc. — none before their in-story introduction beat).' },
  { key: '3d-system-intent', title: 'Pass 3 lens D — system-intent & Flint throttle',
    instruction: 'Check ONLY: system-intent discipline (AI-behavior verbs ALLOWED — decides/infers/adapts/watches; STILL flag transcendent/metaphysical attribution, literal human emotion, future-knowledge the AI cannot have), Flint design-intent throttle (early Book 1 must hedge design-intent claims; no quantum self-diagnosis), and the System-as-corruption contrasts carried in prose rhythm only (never named by a character before the dividing point).' },
  { key: '5-prose-voice', title: 'Pass 5 — prose & voice polish + audio-flow',
    instruction: 'Check ONLY: per-character voice consistency (Storyteller register, Flint, Nate, pack-bond, Josie, Marcus), the voice-transition READ-ALOUD test (tonal bridge / grounding re-anchor / self-contained fragment / callback-fragment grounding for every Storyteller<->Nate<->Flint handoff), and sentence-length burstiness (flag 3+ same-length runs; cross-check linter CV). Audio flow is the tiebreaker.' },
]

// Step 2 — persona critics [P23]. These do NOT apply project rules; each EMBODIES
// a reader from David's 17-book bank and reports felt experience. Pure audience lens.
const personaBase = `You are a READER experiencing this chapter, not a rule-checker. ${fileHint}
Read the chapter (use the Read tool so you can cite line numbers) and report your FELT experience as this specific reader — where the chapter grips you, loses you, or breaks the spell — in your own terms.
You do NOT know the project's internal rules and must not apply them; you only know what works on YOU as a reader.
DETECT ONLY: report reactions as findings, never edit. Use severity "major" for a moment that pulled you out of the story, "minor" for a wobble, and "info" for a positive ("this lands beautifully — protect it"). Cite line numbers or quoted anchors. Keep it to your strongest ~6-10 reactions; do not itemize everything.`

const PERSONAS = [
  { key: 'persona-dresden', title: 'The Dresden / Butcher reader',
    identity: 'Your shelf is The Dresden Files and Iron Druid. You read for dry wit under pressure, humor threaded through danger, and relentless momentum — short beats that never let you set the book down, escalating stakes with permanent cost. Watch for: scenes that idle without a hook; banter that tries too hard, falls flat, or over-stacks and buries the beat; dramatic pivots that lack the quiet around them to breathe; and one-liners that land so well they must be protected.' },
  { key: 'persona-audiobook', title: 'The audiobook listener (hears the full cast)',
    identity: 'You are LISTENING, not reading. Brigid narrates with Irish warmth; Nate (Sam Elliott register), Flint (theatrical), and Rex/Judge (Scots/Aussie) are voiced. You have NO whitespace and NO paragraph breaks — only pauses of indeterminate length. Watch for: voice collisions where two voices hand off jarringly by ear; anything that needs the EYE to parse (an antecedent across a scene break, a fragment whose sense depends on layout, a callback that sounds like the narrator randomly repeating herself); stretches with no voice variation where your attention drifts; and names/terms that are ambiguous by ear.' },
  { key: 'persona-faith', title: 'The faith-fiction reader (Narnia model)',
    identity: 'You love Lewis and the Narnia model: you want the spiritual shape shown through story and NEVER preached. You catch the theme without being told — and you also notice when faith is so absent a beat rings hollow. Watch BOTH directions: any drift toward sermon (a line that tells the theology, names the presence, or explains what should be shown through effect) AND any place the spiritual layer is so buried the beat reads as empty where it should resonate. Flag faith-through-action that lands beautifully (protect it).' },
  { key: 'persona-litrpg', title: 'The LitRPG-mechanics reader',
    identity: 'Your shelf is Primal Hunter, He Who Fights With Monsters, Dungeon Crawler Carl, Cradle. You read LitRPG for EARNED progression and satisfying system payoff — but you have been burned by spreadsheet-creep and menu-pausing. Watch for: progression that feels unearned or skipped (a power-up with no setup or cost); a stat/skill reveal that lands flat after a buildup; crunch that breaks immersion (a stat block too long, the hero pausing the action to read a menu, loadout-optimization creep); and the genre dopamine of a well-earned system beat going MISSING where the scene set it up. Flag a system beat that lands perfectly (protect it).' },
]

// Step 5 — model routing [P28]. Correctness-critical lenses stay on Opus;
// medium-judgement lenses + personas + comedy run on Sonnet; the near-mechanical
// linter-parse runs on Haiku. Tunable: edit OPUS_LENSES / the per-agent model.
// NOTE: genuine Nova/Ollama offload is NOT used here — the Workflow model option
// is Claude-only, and these lenses are judgement-dense (a local model would cost
// quality). Local-model offload is the right fit for G3 (the perplexity gate),
// not this editorial reasoning pass. The win here is Haiku/Sonnet/Opus tiering.
const OPUS_LENSES = new Set(['2-continuity', '3a-theology', '3b-pov-voice', '3d-system-intent', '5-prose-voice'])
const PERSONA_MODEL = 'sonnet'

// ===========================================================================
phase('Prep')
log(`Editing ${chapter} — running deterministic linter (0a) first.`)

const lint = await agent(
  `Run the forge-novel deterministic prose linter and return its findings as structured data — do not edit anything.
${fileHint}
Run via Bash:  python ${LINTER} <draftfile> --format json
(If only a chapter id was given, first glob drafts/ for the matching chNN-*-draft01.md file.)
Parse the JSON output and map each linter finding into the schema: category = the rule/detector name (e.g. "em-dash density", "banned vocabulary", "burstiness CV"); severity = FAIL->major, WARN->minor, INFO->info; location = the reported line number(s); issue = the linter's message; leave suggested_fix empty.
IMPORTANT: on audiobook-locked chapters, em-dashes are reported INFO (deliberate Brigid stutter-fixes) — keep them as info, never flag for stripping.`,
  { label: '0a-linter', phase: 'Prep', schema: FINDINGS_SCHEMA, model: 'haiku' },
)

const lintJson = JSON.stringify(lint?.findings ?? [])

log('Building the anchored-constraints map (do-not-touch) before reviewers run.')
const anchored = await agent(
  `You build the ANCHORED-CONSTRAINTS MAP for an editorial pass on ${chapter} — the do-not-touch list, produced BEFORE any reviewer runs. Anchored spans are DELIBERATE authorial / audiobook choices that reviewers must FLAG-ONLY: never edit, strip, rephrase, or "fix", and never propose naming/clarifying a deliberately withheld reveal.
${fileHint}
Read the chapter, and also read these repo files to ground the map:
- revelation-schedule.json and epistemic-states.json (repo root) — list every reveal or fact scheduled for AFTER this chapter; the chapter deliberately withholds them.
- WRITING_RULES.md — the audiobook-punctuation rule (deliberate em-dashes / fragment-joins are Brigid TTS stutter-fixes).
The deterministic linter findings are below; em-dash findings marked INFO indicate this chapter is audiobook-locked: ${lintJson}

Return anchors of these types (be precise and CONSERVATIVE — only anchor genuinely deliberate spans):
- "emdash-locked": if the chapter is audiobook-locked, anchor em-dashes globally (deliberate Brigid stutter-fixes — never strip). One global entry suffices.
- "audio-punctuation": specific deliberate fragment-joins or sentence fragments functioning as audio stutter-fixes.
- "protected-beat": dramatic pivots that must NOT be punched up for comedy — grief, death, faith-through-action, prayer-as-stillness, anomaly-mechanic reveal, conversion, a Storyteller register-drop from Dial 4-5 to 2-3.
- "withheld-reveal": facts/reveals the chapter deliberately holds back per the schedule (a mechanic not yet named, a true-name term, a System-origin truth) that a reviewer must NOT "fix" by clarifying or paying off here.
Set audiobook_locked accordingly. Cite line numbers or quoted anchors.`,
  { label: 'anchored-map', phase: 'Prep', schema: ANCHORED_SCHEMA, model: 'sonnet' },
)
const anchoredJson = JSON.stringify(anchored?.anchors ?? [])
const anchoredBlock = `ANCHORED-CONSTRAINTS MAP (do-not-touch — these are DELIBERATE choices). Treat every span below as FLAG-ONLY: never propose editing, stripping, rephrasing, or "fixing" it; never propose naming/clarifying/paying-off a withheld reveal in this chapter. If your analysis would flag an anchored span, SUPPRESS that finding (or note only that it is intentional and already-handled). Map:
${anchoredJson}`

// ===========================================================================
phase('Detect')
log(`Fanning out ${LENSES.length} rule reviewers + ${PERSONAS.length} persona critics.`)

// Rule reviewers and persona critics run concurrently (shared concurrency cap).
const [reviews, personaReviews] = await Promise.all([
  parallel(
    LENSES.map((L) => () =>
      agent(
        `${reviewBase}

YOUR ASSIGNED LENS: ${L.title}
${L.instruction}

Linter findings already computed for this chapter (reuse these line numbers; do not recount):
${lintJson}

${anchoredBlock}

Return ONLY findings for your assigned lens.`,
        { label: L.key, phase: 'Detect', schema: FINDINGS_SCHEMA, model: OPUS_LENSES.has(L.key) ? 'opus' : 'sonnet' },
      ),
    ),
  ),
  parallel(
    PERSONAS.map((P) => () =>
      agent(
        `${personaBase}

YOU ARE: ${P.title}
${P.identity}

${anchoredBlock}

Return ONLY your felt reactions as this reader.`,
        { label: P.key, phase: 'Detect', schema: FINDINGS_SCHEMA, model: PERSONA_MODEL },
      ),
    ),
  ),
])

// ===========================================================================
// Phase C — Pass 4 comedy punch-up (DEPENDENT: needs Pass 1 length + protected
// beats, both available now). Proposes only; then a bounded self-check [P27].
phase('Comedy')
const lengthFindings = reviews[LENSES.findIndex((L) => L.key === '1-length')]?.findings ?? []

log('Pass 4 — proposing comedy punch-ups (respecting protected beats + length).')
let comedy = await agent(
  `${reviewBase}

YOUR ASSIGNED PASS: Pass 4 — Comedy Punch-Up (Dial 4-5 calibration). This runs AFTER length (Pass 1) and protected-beat identification — honor both.
Apply the per-voice Comedy Dial matrix from ${SKILL} (Nate dialogue 3-4, Nate close-third 4, Storyteller-omniscient 4-5 variable, Storyteller physical-zoom 4 / 2-3 in combat, Flint 5, pack-bond 3). For each paragraph that is NOT protected/anchored and sits BELOW its target dial, propose a punch-up using the Dial 4+ landing rules (specific nouns, 2-3 stacked punchlines, named targets, italic breaks, let Flint run).
HARD CONSTRAINTS: never punch up a protected/anchored beat (the register-island contrast IS the signal); do not propose punching a line the length pass marked CUT; every proposal is a SUGGESTION for David, not an edit.
Length-pass findings (avoid punching CUT / flat lines): ${JSON.stringify(lengthFindings)}

${anchoredBlock}

Return findings: category "Comedy punch-up", location, severity "info" (opportunity) or "minor" (clear under-calibration), issue = which voice/dial gap, suggested_fix = the proposed punch-up.`,
  { label: '4-comedy', phase: 'Comedy', schema: FINDINGS_SCHEMA, model: 'sonnet' },
)

// Bounded re-check: comedy punch-up can smuggle fluff or touch a protected beat.
const comedyCheck = await agent(
  `You QA the comedy punch-up proposals below for a forge-novel pass on ${chapter}. Load ${SKILL} for the earn-its-place rule, banned vocabulary, and the protected-beat / Dresden-coexistence rules.
Flag any proposal that: (a) punches up a protected/anchored beat, (b) smuggles NEW fluff failing earn-its-place (stacked beats that don't escalate, Flint lines with no new theatricality), (c) introduces banned vocabulary or an AI-tell, or (d) over-eggs Nate past Dial 4 out loud.
${anchoredBlock}
Proposals: ${JSON.stringify(comedy?.findings ?? [])}
Return ok=true with empty problems if all clean; else ok=false listing the problem proposals.`,
  { label: '4-comedy-check', phase: 'Comedy', schema: COMEDY_CHECK_SCHEMA, model: 'sonnet' },
)

if (comedyCheck && comedyCheck.ok === false && (comedyCheck.problems || []).length) {
  log(`Comedy QA flagged ${comedyCheck.problems.length} proposal(s) — one bounded revision.`)
  comedy = await agent(
    `Revise ONLY the flagged comedy proposals; keep the clean ones unchanged. Drop or rework each flagged proposal so it no longer violates the QA note (protected-beat, earn-its-place, banned vocab, or Nate over-dial).
QA problems: ${JSON.stringify(comedyCheck.problems)}
Current proposals: ${JSON.stringify(comedy?.findings ?? [])}
${anchoredBlock}
Return the full revised findings set.`,
    { label: '4-comedy-revised', phase: 'Comedy', schema: FINDINGS_SCHEMA, model: 'sonnet' },
  )
}

// ===========================================================================
phase('Synthesis')

const labeled = [{ source: '0a-linter', findings: lint?.findings ?? [] }]
LENSES.forEach((L, i) => labeled.push({ source: L.key, findings: reviews[i]?.findings ?? [] }))
PERSONAS.forEach((P, i) => labeled.push({ source: P.key, findings: personaReviews[i]?.findings ?? [] }))
labeled.push({ source: '4-comedy', findings: comedy?.findings ?? [] })
const totalFindings = labeled.reduce((n, b) => n + b.findings.length, 0)
log(`Synthesizing ${totalFindings} findings from ${labeled.length} sources.`)

const report = await agent(
  `You are the synthesis/report step (Pass 6) for a forge-novel editorial pass on ${chapter} (Book 1 of a Christian LitRPG; the audiobook is the primary deliverable).
You are given findings from four source types:
  • the deterministic linter ("0a-linter"),
  • rule reviewers (pass/lens keys like "2-continuity", "3a-theology"),
  • the comedy pass ("4-comedy") — these are punch-up OPPORTUNITIES / suggestions, not defects,
  • persona critics (sources prefixed "persona-") — these are READER-EXPERIENCE reactions, not rule violations.
Merge them into ONE report. Render "4-comedy" rows inside the Craft & rule table with a clear "(opportunity)" marker so David reads them as optional punch-ups, not problems.

Rules:
- Dedupe findings at the same location + same issue across reviewers (keep the most specific wording; list contributing sources). A persona reaction that coincides with a rule finding is strong signal — note the agreement.
- Resolve conflicts conservatively: any "critical" stays critical ("one critical = critical").
- ANCHORED MAP (do-not-touch, provided below): DROP any finding that proposes editing / stripping / rephrasing / "fixing" an anchored span, or that proposes naming / clarifying / paying-off a withheld reveal. If such a finding carries genuinely separate signal, downgrade it to severity "info" with the note "anchored — do not act". Em-dashes on an audiobook-locked chapter are anchored: never surface a "reduce em-dashes" action.
- Do NOT propose applying fixes; this is a catalog for David to approve.
- report_markdown has THREE sections:
  1. "## Craft & rule findings" — table with columns | Category | Chapter | Issue | Severity | Location | Source | (Source = "linter" for 0a, else "editorial (<lens>)").
  2. "## Reader experience" — a SEPARATE table for the persona critics with columns | Reader | Reaction | Severity | Location | so their felt responses stay distinct from rule-checks. Lead with the strongest reactions; include "protect this" positives (severity info).
  3. "## Anchored / protected (shielded — do not touch)" — a short list of the anchored spans, so David sees what was shielded from edits this pass.
- scores: 1-5 per dimension (slop, length, continuity, rule-compliance, prose-voice) PLUS "reader-experience" (a composite of how the four personas felt) — 5 = clean/delightful.
- critical_count: number of critical findings (craft + reader combined).
- summary: 3-4 sentence headline — worst craft issues first, then the dominant reader-experience signal (e.g., "the audiobook listener and Dresden reader both flagged X").

ANCHORED MAP (do-not-touch) for this chapter:
${anchoredJson}

Findings (JSON):
${JSON.stringify(labeled)}`,
  { label: 'synthesis', phase: 'Synthesis', schema: REPORT_SCHEMA, model: 'opus' },
)

return report
