#!/usr/bin/env python3
"""forge_preflight - deterministic, repo-local pre-flight gate for /forge-write (G5).

Zero LLM tokens. Before any prose is drafted, verify the repo-local half of the
context a chapter's beats need is actually present (P2 outline-is-law, P3 minimal
context). Reports PASS / HALT; it never drafts, never fills a gap, never edits.

It checks what lives in the repo:
  1. prior-chapter epistemic entry  (epistemic-states.json -> after_ch{N-1})
  2. this chapter's scheduled reveals (revelation-schedule.json) -> MUST-ADVANCE
  3. character sheets present         (characters/*.md) for named characters
  4. named entities resolve           (.forge-known-entities.json cache)

The OUTLINE-BEATS check is deliberately NOT here: the beats live only in
forge-mcp, so that half stays agent-side (forge_outline_beats, or the SSH
fallback the skill documents). This tool covers the deterministic local half;
the report says plainly what it did and did not verify.

Usage:
    python tools/forge_preflight.py --chapter 9
    python tools/forge_preflight.py --chapter 9 --beats 3-5 \\
        --characters "Nate,Flint,Josie" --entities "Briarknight,Meat Grinder"
    python tools/forge_preflight.py --chapter 9 --fail-on warn

Exit codes are governed by --fail-on (default: halt -> non-zero only on a HALT),
so the gate can block a careless draft while warnings stay advisory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CACHE_FILE = (
    REPO_ROOT / ".claude" / "skills" / "forge-write" / "scripts"
    / ".forge-known-entities.json"
)

# Severity tags (fixed width so the report columns line up).
HALT = "HALT"   # a hard-required input is missing -> do not draft
WARN = "WARN"   # a soft gap -> note it, draft may proceed with a flag
INFO = "INFO"   # a reminder (e.g. a scheduled reveal) -> never blocks
OK = " OK "     # checked and present
SKIP = " -- "   # not checked (no input given, or agent-side only)

_RANK = {HALT: 3, WARN: 2, INFO: 1, OK: 0, SKIP: 0}


class Finding:
    """One pre-flight result line."""

    __slots__ = ("severity", "check", "detail")

    def __init__(self, severity: str, check: str, detail: str) -> None:
        self.severity = severity
        self.check = check
        self.detail = detail


# --- loaders ---------------------------------------------------------------


def _load_json(path: Path) -> dict | None:
    """Load a JSON file; return None (not {}) if absent or unparseable."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _split_list(raw: str | None) -> list[str]:
    """Split a comma-separated CLI arg into trimmed, non-empty names."""
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- checks ----------------------------------------------------------------


def check_prior_epistemic(chapter: int, repo: Path) -> Finding:
    """The previous chapter's epistemic entry must exist before we draft N."""
    path = repo / "epistemic-states.json"
    data = _load_json(path)
    if data is None:
        return Finding(HALT, "Prior epistemic state",
                       "epistemic-states.json missing or unparseable")
    if chapter <= 1:
        return Finding(OK, "Prior epistemic state",
                       "chapter 1 - no prior entry required")

    prior_key = f"after_ch{chapter - 1:02d}"
    nate = data.get("characters", {}).get("nate", {})
    if prior_key in nate:
        return Finding(OK, "Prior epistemic state",
                       f"{prior_key} present (Nate's knows/doesnt_know loaded)")
    return Finding(HALT, "Prior epistemic state",
                   f"{prior_key} entry missing - Nate's knowledge boundary for "
                   f"ch{chapter:02d} is undefined")


def check_scheduled_reveals(chapter: int, repo: Path) -> list[Finding]:
    """Reveals scheduled for this chapter are MUST-ADVANCE reminders (never block)."""
    path = repo / "revelation-schedule.json"
    data = _load_json(path)
    if data is None:
        return [Finding(WARN, "Scheduled reveals",
                        "revelation-schedule.json missing or unparseable")]

    hits: list[str] = []
    for rev in data.get("revelations", []):
        rid = rev.get("id", "?")
        roles = []
        if rev.get("plant_chapter") == chapter:
            roles.append("PLANT")
        if chapter in (rev.get("hint_chapters") or []):
            roles.append("hint")
        if rev.get("full_reveal_chapter") == chapter:
            roles.append("FULL REVEAL")
        if rev.get("reader_learns_chapter") == chapter:
            roles.append("reader-learns")
        if roles:
            hits.append(f"{rid} ({'/'.join(roles)})")

    if not hits:
        return [Finding(OK, "Scheduled reveals",
                        f"no revelation scheduled for ch{chapter:02d}")]
    return [Finding(INFO, "Scheduled reveals",
                    f"ch{chapter:02d} MUST advance: " + "; ".join(hits))]


def _find_sheet(name: str, repo: Path) -> Path | None:
    """Match a character name to a characters/*.md sheet by filename token.

    "Nate" -> nate-hall.md, "Josie" -> josie-pickett.md, "Flint" -> flint.md.
    A sheet matches if the lowercased name (or its first token) is one of the
    sheet stem's hyphen-split tokens.
    """
    chars_dir = repo / "characters"
    if not chars_dir.is_dir():
        return None
    key = name.strip().lower().split()[0] if name.strip() else ""
    if not key:
        return None
    for sheet in sorted(chars_dir.glob("*.md")):
        tokens = sheet.stem.lower().split("-")
        if key in tokens:
            return sheet
    return None


def check_character_sheets(characters: list[str], repo: Path,
                           cache_names: set[str]) -> list[Finding]:
    """Each named character needs a sheet, or at least a Codex-cache entry."""
    if not characters:
        return [Finding(SKIP, "Character sheets",
                        "no --characters given (agent supplies the beat's cast)")]
    findings: list[Finding] = []
    for name in characters:
        sheet = _find_sheet(name, repo)
        if sheet is not None:
            findings.append(Finding(OK, "Character sheet",
                                    f'"{name}" -> {sheet.name}'))
        elif name in cache_names or name.split()[0] in cache_names:
            findings.append(Finding(WARN, "Character sheet",
                                    f'"{name}" - no sheet in characters/; '
                                    f"Codex-only (use entity data, note the gap)"))
        else:
            findings.append(Finding(HALT, "Character sheet",
                                    f'"{name}" - no sheet AND not in Codex cache; '
                                    f"identity undefined"))
    return findings


def check_entities(entities: list[str], cache_names: set[str],
                   cache_loaded: bool) -> list[Finding]:
    """Named entities should resolve against the live Codex cache."""
    if not entities:
        return [Finding(SKIP, "Entities",
                        'no --entities given (pass the beat\'s named entities to check)')]
    if not cache_loaded:
        return [Finding(WARN, "Entities",
                        ".forge-known-entities.json absent - run "
                        "scripts/refresh-entity-cache.py; cannot resolve names")]
    findings: list[Finding] = []
    for name in entities:
        if name in cache_names or name.split()[0] in cache_names:
            findings.append(Finding(OK, "Entity", f'"{name}" resolves to Codex cache'))
        else:
            findings.append(Finding(WARN, "Entity",
                                    f'"{name}" not in Codex cache - new entity to '
                                    f"create, mark [INVENTED:], or refresh the cache"))
    return findings


# --- orchestration + report ------------------------------------------------


def run_preflight(chapter: int, characters: list[str], entities: list[str],
                  repo: Path) -> list[Finding]:
    cache = _load_json(CACHE_FILE)
    cache_loaded = cache is not None
    cache_names = set(cache.get("all_names", [])) if cache_loaded else set()

    findings: list[Finding] = []
    findings.append(check_prior_epistemic(chapter, repo))
    findings.extend(check_scheduled_reveals(chapter, repo))
    findings.extend(check_character_sheets(characters, repo, cache_names))
    findings.extend(check_entities(entities, cache_names, cache_loaded))
    # The outline-beats check is agent-side by design (beats live in forge-mcp).
    findings.append(Finding(SKIP, "Outline beats",
                            "agent-side - run forge_outline_beats (or the SSH "
                            "fallback) to confirm the beats exist and are unwritten"))
    return findings


def render_text(chapter: int, beats: str | None, findings: list[Finding]) -> str:
    head = f"forge pre-flight - Chapter {chapter}"
    if beats:
        head += f" (beats {beats})"
    lines = [head, "=" * len(head), ""]
    width = max((len(f.check) for f in findings), default=0)
    for f in findings:
        lines.append(f"[{f.severity}]  {f.check.ljust(width)}  {f.detail}")
    lines.append("")

    halts = sum(1 for f in findings if f.severity == HALT)
    warns = sum(1 for f in findings if f.severity == WARN)
    if halts:
        lines.append(f"RESULT: HALT - {halts} blocking gap(s). Do NOT draft. "
                     f"Resolve, or raise each as a pre-draft question.")
    elif warns:
        lines.append(f"RESULT: PASS with {warns} warning(s). Note them; "
                     f"drafting may proceed.")
    else:
        lines.append("RESULT: PASS. Repo-local context present. Confirm the "
                     "outline-beats check agent-side, then draft.")
    lines.append("(Repo-local gate only - the outline-beats half is agent-side.)")
    return "\n".join(lines)


def exit_code(findings: list[Finding], fail_on: str) -> int:
    worst = max((_RANK[f.severity] for f in findings), default=0)
    if fail_on == "never":
        return 0
    if fail_on == "warn":
        return 3 if worst >= _RANK[WARN] else 0
    return 3 if worst >= _RANK[HALT] else 0  # fail_on == "halt" (default)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic repo-local pre-flight gate for /forge-write (G5)")
    parser.add_argument("--chapter", type=int, required=True,
                        help="target chapter number (e.g. 9)")
    parser.add_argument("--beats", default=None,
                        help="beat range, informational only (e.g. 3-5)")
    parser.add_argument("--characters", default=None,
                        help='comma-separated cast for the beats, e.g. "Nate,Flint"')
    parser.add_argument("--entities", default=None,
                        help='comma-separated named entities, e.g. "Briarknight"')
    parser.add_argument("--repo", type=Path, default=REPO_ROOT,
                        help="forge-novel repo root (default: parent of tools/)")
    parser.add_argument("--fail-on", choices=("halt", "warn", "never"),
                        default="halt", help="exit non-zero threshold (default: halt)")
    args = parser.parse_args()

    findings = run_preflight(
        chapter=args.chapter,
        characters=_split_list(args.characters),
        entities=_split_list(args.entities),
        repo=args.repo,
    )
    print(render_text(args.chapter, args.beats, findings))
    sys.exit(exit_code(findings, args.fail_on))


if __name__ == "__main__":
    main()
