# prose_lint — deterministic AI-tell linter

`prose_lint.py` scans forge-novel chapter drafts for the "AI tells" that
negative prompting cannot reliably suppress — em-dash density, sentence-length
uniformity, tricolon overuse, banned vocabulary, and the `not just X but Y` /
`it wasn't X, it was Y` constructions. It is **stdlib-only**, deterministic, and
costs **zero LLM tokens**. It reports; it never rewrites.

## Usage

```bash
python tools/prose_lint.py drafts/ch05-first-blood-draft01.md   # one chapter
python tools/prose_lint.py drafts/                              # all chNN-*.md
python tools/prose_lint.py drafts/ch04-*.md --format json       # machine output
python tools/prose_lint.py drafts/ch05-*.md --report-file reports/
```

Flags: `--config` (default `tools/prose_lint_config.json`), `--anti-slop`
(default the `forge-write` skill's `references/anti-slop.md`), `--format`
(`text`|`json`), `--report-file DIR` (writes `reports/prose-lint-<ch>-<date>.md`),
`--fail-on` (`fail`|`warn`|`never`).

## Exit codes

`--fail-on never` (the default) always exits `0`. This is deliberate: the
PostToolUse hook and `editors-hat` Pass 0a both run the linter advisorily, and
a non-zero exit would (a) reject legitimate Brigid em-dash stutter-fixes on
narrated chapters and (b) train the model to game statistical metrics. Use
`--fail-on warn|fail` only for manual gating.

## Path guard

If the target is not a `chNN-*.md` chapter draft, the linter exits `0` silently
and prints nothing — so the Edit/Write hook stays quiet on every other file.

## The audiobook-locked exception

Em-dashes are deliberately added to **narrated** chapters as TTS stutter-fixes
for Brigid (ElevenLabs); "audiobook is the primary medium" is the project's
master tiebreaker. So `prose_lint_config.json` carries an `audiobook_locked`
flag per chapter. On a locked chapter the em-dash finding drops to **INFO** and
is never a FAIL — review by hand, never auto-strip. **Every other detector
still runs at full severity on locked chapters.** Set `audiobook_locked: true`
once a chapter has been narrated.

## Files

| File | Role |
|---|---|
| `prose_lint.py` | CLI: arg parsing, anti-slop parsing, orchestration, reporting |
| `prose_lint_rules.py` | one `check_*` detector per AI-tell category |
| `prose_lint_segment.py` | markdown-aware line classification + sentence splitting |
| `prose_lint_config.json` | thresholds + per-chapter `audiobook_locked` flags |

## Detectors

`check_emdash_density`, `check_not_just_construction`,
`check_it_wasnt_x_construction`, `check_banned_vocab` (Tier 1/2 sourced live
from `anti-slop.md`), `check_fiction_tells`, `check_burstiness`
(sentence-length coefficient of variation), `check_participial_stacks`,
`check_transition_clustering`, `check_consecutive_same_ending`,
`check_tricolon_density`, `check_paragraph_uniformity`.

## Adding a detector

1. Write a `check_<name>(doc: Doc) -> list[Finding]` in `prose_lint_rules.py`.
2. Append it to the `DETECTORS` list at the bottom of that file.
3. Add any threshold it needs to `prose_lint_config.json` `defaults` and to the
   built-in fallback in `load_config()`.

Detectors only ever see `doc.prose_lines` / `doc.sentences` — System panels,
headers, scene-break rules, and code fences are already filtered out by
`prose_lint_segment.segment()`.

## Word-level rule source

`check_banned_vocab` parses the Tier 1 table and Tier 2 word list directly out
of `anti-slop.md` at runtime. There is one source of truth — edit that file and
the linter follows. No word lists are duplicated here.

---

## prose_predictability — local-model perplexity spot-checker (G3)

`prose_predictability.py` is the **probabilistic cousin** of `prose_lint`'s
deterministic burstiness check. Where prose_lint measures *structural* flatness
for free, this measures *statistical* flatness: it asks a local model on Nova how
**predictable** each sentence is. **Low perplexity = the model saw it coming =
AI-flat** (cliché openings, stock phrasing); high perplexity = distinctive voice.
Validated discrimination: planted clichés score ppl 10-31, forge-novel prose
800-2300. **Report only — never edits or auto-strips.**

### It is a SPOT-CHECKER, not a bulk scanner

Ollama exposes logprobs only for *generated* tokens, so perplexity of existing
text is computed by **teacher forcing** — one model call *per word*. A 15-word
sentence = 15 calls; 15 sentences ≈ 4 min. Always bound it (`--max-sentences`,
default 25). Use it on suspect passages, not whole books.

```bash
python tools/prose_predictability.py drafts/ch03-first-boot-draft01.md           # first 25 sentences
python tools/prose_predictability.py drafts/ch03-*.md --longest --top 20         # 25 longest, show 20 flattest
python tools/prose_predictability.py drafts/ch03-*.md --model gemma3:4b          # faster model
python tools/prose_predictability.py drafts/ch03-*.md --max-sentences 0          # whole chapter (slow!)
python tools/prose_predictability.py drafts/ch03-*.md --format json --report-file reports/
```

Flags: `--host`/`$OLLAMA_HOST` (default Nova Tailscale), `--model` (default
`llama3:latest`), `--max-sentences` (0=all), `--longest` (score the meatiest
sentences), `--top N` (flattest to print), `--context-window`, `--top-logprobs`
(max 20, Ollama's cap), `--floor` (logprob for words outside top-K), `--min-words`.

### Requires Nova online

Needs Ollama reachable (`tailscale status` → nova active). If Nova is offline the
tool exits `2` with a clear message. Nothing else in the repo depends on it.

### Why teacher-forced (a build note)

A cheap one-call-per-sentence "agreement scan" (does the model reproduce your
sentence?) was built and tested first — it did **not** discriminate flat from
distinctive prose (free continuation never aligns with the next sentence), so it
was replaced by teacher forcing. Two Ollama constraints shape the design: no
prompt/echo logprobs, and `raw: true` is required or instruct models *comment on*
the prose ("What a beautiful passage!") instead of continuing it.

---

## forge_preflight — outline-is-law pre-flight gate (G5)

`forge_preflight.py` is the **front-end** mirror of `check-proper-nouns.py`'s
back-end catch. Where that hook flags *unflagged inventions after* a draft is
written, this verifies — **before** any prose — that the repo-local context a
chapter's beats need is actually present (P2 outline-is-law, P3 minimal context).
**Stdlib-only, deterministic, zero LLM tokens. Reports PASS / HALT; it never
drafts, never fills a gap, never edits.** Invoked by `/forge-write` Step 4.

```bash
python tools/forge_preflight.py --chapter 9
python tools/forge_preflight.py --chapter 9 --beats 3-5 \
    --characters "Nate,Flint,Josie" --entities "Briarknight,Meat Grinder"
python tools/forge_preflight.py --chapter 9 --fail-on warn   # escalate WARN to exit 3
```

### What it checks (repo-local only)

| Check | Source | Severity if missing |
|---|---|---|
| prior-chapter epistemic entry (`after_ch{N-1}`) | `epistemic-states.json` | **HALT** |
| this chapter's scheduled reveals (must-advance) | `revelation-schedule.json` | INFO (never blocks) |
| character sheet per named character | `characters/*.md` | **HALT** (or WARN if Codex-only) |
| named entity resolves to Codex cache | `.forge-known-entities.json` | WARN |

### The forge-side half is deliberately NOT here

The chapter **outline/beats live only in forge-mcp**, so that check (do the beats
exist and are they unwritten?) stays agent-side — `forge_outline_beats`, or the
SSH fallback the skill documents. The report says plainly that the outline half
is agent-side, so a PASS never over-claims. The four checks above are everything
that is locally, deterministically verifiable.

### Exit codes & gating

Governed by `--fail-on` (default `halt`): `halt` → exit `3` only on a HALT;
`warn` → exit `3` on HALT-or-WARN; `never` → always `0`. A `[WARN]` (Codex-only
character, uncached entity) does not stop a draft — it folds into the skill's
Pre-Draft Questions. Only a `[HALT]` (missing epistemic entry, undefined
character, missing beats) stops it cold.

### Flags

`--chapter N` (required), `--beats` (informational), `--characters "A,B"`
(cast for the beats), `--entities "A,B"` (named entities to resolve),
`--repo PATH` (default: parent of `tools/`), `--fail-on {halt,warn,never}`.
The cast/entity lists come from the beats — the agent derives them in Step 4b
(the minimal-context set) and passes them in.
