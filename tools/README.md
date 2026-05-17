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
