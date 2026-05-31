# G1 — Editorial Pipeline as a Workflow: Build Plan

> **For David's approval before any code.** Turns the existing `/editors-hat`
> sequential pipeline into a parallel **Workflow** fan-out, grafting in the
> harvested patterns (anchored constraints, persona critics, parallel
> extraction, gated scoring, model routing). Source: `skill-mining-fantasy-writing.md`
> grafts G1/P5/P12/P17/P22/P23/P24/P27/P28.

---

## What this is — and isn't

- **Augments, does not replace.** The current sequential `/editors-hat` stays as
  the default. The Workflow is a new *execution mode* for the same rules.
- **Orchestration, not rules.** Every editorial rule stays in
  `editors-hat/SKILL.md` (the single source of truth). The Workflow *calls* those
  rules from parallel agents; it does not restate or fork them.
- **Code effort, not craft effort.** Per the two-efforts split, this touches
  scripts/orchestration only — zero changes to the editorial rules themselves.
- **Preserves the contract.** Catalog-then-approve-then-apply is kept: agents
  *detect* in parallel, David approves, fixes apply grouped by chapter. No agent
  mutates prose unprompted.

---

## Current state (what we're restructuring)

`/editors-hat` runs **one agent, eight passes, in strict order**, in a single
context:

`0a` deterministic linter → `0b` judgement slop → `1` length discipline →
`2` continuity → `3` rule compliance (+ marks protected beats) → `4` comedy
punch-up (needs 1+3) → `5` prose/voice + audio-flow → `6` merged report.

Most passes **catalog findings only**; fixes apply after approval. That means the
detection passes are *independent* and parallelizable — the sequential ordering
is mostly convention, not hard dependency. Only two real dependencies exist:
**Pass 4 needs Pass 1 (trim map) + Pass 3 (protected beats)**, and **Pass 6
synthesizes everything**.

---

## Target architecture — five Workflow phases

```
A. PREP (parallel, cheap)            B. DETECTION FAN-OUT (parallel, the work)
   ├─ 0a linter (script, no model)      ├─ 0b slop-judgement
   ├─ anchored-map builder [P22]        ├─ 2  continuity (Codex + adjacent ch)
   └─ reader-extraction [P24]           ├─ 3  rule-compliance (split into lenses)
      (multi-chapter only)              ├─ 5  prose/voice + AUDIO-FLOW gate
                                        ├─ 1  length-discipline (KEEP/TRIM/CUT)
                                        └─ persona critics [P23] ×4
                                            │
C. DEPENDENT (after 1+3) ───────────────────┘
   └─ 4 comedy punch-up (respects protected beats + anchored map)

D. SYNTHESIS [P5/P27]                 E. APPROVAL + BOUNDED FIX [P27]
   ├─ dedupe across all reviewers        ├─ present unified table (Source col)
   ├─ conflict resolution (anchored      ├─ David approves (current behavior)
   │   map wins; protected beats win)    └─ apply grouped → re-run 0a + light
   └─ "one critical = critical" gate         recheck on changed spans; ≤1 loop
```

Every Phase-B/C agent receives the **same packet**: the chapter text, the
**anchored map** (Phase A), the linter output (0a), and — for multi-chapter
runs — the continuity context from reader-extraction. Each returns **structured
findings** (location, severity, rule, suggested fix), never mutates prose.

---

## Pass → agent mapping

| Pass | Agent(s) | Phase | Parallel? | Model [P28] |
|---|---|---|---|---|
| 0a linter | script (Bash) | A | n/a | none |
| anchored-map | builder | A | with 0a | Sonnet/Haiku |
| reader-extract | per-chapter | A | yes (multi-ch) | Haiku / Nova |
| 0b slop | 1 reviewer | B | yes | Sonnet |
| 1 length | 1 reviewer | B | yes | Sonnet |
| 2 continuity | 1 reviewer (Codex+adjacent) | B | yes | Opus |
| 3 rule-compliance | **split**: theology/true-names · POV/voice-routing · language/Lord's-name · system-intent | B | yes (4 lenses) | Opus |
| 5 prose/voice + audio-flow | 1 reviewer | B | yes | Opus |
| persona critics | Dresden · audiobook-listener · faith-fiction · LitRPG-mechanics | B | yes (×4) | Sonnet |
| 4 comedy punch-up | 1 reviewer | C | after 1+3 | Opus |
| 6 synthesis/report | reducer | D | n/a | Opus |

Splitting Pass 3 into four lenses is the biggest accuracy win — it's the densest
pass today (theology, true-names, POV, language-rating, system-intent,
nickname, flint-throttle all in one). Parallel lenses each go deep on one
ruleset instead of one agent skimming all of them.

---

## New grafts, concretely

### Anchored-constraints map [P22] — the audio-flow safeguard
Phase A builds a **do-not-touch map** before any reviewer runs. It marks:
- **Locked-chapter em-dashes** (linter already reports INFO not FAIL — formalize).
- **Audiobook punctuation fixes** (fragment joins, deliberate Brigid stutter-fixes).
- **Protected dramatic beats** (Pass 3 already marks these — promote to the map so
  Pass 4 + persona critics *cannot* punch them up).
- **Scheduled-reveal withholdings** (epistemic-states / revelation-schedule — a
  reviewer must not "fix" something deliberately withheld).

Every downstream agent treats anchored spans as **flag-only, never edit**. This
directly kills the recurring pain where an editor pass "improves" a deliberate
audio fix. In synthesis, any finding that targets an anchored span is dropped
(or downgraded to FYI).

### Persona critics [P23] — audience-felt lenses
Four reader-personas drawn from the 17-book bank + our constraints, each
returning *felt-experience* findings, not rule-checks:
- **Dresden reader** — wit-under-pressure, momentum, dry-voice landings.
- **Audiobook listener** — does it land in the ear; voice collisions; Brigid flow.
- **Faith-fiction reader** — show-don't-tell on theme; any drift toward sermon.
- **LitRPG-mechanics reader** — progression payoff, stat-reveal satisfaction,
  crunch guardrails.

### Parallel reader-extraction [P24] — multi-chapter scaling
For `/editors-hat 1-5` or `all`, per-chapter extractor agents pull
summary + open threads + canon touched, so the continuity reviewer gets
cross-chapter context **without loading every chapter into one window**.

### Gated scoring + disagreement rule [P27]
Synthesis applies: **any finding marked `critical` is critical regardless of
averages.** Optional per-dimension 1-5 score for a quick chapter dashboard.
Bounded revision: after fixes apply, re-run 0a + a light recheck on changed
spans; if a fix introduced a new violation, **one** auto-revision loop, then
hand back to David.

### Model routing [P28]
Cheap/mechanical work (extraction, anchored-map, lighter lenses) → Sonnet/Haiku
or **Nova/Ollama**; judgement-dense work (continuity, rule lenses, prose/voice,
comedy, synthesis) → Opus. Real savings on `all`-chapter runs.

---

## Invocation / UX

- **Backward compatible.** `/editors-hat 3` keeps today's sequential behavior.
- **New mode:** `/editors-hat 3 --workflow` (or `/editors-hat all --workflow`)
  triggers the fan-out. Workflow runs require the harness "workflow" opt-in, so
  it's never auto-invoked.
- **Output is identical in shape** — the same Pass 6 table with the `Source`
  column, plus an optional per-dimension score line. David's approve-then-apply
  step is unchanged.

---

## Build steps (phased — MVP first)

> **Status (2026-05-30): G1 COMPLETE (Steps 1-5 BUILT)** —
> `tools/editors_hat_fanout.workflow.js` (+ README). Step 1 validated live on Ch3
> (`reports/ch03-editorial-fanout-2026-05-30.md`): caught a real POV break,
> overrode linter false-positives, cross-chapter continuity worked. Steps 2
> (persona critics), 3 (anchored-constraints map), 4 (comedy + bounded
> self-check), and 5 (model tiering Opus/Sonnet/Haiku) built + syntax-checked.
> **Not yet run live with all five steps together.** Note on Step 5: literal
> Nova/Ollama offload is not applicable (Workflow model option is Claude-only;
> lenses are judgement-dense) — the cost win is Claude-tier routing. Local-model
> offload belongs to G3 (perplexity gate).

1. **MVP — detection fan-out + synthesis.** Workflow script: Phase A (0a + a
   first-cut anchored map) → Phase B (0b, 1, 2, 3-as-4-lenses, 5) → Phase D
   synthesis into the existing report table. *No personas, no Nova, no comedy
   loop yet.* Proves the parallel structure and the report parity.
2. **Add persona critics [P23]** as four Phase-B agents; fold their felt-findings
   into synthesis.
3. **Add the anchored-map safeguard [P22]** in full (audio fixes + protected
   beats + scheduled reveals) and wire the "drop findings on anchored spans" rule.
4. **Add Pass 4 comedy (Phase C)** with the 1+3 dependency and protected-beat
   respect, then the bounded re-check loop [P27].
5. **Model routing / Nova [P28]** for the cheap lenses; measure cost/quality.

Each step is independently shippable and testable against a known chapter
(Ch 4 is the canonical reference beat).

---

## Open decisions for David

1. **Execution model** — new `--workflow` mode that augments (recommended) vs
   replacing the sequential pipeline outright.
2. **Persona set** — the four proposed lenses, or a different cut.
3. **Nova/Ollama routing** — use local models for cheap lenses (saves tokens,
   needs Nova up) vs all-Claude (simpler, costlier).
4. **MVP scope** — full pipeline vs the thin Step-1 MVP first.

---

## What this does NOT change
- No edits to any editorial rule in `editors-hat/SKILL.md`.
- No change to the approve-then-apply contract or the draft01-in-place workflow.
- `prose_lint.py` stays the deterministic, zero-token, report-only Pass 0a.
