# The Three-Layer Model — Standards / Novel / Book

The organizing principle for "a reusable craft kit **and** a specific novel" living
in one repo. Three layers, each narrowing the one above. (Pattern after
`forsonny/book-os`: Standards → Novel → Manuscripts.)

| Layer | What it holds | Lifetime | Owns |
|---|---|---|---|
| **Standards** (`kit/`) | Genre-agnostic craft tooling + methods. Knows nothing of any specific book. | Permanent; portable across projects. | The tool engines, the binding *schema*, the craft *methods*. |
| **Novel** (repo canon) | This book's locked worldbuilding, craft rules, voice, skills, and book-specific orchestration. | The life of the project. | Canon docs, character sheets, the drafting/editing skills, `kit.config.json`. |
| **Book** (per-volume state) | The mutable narrative state the tools read and the author advances. | Per volume; resets each book. | Drafts, epistemic/revelation state, per-chapter flags, caches, reports. |

## The seam: `kit.config.json`

A Standards tool must never hardcode a Novel's filenames or its POV character. The
**Novel layer owns a `kit.config.json` at the repo root**; the Standards tools
**discover** it (walk up from CWD, then from the script dir) and bind to it.

Resolution order for every configurable value:

```
explicit CLI flag  >  kit.config.json binding  >  the tool's portable built-in
```

When no binding is found, each tool runs on built-in defaults — so the kit is
copy-pasteable into a fresh project that supplies its own `kit.config.json`. When
the binding *is* present, the tools behave exactly as a hardcoded version would.

## What lives where (this repo)

- **Standards** — `kit/prose_lint/` (AI-tell linter), `kit/perplexity/`
  (predictability spot-checker), `kit/preflight/` (outline-is-law gate),
  `kit/methods/` (e.g. the genre-conventions HONOR/BEND/BREAK template).
- **Novel** — `REFERENCE.md`, `WRITING_RULES.md`, `LITRPG_CONVENTIONS.md`,
  `characters/`, `voice/`, `.claude/skills/{forge-write,editors-hat}/`,
  `tools/` (chronicler + editorial-fanout Workflows — book-specific
  orchestration), the Codex tooling under the skill's `scripts/`,
  `kit.config.json`.
- **Book** — `drafts/`, `epistemic-states.json`, `revelation-schedule.json`,
  `prose_lint_config.json` (per-chapter `audiobook_locked`), `SESSIONS.md`,
  `reports/`, the entity cache.

## Retargeting the kit to another project

1. Copy `kit/` into the new repo.
2. Write a `kit.config.json` at that repo's root (see `kit.config.example.json`).
3. Provide the Novel layer (canon/voice/skills) and Book layer (state files) the
   binding points at. The Standards tools need no edits.
