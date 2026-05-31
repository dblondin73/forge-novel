# editors-hat fan-out Workflow (G1 — Step 1 MVP)

The parallel execution mode for `/editors-hat`. Runs the **detection** passes as
concurrent reviewer subagents, then synthesizes the canonical Pass 6 report.
**Detection only — it never edits prose.** Design + roadmap:
[research/g1-editorial-pipeline-plan.md](../research/g1-editorial-pipeline-plan.md).

## What it does

1. **Prep** — runs `prose_lint.py --format json` (Pass 0a), then builds the
   **anchored-constraints map** [Step 3]: a do-not-touch list of deliberate spans
   (locked em-dashes, audio punctuation fixes, protected dramatic beats, and
   schedule-withheld reveals from `revelation-schedule.json` / `epistemic-states.json`).
2. **Detect** — fans out **8 rule reviewers + 4 persona critics in parallel** (12 total):
   - *Rule reviewers* each load `.claude/skills/editors-hat/SKILL.md` and apply ONE pass/lens:
     `0b` slop · `1` length · `2` continuity · `3a` theology/true-names ·
     `3b` POV/voice · `3c` language/Lord's-name · `3d` system-intent/Flint · `5` prose/voice + audio-flow.
     (Pass 3 is split into 4 lenses — it's the densest pass today.)
   - *Persona critics* [Step 2] do NOT apply rules; each embodies a reader from the
     17-book bank and reports felt experience: **Dresden reader · audiobook listener ·
     faith-fiction reader · LitRPG-mechanics reader.**

   Every reviewer and persona receives the anchored map and treats anchored spans
   as **flag-only, never edit.**
3. **Comedy** [Step 4] — Pass 4 proposes Dial 4-5 punch-up *opportunities* for the
   non-protected paragraphs, then a **bounded self-check** (≤1 revision) drops any
   proposal that touches a protected beat, smuggles fluff, or over-dials Nate.
4. **Synthesis** — merges + dedupes into three sections — **Craft & rule findings**,
   **Reader experience**, and **Anchored / protected** — honoring the anchored map
   (findings that target anchored spans are dropped or downgraded to "do not act").
   Includes per-dimension scores (incl. `reader-experience`) and a `critical_count`;
   persona/rule agreement is flagged as strong signal.

## How to run

Running spawns ~17 subagents, so it needs the harness **"workflow" opt-in**
(say "run the editors-hat workflow on ch4" or include the word *workflow*):

```js
Workflow({
  scriptPath: 'tools/editors_hat_fanout.workflow.js',
  args: {
    chapter: 'ch04',
    file: 'drafts/ch04-<slug>-draft01.md',
    adjacent: ['drafts/ch03-<slug>-draft01.md', 'drafts/ch05-<slug>-draft01.md']
  }
})
```

- `file` optional — if omitted, reviewers glob `drafts/` for the chapter.
- `adjacent` optional — improves the continuity pass.
- `args` may also be just a path string.

## What it returns

`{ report_markdown, scores, critical_count, summary }` — the same report shape as
today's sequential Pass 6. **You still approve before any fix is applied;** the
Workflow stops at the catalog.

## Model routing (Step 5)

Cost is tiered by task weight (`opts.model` per agent):

- **Opus** — the correctness-critical lenses (`2-continuity`, `3a-theology`,
  `3b-pov-voice`, `3d-system-intent`, `5-prose-voice`) + `synthesis`.
- **Sonnet** — medium-judgement lenses (`0b-slop`, `1-length`, `3c-language`),
  all persona critics, the anchored-map builder, and the whole comedy pass.
- **Haiku** — the near-mechanical `0a-linter` parse.

Tune via `OPUS_LENSES` / `PERSONA_MODEL` at the top of the script.

> **Why not literal Nova/Ollama offload?** The Workflow `model` option is
> Claude-only, and these lenses are judgement-dense — a local model would cost
> accuracy. Genuine local-model offload is the right fit for **G3 (the perplexity
> gate)**, a mechanical scoring task, not this editorial reasoning pass. The cost
> win here is Opus→Sonnet→Haiku tiering, which protects the load-bearing lenses.

## Scope boundary

**G1 complete (Steps 1-5):** anchored-constraints map + parallel rule-detection +
persona critics + the Pass-4 comedy punch-up with bounded self-check + model
tiering + synthesis (report parity, Reader-experience table, Anchored table).

## Notes

- **Rules live in `SKILL.md`, not here.** Reviewers load them at runtime; this
  script is pure orchestration (keeps the craft/code two-efforts split clean).
- Backward compatible: `/editors-hat 3` still runs the normal sequential pass.
- Canonical test chapter for parity checks: **Ch 4** (the reference beat).
