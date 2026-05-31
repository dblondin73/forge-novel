# kit/ — Standards Layer (portable craft tooling)

The genre-agnostic, reusable half of this repo. These tools know nothing of any
specific novel; they bind to a project through a repo-root `kit.config.json`
they **discover** at runtime (see `LAYERS.md`). Copy `kit/` into any prose
project, drop a `kit.config.json` at that repo's root, and the tools work.

**Resolution order for every path / key:** explicit CLI flag > `kit.config.json`
binding > the tool's portable built-in default. With no binding, each tool runs
standalone on built-ins; with the binding present, behavior is identical to a
hardcoded version. **Report-only, always** — no kit tool rewrites prose or
auto-strips anything (em-dashes especially can be deliberate audiobook
stutter-fixes downstream).

## Tools at a glance

| Tool | What it does | Tokens |
|---|---|---|
| `prose_lint/prose_lint.py` | Deterministic AI-tell linter. Report-only. | 0 |
| `prose_lint/prose_lint_hook.py` | PostToolUse wrapper: lints a draft after a Write/Edit, advisory, always exits 0. | 0 |
| `perplexity/prose_predictability.py` | Local-model perplexity spot-checker — flags statistically *flat* sentences. Report-only. | local GPU |
| `preflight/preflight.py` | Outline-is-law pre-flight gate before drafting chapter N. HALT/PASS; never drafts. | 0 |
| `timeline/timeline.py` | Append-only continuity event log: validate, append-only integrity gate (vs git HEAD), event views. Report-only. | 0 |
| `ledger/ledger.py` | Promise/payoff ledger ("Mercy Engine"): validate, overdue-thread sweep, surface planted-but-unpaid threads. Report-only. | 0 |
| `recap/recap.py` | "Previously On" source-pack aggregator: merges timeline + ledger + epistemic for a chapter range. Emits source material, never prose. | 0 |
| `methods/genre-conventions-template.md` | The HONOR/BEND/BREAK genre-contract method template. | — |

## Binding (`kit.config.json`)

Lives at the **repo root** (the Novel layer owns it), not inside `kit/`. Keys:
`pov_character`, and `paths.{epistemic_states, revelation_schedule,
characters_dir, entity_cache, anti_slop, prose_lint_config, timeline, promises,
draft_glob}` — all relative to the repo root. See `kit.config.example.json`. Omit
any key to fall back to the tool's built-in default. (`recap` needs no key of its
own — it reads `timeline`, `promises`, `epistemic_states`, and `pov_character`.)

---

## prose_lint — deterministic AI-tell linter

Scans chapter drafts for the "AI tells" negative prompting can't reliably
suppress — em-dash density, sentence-length uniformity, tricolon overuse, banned
vocabulary, and the `not just X but Y` / `it wasn't X, it was Y` constructions.
**Stdlib-only, deterministic, zero LLM tokens. Reports; never rewrites.**

```bash
python kit/prose_lint/prose_lint.py drafts/ch05-first-blood-draft01.md   # one chapter
python kit/prose_lint/prose_lint.py drafts/                              # all chNN-*.md
python kit/prose_lint/prose_lint.py drafts/ch04-*.md --format json       # machine output
python kit/prose_lint/prose_lint.py drafts/ch05-*.md --report-file reports/
```

Flags: `--config` (default: binding's `prose_lint_config`, else built-in
thresholds), `--anti-slop` (default: binding's `anti_slop`, else
`prose_lint/anti-slop-base.md`), `--format` (`text`|`json`), `--report-file DIR`,
`--fail-on` (`fail`|`warn`|`never`).

### Exit codes

`--fail-on never` (the default) always exits `0`. This is deliberate: the
PostToolUse hook and `editors-hat` Pass 0a both run the linter advisorily, and a
non-zero exit would (a) reject legitimate audiobook em-dash stutter-fixes on
narrated chapters and (b) train the model to game statistical metrics. Use
`--fail-on warn|fail` only for manual gating.

### Path guard

If the target is not a `chNN-*.md` chapter draft, the linter exits `0` silently
and prints nothing — so the Edit/Write hook stays quiet on every other file.

### The audiobook-locked exception

Em-dashes are deliberately added to **narrated** chapters as TTS stutter-fixes;
"audiobook is the primary medium" is forge-novel's master tiebreaker. So the
bound `prose_lint_config.json` carries an `audiobook_locked` flag per chapter. On
a locked chapter the em-dash finding drops to **INFO** and is never a FAIL —
review by hand, never auto-strip. **Every other detector still runs at full
severity on locked chapters.**

### Files + detectors

| File | Role |
|---|---|
| `prose_lint.py` | CLI: binding discovery, arg parsing, anti-slop parsing, orchestration, reporting |
| `prose_lint_rules.py` | one `check_*` detector per AI-tell category |
| `prose_lint_segment.py` | markdown-aware line classification + sentence splitting |
| `anti-slop-base.md` | portable banned-vocab fallback (a bound project overrides via `anti_slop`) |

Detectors: `check_emdash_density`, `check_not_just_construction`,
`check_it_wasnt_x_construction`, `check_banned_vocab` (Tier 1/2 parsed live from
the anti-slop file), `check_fiction_tells`, `check_burstiness`,
`check_participial_stacks`, `check_transition_clustering`,
`check_consecutive_same_ending`, `check_tricolon_density`,
`check_paragraph_uniformity`. To add one: write `check_<name>(doc) -> list[Finding]`
in `prose_lint_rules.py`, append it to `DETECTORS`, and add any threshold to the
built-in defaults in `load_config()`.

---

## prose_predictability — local-model perplexity spot-checker

The **probabilistic cousin** of prose_lint's deterministic burstiness check.
Where prose_lint measures *structural* flatness for free, this measures
*statistical* flatness: it asks a local Ollama model how **predictable** each
sentence is. **Low perplexity = the model saw it coming = AI-flat**; high
perplexity = distinctive voice. **Report only.**

### It is a SPOT-CHECKER, not a bulk scanner

Ollama exposes logprobs only for *generated* tokens, so perplexity of existing
text is computed by **teacher forcing** — one model call *per word*. Always bound
it (`--max-sentences`, default 25). Use it on suspect passages, not whole books.

```bash
python kit/perplexity/prose_predictability.py drafts/ch03-*.md                 # first 25 sentences
python kit/perplexity/prose_predictability.py drafts/ch03-*.md --longest --top 20
python kit/perplexity/prose_predictability.py drafts/ch03-*.md --model gemma3:4b
python kit/perplexity/prose_predictability.py drafts/ch03-*.md --max-sentences 0   # whole chapter (slow!)
```

Flags: `--host`/`$OLLAMA_HOST`, `--model` (default `llama3:latest`),
`--max-sentences` (0=all), `--longest`, `--top N`, `--context-window`,
`--top-logprobs` (max 20, Ollama's cap), `--floor`, `--min-words`. Needs Ollama
reachable; if offline it exits `2` with a clear message. **Build note:** a cheap
one-call-per-sentence "agreement scan" was tried first and did **not**
discriminate flat from distinctive prose — teacher forcing replaced it. `raw: true`
is required or instruct models *comment on* the prose instead of continuing it.

---

## preflight — outline-is-law pre-flight gate

The **front-end** mirror of an after-write invention catch. Before any prose, it
verifies the repo-local context a chapter's beats need is present (outline-is-law,
minimal context). **Stdlib-only, deterministic, zero LLM tokens. Reports
PASS / HALT; never drafts, never fills a gap, never edits.**

```bash
python kit/preflight/preflight.py --chapter 9
python kit/preflight/preflight.py --chapter 9 --beats 3-5 \
    --characters "Nate,Flint,Josie" --entities "Briarknight,Meat Grinder"
python kit/preflight/preflight.py --chapter 9 --fail-on warn   # escalate WARN to exit 3
```

### What it checks (repo-local only)

| Check | Source (via binding) | Severity if missing |
|---|---|---|
| prior-chapter epistemic entry (`after_ch{N-1}`) | `epistemic_states` + `pov_character` | **HALT** |
| this chapter's scheduled reveals (must-advance) | `revelation_schedule` | INFO (never blocks) |
| character sheet per named character | `characters_dir` | **HALT** (or WARN if Codex-only) |
| named entity resolves to cache | `entity_cache` | WARN |

### The outline-beats half is deliberately NOT here

The chapter outline/beats live only in the project's outline store, so that check
stays agent-side. The report says plainly the outline half is agent-side, so a
PASS never over-claims.

### Exit codes & flags

Governed by `--fail-on` (default `halt`): `halt` → exit `3` only on a HALT;
`warn` → exit `3` on HALT-or-WARN; `never` → always `0`. Flags: `--chapter N`
(required), `--beats` (informational), `--characters "A,B"`, `--entities "A,B"`,
`--repo PATH` (default: the binding dir, else CWD), `--pov-character` (default:
binding's `pov_character`), `--fail-on {halt,warn,never}`.

---

## timeline — append-only continuity event log

The third leg of the **P19 discipline** — *Bible / State / Timeline*:

| Leg | What | Mutability | Here |
|---|---|---|---|
| **Bible** | locked canon | read-only while drafting | `REFERENCE.md` + Codex |
| **State** | who-knows-what | versioned, overwritten per chapter | `epistemic-states.json` |
| **Timeline** | what happened | **append-only, never edited** | `timeline.json` |

A timeline is a flat, ordered list of in-world events — one record per thing that
happened, grouped by chapter. Once an event is committed it is **sealed**: you
never edit or delete it. To correct the record you **append** a new event and name
the old `id` in `supersedes`. That immutability is what makes the log a
trustworthy continuity ground-truth: a contradiction between a fresh chapter and
the timeline means *the chapter is wrong*, not that history was quietly rewritten.

```bash
python kit/timeline/timeline.py check                       # validate + append-only gate
python kit/timeline/timeline.py validate                    # structure only
python kit/timeline/timeline.py events --chapter 8          # recorded events for a chapter
python kit/timeline/timeline.py events --chapter 1-6 --format json
python kit/timeline/timeline.py render --chapter 1-3        # human-readable markdown
```

### The deterministic half vs the agent's half

Like `preflight` (which leaves the outline-beats check agent-side), this tool does
only the **deterministic** half: it keeps the log honest (`check`) and **surfaces**
the recorded events (`events`). The **semantic continuity diff** — *does this draft
contradict the record?* — is an editorial judgement and stays agent-side
(`editors-hat` Pass 2). The tool never reads prose and never edits the log.

### The append-only gate (`check`)

`check` runs structural validation **and** compares the working `timeline.json`
against `git HEAD`. Any sealed (committed) event that was **modified** or
**deleted** is a **[BREACH]** (exit `3`); newly **appended** events are fine. If
the file isn't committed yet, or it's not a git work tree, the sealed-history
check is skipped with INFO (nothing is sealed yet). Git output is decoded UTF-8
explicitly so non-ASCII event text never false-positives on Windows.

### Event schema

Required: `id` (stable, unique, never reused), `chapter` (int), `event` (what
happened). Optional: `seq` (order within chapter), `kind`
(`world`/`system`/`character`/`relationship`/`knowledge`/`progression`/`combat`/
`death`/`item`/`location`/`travel`), `who` (list), `where`, `when` (free-text
in-world clock), `supersedes` (id this corrects), `source` (provenance). Validation
errors (duplicate id, missing required field) are **ERROR**; soft issues
(non-monotonic chapter order, unknown `kind`, dangling `supersedes`, duplicate
`(chapter, seq)`) are **WARN**.

### Exit codes & flags (timeline)

Governed by `--fail-on` (default `error`): `error` → exit `3` on BREACH-or-ERROR;
`warn` → exit `3` on WARN+; `never` → always `0`. Flags: `command`
(`check`|`validate`|`events`|`render`), `--timeline PATH` (default: binding's
`timeline`, else `<repo>/timeline.json`), `--repo PATH` (default: binding dir, else
CWD), `--chapter "8"|"1-6"|"1,3,5"`, `--format {text,json,md}`,
`--fail-on {error,warn,never}`.

---

## ledger — promise/payoff continuity ledger ("Mercy Engine")

The companion to the timeline. Where the timeline records *what happened*
(append-only), the ledger records *what was promised* — and whether the story has
paid it back. Every planted promise gets a payoff slot:

| Kind | What it tracks |
|---|---|
| `foreshadow` | a hint planted now that must land later |
| `chekhov` | an object/detail introduced that must matter |
| `mercy` | a compassionate act that must return at the climax (the "Mercy Engine") |
| `debt` | an obligation owed that must be settled |
| `threat` | a danger promised that must be delivered |
| `question` | a mystery posed that must resolve |
| `vow` | a promise a character makes on the page |
| `reveal` | a scheduled information reveal (seeded from `revelation-schedule.json`) |

The point is the **unpaid sweep**: a Chekhov's gun that never fires, a mercy that
never returns, a mystery posed and forgotten is a continuity hole. The tool keeps
the store honest and **surfaces the open threads**; the semantic judgement — does
*this* draft pay off *this* promise? — stays agent-side (`editors-hat` Pass 2),
exactly as preflight leaves the outline-beats check agent-side.

```bash
python kit/ledger/ledger.py check --through 8        # validate + overdue sweep
python kit/ledger/ledger.py validate                 # structure only
python kit/ledger/ledger.py open --through 8         # planted-but-unpaid threads
python kit/ledger/ledger.py open --through 16 --overdue   # only threads past due-by
python kit/ledger/ledger.py render --kind mercy      # markdown, grouped by status
```

### Mutable state, not append-only

Unlike the timeline, the ledger is **mutable state** (the `revelation-schedule.json`
analog, not the `timeline.json` analog): a promise's status legitimately changes
over its life (`open` → `paid`), so there is **no git seal** here. A thread that is
silently dropped surfaces as perpetually `open` — that is the report, not a breach.
The reveal-kind promises are seeded from `revelation-schedule.json`, which remains
the source of truth for *scheduling* (which reveal to advance in a given chapter);
the ledger is the source of truth for *payoff status across all kinds*.

### Overdue needs a frontier

A promise is **overdue** when it is open, has a `due_by_chapter`, and that chapter
has been reached. "Reached" can't be inferred from the data (the ledger holds
future-targeted hint/reveal chapters), so overdue detection requires
`--through N` — the latest drafted chapter. Without it, `check` reports open/paid
counts and tells you to pass `--through`. Overdue is **WARN**, never a hard block:
a 7-book series legitimately holds a promise open across volumes.

### Promise schema

Required: `id` (stable, unique), `kind`, `promise` (what was set up), `planted_chapter`
(int ≥ 1), `status` (`open`/`paid`/`abandoned`/`subverted`). Optional:
`reinforced_chapters` (list), `due_by_chapter` (soft deadline), `payoff` + `paid_chapter`
(filled when paid), `who` (list), `notes`, `source`. Validation errors (duplicate id,
missing required field, bad `planted_chapter`, unknown `status`) are **ERROR**; soft
issues (unknown `kind`, paid-without-`paid_chapter`, open-with-`paid_chapter`,
out-of-order due-by) are **WARN**.

### Exit codes & flags (ledger)

Governed by `--fail-on` (default `error`): `error` → exit `3` on ERROR; `warn` →
exit `3` on WARN+; `never` → always `0`. Overdue threads are WARN, so the default
gate stays green on them. Flags: `command` (`check`|`validate`|`open`|`render`),
`--promises PATH` (default: binding's `promises`, else `<repo>/promises.json`),
`--through N` (frontier chapter), `--overdue` (filter `open` to overdue only),
`--kind K` (filter `render`), `--format {text,json,md}`, `--fail-on {error,warn,never}`.

---

## recap — "Previously On" source-pack aggregator

A thin, zero-token aggregator for a recap. It pulls three already-maintained
stores — the timeline (what happened), the ledger (what's still promised), and
epistemic-states (what the POV learned) — slices each to a chapter range, and
merges them into one **source pack**. It writes **no prose**: the recap itself
("Previously on…") is a Storyteller-voice task and stays agent-side. The tool
gathers the deterministic ground truth; the agent writes from it.

```bash
python kit/recap/recap.py --chapter 1-8              # text source pack
python kit/recap/recap.py --chapter 6 --format md    # markdown
python kit/recap/recap.py --chapter 1-8 --format json
```

Any missing source is skipped with a note, so a partly-wired project still gets a
usable pack. It needs no binding key of its own — it resolves `timeline`,
`promises`, `epistemic_states`, and `pov_character` from the binding (each
overridable: `--timeline`, `--promises`, `--epistemic`, `--pov-character`). It is
a generator, not a gate: exit `0` always.
