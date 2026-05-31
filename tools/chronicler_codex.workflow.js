export const meta = {
  name: 'chronicler-codex',
  description: 'G2 MVP (Chronicler → Codex) — after a chapter is approved, mine it for new Codex entities and for Nate\'s mechanical progression, dedup against REFERENCE.md (Codex proxy), flag mechanical/epistemic/reveal drift, and emit PROPOSED forge_codex calls + a progression-state.json delta for David to confirm. Proposes only; never writes canon.',
  phases: [
    { title: 'Extract', detail: 'parallel: Codex-entity candidates + progression (skills/abilities/ranks/stats)' },
    { title: 'Validate', detail: 'dedup vs REFERENCE.md (P29) + drift vs skill-system-design / epistemic / reveal schedule' },
    { title: 'Synthesis', detail: 'proposal report: Codex changes + progression-state.json delta + drift flags + copy-ready calls' },
  ],
}

// ---------------------------------------------------------------------------
// G2 Step-1 MVP. Run via the Workflow tool:
//   Workflow({ scriptPath: 'tools/chronicler_codex.workflow.js',
//              args: { chapter: 'ch03',
//                      file: 'drafts/ch03-first-boot-draft01.md' } })
// Spawns 4 subagents (2 extractors + validate + synthesis) — needs the
// harness "workflow" opt-in.
//
// PROPOSES ONLY. This Workflow never writes canon, the ledger, or the schedule.
// It returns a report; David confirms; an apply step (manual now) executes.
//
// FORGE-MCP CAVEAT: the authoritative 153-entity Codex lives only in forge-mcp.
// This MVP dedups against REFERENCE.md, a PROSE REBUILD of the Codex (last
// rebuilt 2026-04-09) — so dedup is best-effort and may lag the live Codex.
// When forge_codex tools are session-live, the increment swaps in a live read.
// Design rationale + increments: research/g2-chronicler-codex-plan.md
// ---------------------------------------------------------------------------

const REFERENCE = 'REFERENCE.md'                              // Codex prose proxy (dedup target)
const SKILLS = 'research/skill-system-design.md'              // progression ground truth
const EPISTEMIC = 'epistemic-states.json'                     // what the POV character knows when
const SCHEDULE = 'revelation-schedule.json'                   // scheduled reveals (don't pay early)
const PROGRESSION = 'progression-state.json'                  // running ledger (may not exist yet)

const a = (typeof args === 'string') ? { file: args } : (args || {})
const chapter = a.chapter || (a.file ? a.file : 'the target chapter')
const fileHint = a.file
  ? `The approved chapter draft is: ${a.file}`
  : `No explicit path given — find the draft under drafts/ matching ${chapter} (pattern chNN-*-draft01.md).`

// New Codex entities / updates the chapter introduces or touches. [P13]
const ENTITY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    entities: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          name: { type: 'string', description: 'canonical entity name as it should appear in the Codex' },
          entity_type: { type: 'string', enum: ['character', 'creature', 'item', 'location', 'faction', 'mechanic', 'ability', 'event', 'other'] },
          status: { type: 'string', enum: ['new', 'update', 'uncertain'], description: 'new entity, update to an existing one, or unsure (flag for David)' },
          codex_ref: { type: 'string', description: 'existing Codex number if matched in REFERENCE.md, e.g. "#64"; empty if none' },
          proposed_description: { type: 'string', description: '1-3 sentence Codex-style entry (for a new entity) OR the specific delta (for an update)' },
          evidence: { type: 'string', description: 'line number(s) or short quote that introduces/changes this entity' },
          notes: { type: 'string', description: 'optional: alias concerns, ambiguity, why uncertain' },
        },
        required: ['name', 'entity_type', 'status', 'proposed_description', 'evidence'],
      },
    },
  },
  required: ['entities'],
}

// Nate's (and companions') mechanical progression deltas. [P20]
const PROGRESSION_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    progression: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          character: { type: 'string', description: 'whose progression — usually "Nate"; also Rex/Judge/Flint/cohort' },
          kind: { type: 'string', enum: ['skill', 'ability', 'rank', 'stat', 'class', 'loadout', 'resource', 'other'] },
          name: { type: 'string', description: 'the skill/ability/stat/class name as shown or implied' },
          change: { type: 'string', enum: ['gained', 'advanced', 'revealed', 'used', 'lost', 'changed'] },
          detail: { type: 'string', description: 'what specifically — value, rank, context' },
          evidence: { type: 'string', description: 'line number(s) or short quote' },
          drift_suspected: { type: 'boolean', description: 'true if this looks inconsistent with prior chapters or the skill system (the validator will confirm)' },
        },
        required: ['character', 'kind', 'name', 'change', 'detail', 'evidence'],
      },
    },
  },
  required: ['progression'],
}

// Validate/diff agent output — dedup + drift, the barrier step.
const VALIDATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    codex_proposals: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          action: { type: 'string', enum: ['create', 'update', 'uncertain'] },
          entity_type: { type: 'string' },
          name: { type: 'string' },
          codex_ref: { type: 'string', description: 'existing Codex # for an update; empty for create' },
          proposed_body: { type: 'string', description: 'the Codex entry text to create, or the precise edit for an update' },
          evidence: { type: 'string' },
          dedup_note: { type: 'string', description: 'how this was matched/deduped against REFERENCE.md; flag aliases and staleness risk' },
        },
        required: ['action', 'entity_type', 'name', 'proposed_body', 'evidence'],
      },
    },
    progression_delta: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          character: { type: 'string' },
          kind: { type: 'string' },
          name: { type: 'string' },
          change: { type: 'string' },
          detail: { type: 'string' },
          evidence: { type: 'string' },
        },
        required: ['character', 'kind', 'name', 'change', 'detail', 'evidence'],
      },
    },
    drift_flags: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          kind: { type: 'string', enum: ['mechanical', 'epistemic', 'reveal', 'continuity'] },
          issue: { type: 'string' },
          location: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor', 'info'] },
        },
        required: ['kind', 'issue', 'severity'],
      },
    },
    summary: { type: 'string' },
  },
  required: ['codex_proposals', 'progression_delta', 'drift_flags', 'summary'],
}

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    report_markdown: { type: 'string', description: 'the full proposal report (sections below)' },
    progression_state_json: { type: 'string', description: 'a JSON fragment to MERGE into progression-state.json (do not write it — return as text)' },
    proposed_codex_calls: {
      type: 'array',
      description: 'copy-ready proposed forge_codex calls, one per Codex change',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          action: { type: 'string', enum: ['create', 'update', 'uncertain'] },
          entity_type: { type: 'string' },
          name: { type: 'string' },
          codex_ref: { type: 'string' },
          body: { type: 'string' },
        },
        required: ['action', 'name', 'body'],
      },
    },
    counts: { type: 'object', additionalProperties: { type: 'number' } },
    summary: { type: 'string' },
  },
  required: ['report_markdown', 'summary'],
}

const projectBase = `This is the forge-novel ghostwriting project — Book 1 of a 7-book Christian LitRPG series. The Codex is the canon registry (153 entities). You are the CHRONICLER: you mine an APPROVED chapter for canon to keep the Codex and the progression ledger current.
${fileHint}
DETECT/PROPOSE ONLY: you NEVER write canon and NEVER edit the chapter. Everything you return is a PROPOSAL for David to confirm.
Cite evidence as line numbers (use the Read tool so you can cite) or short quotes for every item.`

// ===========================================================================
phase('Extract')
log(`Chronicler: mining ${chapter} for new Codex entities + progression deltas.`)

// Two independent extractors run concurrently, then a barrier so the validator
// can dedup/cross-check all candidates at once.
const [entityOut, progOut] = await Promise.all([
  agent(
    `${projectBase}

YOUR JOB — CODEX ENTITY EXTRACTION.
Read the chapter and list every entity it INTRODUCES or MATERIALLY CHANGES that the Codex should track: named characters, creatures/monsters, items/gear, locations, factions/groups, named mechanics/systems, and named abilities.
For each: give the canonical name, entity_type, a 1-3 sentence Codex-style description (or, for an update, the specific new fact), and the line evidence.
Decide status:
- "new" if you believe the Codex has no entry for it,
- "update" if it extends an entity the Codex almost certainly already has (Nate, Flint, Rex, Judge, the System, Thornlings, etc.) — set codex_ref if you can name the number,
- "uncertain" if you cannot tell — DO NOT guess a number; flag it in notes.
Be CONSERVATIVE about "new": minor scenery and one-off descriptive nouns are NOT Codex entities. A thing earns an entry if it has a proper name, recurring significance, or mechanical/worldbuilding weight.
Do NOT dedup against the Codex yourself (the next step does that against REFERENCE.md) — just extract and best-guess status.`,
    { label: 'entities', phase: 'Extract', schema: ENTITY_SCHEMA, model: 'sonnet' },
  ),
  agent(
    `${projectBase}

YOUR JOB — PROGRESSION EXTRACTION (the LitRPG ledger). [P20]
Read the chapter and extract every mechanical progression event for Nate and his companions/cohort: skills or abilities gained or advanced, rank changes, stat/attribute reveals or changes, class developments, loadout/inventory changes, and resource state (lives, health, etc.) where the chapter makes it explicit.
Ground your reading in the skill system: read ${SKILLS} for the Domain→Skill→Ability hierarchy and the Conduit-Gift category, so you classify each event correctly and use the right names. Remember the in-prose discipline: the book shows effects, rarely raw numbers — infer the mechanical event from what is shown, and cite the line.
For each event: character, kind, name, change, detail, evidence. Set drift_suspected=true if an event looks inconsistent with what you'd expect this early (e.g. an ability used before it could be unlocked) — the validator will confirm.
Capture explicit System-panel readouts verbatim in detail where present.`,
    { label: 'progression', phase: 'Extract', schema: PROGRESSION_SCHEMA, model: 'sonnet' },
  ),
])

const entitiesJson = JSON.stringify(entityOut?.entities ?? [])
const progressionJson = JSON.stringify(progOut?.progression ?? [])

// ===========================================================================
phase('Validate')
log('Dedup vs REFERENCE.md (Codex proxy) + drift vs skill-system / epistemic / schedule.')

const validated = await agent(
  `${projectBase}

YOUR JOB — VALIDATE & DIFF (P29 validate-before-add). You are given raw extractions; turn them into clean, deduped PROPOSALS and flag drift.

Read these canon sources:
- ${REFERENCE} — the Codex proxy (a PROSE REBUILD of the live 153-entity Codex, last rebuilt 2026-04-09). Use it to dedup. CAVEAT: it may LAG the live Codex, so when you match an entity, say so in dedup_note and note residual staleness risk; when you cannot find an entity, prefer action "create" but acknowledge it might already exist live.
- ${SKILLS} — the skill-system ground truth, for mechanical-drift checks.
- ${EPISTEMIC} — what each character knows at each chapter boundary, for epistemic-drift checks.
- ${SCHEDULE} — the revelation schedule, for reveal-timing checks.

ENTITY CANDIDATES (raw): ${entitiesJson}
PROGRESSION EVENTS (raw): ${progressionJson}

Produce:
1. codex_proposals — one per real Codex change. Dedup against REFERENCE.md and against each other (resolve aliases — e.g. a nickname vs the canonical name are ONE entity). action: "create" (genuinely absent), "update" (extends an existing entry — set codex_ref to the # from REFERENCE.md), or "uncertain" (ambiguous — explain in dedup_note). Write proposed_body as the Codex entry text (create) or the precise added/changed fact (update). DROP pure scenery that doesn't earn an entry.
2. progression_delta — the cleaned, de-duplicated progression events to record in progression-state.json.
3. drift_flags — inconsistencies, each typed:
   - "mechanical": an event that contradicts ${SKILLS} or an earlier chapter (a skill used before it could exist; a rank that skips a step).
   - "epistemic": the chapter has the POV character know/use something ${EPISTEMIC} says they don't know yet.
   - "reveal": the chapter pays off or names a reveal BEFORE its scheduled chapter in ${SCHEDULE} (the Codex may hold the full truth, but the in-world reveal must not run ahead of schedule).
   - "continuity": any other canon contradiction.
   Severity: "critical" only for a hard canon contradiction; else major/minor/info.
Be conservative: when unsure an entity is new, prefer "update"/"uncertain" over minting a duplicate.`,
  { label: 'validate', phase: 'Validate', schema: VALIDATE_SCHEMA, model: 'opus' },
)

// ===========================================================================
phase('Synthesis')
const codexProposals = validated?.codex_proposals ?? []
const progDelta = validated?.progression_delta ?? []
const driftFlags = validated?.drift_flags ?? []
log(`Synthesizing ${codexProposals.length} Codex proposal(s), ${progDelta.length} progression delta(s), ${driftFlags.length} drift flag(s).`)

const report = await agent(
  `You are the SYNTHESIS step of the Chronicler (G2) for forge-novel ${chapter}. Assemble a single PROPOSAL report for David to confirm. PROPOSE ONLY — never write canon.

You are given validated proposals (already deduped and drift-checked):
- codex_proposals: ${JSON.stringify(codexProposals)}
- progression_delta: ${JSON.stringify(progDelta)}
- drift_flags: ${JSON.stringify(driftFlags)}

Produce:

report_markdown with FOUR sections:
  1. "## Proposed Codex changes" — table: | Action | Type | Name | Codex# | Proposed entry / delta | Evidence |. Group create vs update; put any "uncertain" rows last with a clear "(confirm: new or existing?)" marker.
  2. "## Progression ledger delta" — table: | Character | Kind | Name | Change | Detail | Evidence |. This is the LitRPG ground-truth ledger for this chapter.
  3. "## Drift & continuity flags" — table: | Kind | Severity | Issue | Location |. If empty, say "No drift detected." Lead with critical/major.
  4. "## How to apply" — one short paragraph: these are proposals; forge_codex calls are in proposed_codex_calls (run when forge tools are session-live); the progression delta is in progression_state_json (merge into progression-state.json — created on first confirmed run). Remind that REFERENCE.md dedup may lag the live Codex, so sanity-check create-vs-update against the live Codex before applying.

progression_state_json: a JSON fragment to MERGE into progression-state.json. Use this shape (return as a STRING, do not write a file):
{"book":1,"characters":{"<char>":{"by_chapter":{"${chapter}":[{"kind":"...","name":"...","change":"...","detail":"...","evidence":"..."}]}}}}
Include one entry per progression_delta item, grouped by character. If progression_delta is empty, return "{}".

proposed_codex_calls: one object per codex_proposals row — action, entity_type, name, codex_ref (empty for create), body (the entry text or the update delta). These map 1:1 to forge_codex create/update calls.

counts: { codex_create, codex_update, codex_uncertain, progression_events, drift_critical, drift_total }.

summary: 2-3 sentences — how many Codex changes and progression events, then the most important drift flag (or "no drift"). Note explicitly that nothing was written.`,
  { label: 'synthesis', phase: 'Synthesis', schema: REPORT_SCHEMA, model: 'opus' },
)

return report
