#!/usr/bin/env python3
"""timeline - append-only continuity event log + integrity gate.

Zero LLM tokens. The third leg of the P19 discipline:

    Bible (canon)   -> read-only during drafting   (REFERENCE.md / Codex)
    State (knowledge) -> versioned, overwritten per chapter (epistemic-states)
    Timeline (events) -> APPEND-ONLY, never edited  (this tool's store)

A timeline is a flat, ordered list of in-world events, one record per thing that
happened, grouped by chapter. Once an event is committed it is *sealed*: you
never edit or delete it. To correct the record you APPEND a new event that
supersedes the old one (reference its id in `supersedes`). That immutability is
what makes the log a trustworthy continuity ground-truth - a contradiction
between a fresh chapter and the timeline means the *chapter* is wrong, not that
history was quietly rewritten.

This tool does the deterministic half of continuity work:
  * validate        - the store is well-formed (unique ids, required fields)
  * check           - validate + APPEND-ONLY integrity vs git HEAD (the gate)
  * events          - print the recorded events for a chapter (ground truth to
                      diff a draft against - the SEMANTIC diff stays agent-side)
  * render          - human-readable markdown of the log

The semantic continuity diff (does this draft contradict the recorded events?)
is an editorial judgement and stays agent-side, exactly as preflight leaves the
outline-beats check agent-side. This tool keeps the log HONEST and SURFACES it.

STANDARDS-LAYER TOOL: it knows nothing of any specific novel. The Novel layer
binds it to its own files via a repo-root kit.config.json that this tool
DISCOVERS (walking up from CWD, then the script dir). Resolution order for the
timeline path is: explicit --timeline flag > kit.config.json paths.timeline >
portable built-in default (<repo>/timeline.json).

Usage:
    python kit/timeline/timeline.py check
    python kit/timeline/timeline.py validate
    python kit/timeline/timeline.py events --chapter 8
    python kit/timeline/timeline.py events --chapter 8 --format json
    python kit/timeline/timeline.py render --chapter 1-6
    python kit/timeline/timeline.py check --fail-on warn

Exit codes are governed by --fail-on (default: error -> non-zero only on a
BREACH or structural ERROR), so the gate can block a sealed-history rewrite
while soft warnings stay advisory.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BINDING_FILENAME = "kit.config.json"
DEFAULT_TIMELINE_NAME = "timeline.json"

# Severity tags (fixed width so the report columns line up).
BREACH = "BREACH"  # a sealed (committed) event was edited or deleted -> append-only violated
ERROR = "ERROR "  # the store is structurally invalid (bad json, dup id, missing field)
WARN = "WARN  "   # a soft issue (non-monotonic order, unknown kind, dangling supersedes)
INFO = "INFO  "   # advisory (not in git yet, n events appended)
OK = "  OK  "     # checked and clean

_RANK = {BREACH: 3, ERROR: 3, WARN: 2, INFO: 1, OK: 0}

# `kind` is a free taxonomy; these are the recognised values (others -> WARN, not blocked).
KNOWN_KINDS = {
    "world", "system", "character", "relationship", "knowledge",
    "progression", "combat", "death", "item", "location", "travel",
}

REQUIRED_FIELDS = ("id", "chapter", "event")


class Finding:
    """One timeline-check result line."""

    __slots__ = ("severity", "check", "detail")

    def __init__(self, severity: str, check: str, detail: str) -> None:
        self.severity = severity
        self.check = check
        self.detail = detail


# --- kit binding discovery -------------------------------------------------


def find_binding() -> Path | None:
    """Locate kit.config.json by walking up from CWD, then from this script."""
    seen: set[Path] = set()
    for start in (Path.cwd(), SCRIPT_DIR):
        for d in (start, *start.parents):
            if d in seen:
                continue
            seen.add(d)
            cand = d / BINDING_FILENAME
            if cand.is_file():
                return cand
    return None


def load_binding() -> tuple[dict, Path | None]:
    """Return (binding-dict, binding-base-dir); ({}, None) when none found."""
    binding = find_binding()
    if binding is None:
        return {}, None
    try:
        data = json.loads(binding.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, None
    return data, binding.parent


# --- loading + normalising -------------------------------------------------


def load_events(text: str) -> list[dict]:
    """Parse a timeline document's text into its events list (raises on bad json)."""
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("timeline root must be a JSON object")
    events = data.get("events", [])
    if not isinstance(events, list):
        raise ValueError("timeline `events` must be a list")
    return events


def event_key(ev: dict) -> str:
    """The stable identity of an event (its id), used for sealed-history diffing."""
    return str(ev.get("id", ""))


def normalise(ev: dict) -> dict:
    """A canonical, order-insensitive view of an event for content comparison.

    Two sealed events compare equal iff every recorded field matches. JSON object
    key order and list identity are irrelevant; only values matter.
    """
    return {k: ev[k] for k in sorted(ev) if not str(k).startswith("_")}


# --- structural validation -------------------------------------------------


def validate_events(events: list[dict]) -> list[Finding]:
    findings: list[Finding] = []
    seen_ids: dict[str, int] = {}
    seen_chap_seq: dict[tuple, str] = {}
    last_chapter = 0
    id_set = {event_key(ev) for ev in events if isinstance(ev, dict)}

    for idx, ev in enumerate(events):
        where = f"events[{idx}]"
        if not isinstance(ev, dict):
            findings.append(Finding(ERROR, "Event shape", f"{where} is not an object"))
            continue

        # required fields
        for field in REQUIRED_FIELDS:
            if field not in ev or ev[field] in (None, "", []):
                findings.append(Finding(ERROR, "Required field",
                                        f"{where} missing/empty `{field}`"))

        # id uniqueness
        eid = event_key(ev)
        if eid:
            if eid in seen_ids:
                findings.append(Finding(ERROR, "Duplicate id",
                                        f'id "{eid}" reused ({where} and '
                                        f"events[{seen_ids[eid]}])"))
            else:
                seen_ids[eid] = idx

        # chapter type + ordering
        chap = ev.get("chapter")
        if isinstance(chap, int) and chap >= 1:
            if chap < last_chapter:
                findings.append(Finding(WARN, "Append order",
                                        f'{where} chapter {chap} appears after '
                                        f"chapter {last_chapter} - append events in "
                                        f"chapter order"))
            last_chapter = max(last_chapter, chap)
        elif chap is not None:
            findings.append(Finding(ERROR, "Chapter value",
                                    f"{where} chapter must be an int >= 1 (got {chap!r})"))

        # (chapter, seq) uniqueness when seq is given
        seq = ev.get("seq")
        if seq is not None:
            if not isinstance(seq, int) or seq < 1:
                findings.append(Finding(WARN, "Seq value",
                                        f"{where} seq should be an int >= 1 (got {seq!r})"))
            elif isinstance(chap, int):
                cs = (chap, seq)
                if cs in seen_chap_seq:
                    findings.append(Finding(WARN, "Duplicate seq",
                                            f"ch{chap} seq {seq} used by both "
                                            f'"{eid}" and "{seen_chap_seq[cs]}"'))
                else:
                    seen_chap_seq[cs] = eid

        # kind taxonomy (advisory)
        kind = ev.get("kind")
        if kind is not None and kind not in KNOWN_KINDS:
            findings.append(Finding(WARN, "Unknown kind",
                                    f'{where} kind "{kind}" not in the known set '
                                    f"({', '.join(sorted(KNOWN_KINDS))})"))

        # supersedes must point at a real id
        sup = ev.get("supersedes")
        if sup not in (None, "", []):
            refs = sup if isinstance(sup, list) else [sup]
            for ref in refs:
                if ref not in id_set:
                    findings.append(Finding(WARN, "Dangling supersedes",
                                            f'{where} supersedes "{ref}" - no such event id'))

        # who shape (advisory)
        who = ev.get("who")
        if who is not None and not isinstance(who, list):
            findings.append(Finding(WARN, "Field shape",
                                    f"{where} `who` should be a list of names"))

    if not events:
        findings.append(Finding(INFO, "Empty timeline",
                                "no events recorded yet - the log will grow append-only"))
    if not any(f.severity in (ERROR, BREACH, WARN) for f in findings):
        findings.append(Finding(OK, "Structure",
                                f"{len(events)} event(s), ids unique, fields present"))
    return findings


# --- append-only integrity (git) -------------------------------------------


def _git(repo: Path, *args: str) -> tuple[int, str, str]:
    """Run a git command under `repo`; return (returncode, stdout, stderr).

    Decode git's output as UTF-8 explicitly: `text=True` alone would use the
    platform default (cp1252 on Windows), which mangles any non-ASCII event text
    and makes a sealed event falsely compare as modified against the UTF-8
    working copy.
    """
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


def check_append_only(timeline_path: Path, repo: Path,
                      working_events: list[dict]) -> list[Finding]:
    """Compare the working timeline against git HEAD: sealed events must not change.

    Returns BREACH findings for any committed event that was modified or deleted,
    and an INFO count of appended events. If the file is not tracked yet, or this
    is not a git repo, the check is skipped with INFO (nothing is sealed yet).
    """
    rc, _, _ = _git(repo, "rev-parse", "--is-inside-work-tree")
    if rc != 0:
        return [Finding(INFO, "Append-only",
                        "not a git work tree - sealed-history check skipped")]

    try:
        rel = timeline_path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return [Finding(INFO, "Append-only",
                        "timeline is outside the git repo - sealed-history check skipped")]

    rc, head_text, _ = _git(repo, "show", f"HEAD:{rel}")
    if rc != 0:
        return [Finding(INFO, "Append-only",
                        f"{rel} not in HEAD yet - nothing sealed; this commit "
                        f"seals {len(working_events)} event(s)")]

    try:
        head_events = load_events(head_text)
    except (json.JSONDecodeError, ValueError):
        return [Finding(WARN, "Append-only",
                        "HEAD copy of the timeline is unparseable - cannot diff "
                        "sealed history")]

    head_by_id = {event_key(e): e for e in head_events if isinstance(e, dict)}
    work_by_id = {event_key(e): e for e in working_events if isinstance(e, dict)}

    findings: list[Finding] = []
    for eid, head_ev in head_by_id.items():
        if not eid:
            continue
        if eid not in work_by_id:
            findings.append(Finding(BREACH, "Deleted event",
                                    f'sealed event "{eid}" (ch{head_ev.get("chapter", "?")}) '
                                    f"was removed - append-only forbids deletion; "
                                    f"append a superseding event instead"))
            continue
        if normalise(head_ev) != normalise(work_by_id[eid]):
            changed = _changed_fields(head_ev, work_by_id[eid])
            findings.append(Finding(BREACH, "Modified event",
                                    f'sealed event "{eid}" was edited ({changed}) - '
                                    f"append-only forbids editing a committed event; "
                                    f"append a superseding event instead"))

    appended = [eid for eid in work_by_id if eid and eid not in head_by_id]
    if not findings:
        findings.append(Finding(OK, "Append-only",
                                f"{len(head_by_id)} sealed event(s) intact; "
                                f"{len(appended)} appended since HEAD"))
    return findings


def _changed_fields(old: dict, new: dict) -> str:
    keys = sorted(set(old) | set(new))
    diffs = [k for k in keys if not str(k).startswith("_") and old.get(k) != new.get(k)]
    return "fields: " + ", ".join(diffs) if diffs else "content differs"


# --- views: events + render ------------------------------------------------


def parse_chapter_range(raw: str | None) -> set[int] | None:
    """Parse "8" or "1-6" or "1,3,5" into a set of chapter numbers (None = all)."""
    if not raw:
        return None
    out: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            out.update(range(int(lo), int(hi) + 1))
        elif part:
            out.add(int(part))
    return out or None


def select(events: list[dict], chapters: set[int] | None) -> list[dict]:
    rows = [e for e in events if isinstance(e, dict)
            and (chapters is None or e.get("chapter") in chapters)]
    return sorted(rows, key=lambda e: (e.get("chapter") or 0, e.get("seq") or 0))


def render_events_text(rows: list[dict]) -> str:
    if not rows:
        return "(no events for that selection)"
    lines = []
    for e in rows:
        chap = e.get("chapter", "?")
        seq = e.get("seq")
        tag = f"ch{chap:02d}.{seq:02d}" if isinstance(chap, int) and isinstance(seq, int) \
            else f"ch{chap}"
        kind = e.get("kind")
        kindstr = f"({kind}) " if kind else ""
        meta = []
        if e.get("who"):
            meta.append("who: " + ", ".join(str(w) for w in e["who"]))
        if e.get("where"):
            meta.append("@ " + str(e["where"]))
        if e.get("when"):
            meta.append("when: " + str(e["when"]))
        metastr = ("  {" + "; ".join(meta) + "}") if meta else ""
        lines.append(f"[{tag}] [{e.get('id', '?')}] {kindstr}{e.get('event', '')}{metastr}")
    return "\n".join(lines)


def render_markdown(rows: list[dict]) -> str:
    if not rows:
        return "_(no events)_"
    out: list[str] = []
    current = object()
    for e in rows:
        chap = e.get("chapter", "?")
        if chap != current:
            out.append(f"\n## Chapter {chap}\n")
            current = chap
        bits = [str(e.get("event", "")).rstrip(".")]
        tail = []
        if e.get("who"):
            tail.append(", ".join(str(w) for w in e["who"]))
        if e.get("where"):
            tail.append("@ " + str(e["where"]))
        if e.get("when"):
            tail.append(str(e["when"]))
        suffix = f" — {' · '.join(tail)}" if tail else ""
        out.append(f"- **[{e.get('id', '?')}]** {bits[0]}.{suffix}")
    return "\n".join(out).lstrip("\n")


# --- report + exit ---------------------------------------------------------


def render_report(command: str, findings: list[Finding]) -> str:
    head = f"timeline {command}"
    lines = [head, "=" * len(head), ""]
    width = max((len(f.check) for f in findings), default=0)
    for f in findings:
        lines.append(f"[{f.severity}]  {f.check.ljust(width)}  {f.detail}")
    lines.append("")

    breaches = sum(1 for f in findings if f.severity == BREACH)
    errors = sum(1 for f in findings if f.severity == ERROR)
    warns = sum(1 for f in findings if f.severity == WARN)
    if breaches:
        lines.append(f"RESULT: BREACH - {breaches} sealed event(s) edited or deleted. "
                     f"The timeline is APPEND-ONLY: revert the change and append a "
                     f"superseding event instead.")
    elif errors:
        lines.append(f"RESULT: INVALID - {errors} structural error(s). Fix the store "
                     f"before relying on it for continuity.")
    elif warns:
        lines.append(f"RESULT: PASS with {warns} warning(s). Note them; the log is usable.")
    else:
        lines.append("RESULT: PASS. The timeline is well-formed and sealed history is intact.")
    return "\n".join(lines)


def exit_code(findings: list[Finding], fail_on: str) -> int:
    worst = max((_RANK[f.severity] for f in findings), default=0)
    if fail_on == "never":
        return 0
    if fail_on == "warn":
        return 3 if worst >= _RANK[WARN] else 0
    return 3 if worst >= _RANK[ERROR] else 0  # fail_on == "error" (default)


# --- main ------------------------------------------------------------------


def _resolve_timeline(args_timeline: str | None, base: Path | None,
                      repo: Path, paths: dict) -> Path:
    if args_timeline:
        return Path(args_timeline)
    rel = paths.get("timeline")
    if rel and base is not None:
        return base / rel
    return repo / DEFAULT_TIMELINE_NAME


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Append-only continuity timeline: validate, integrity-check, view.")
    parser.add_argument("command", choices=("check", "validate", "events", "render"),
                        help="check = validate + append-only gate; validate = structure "
                             "only; events/render = view recorded events")
    parser.add_argument("--timeline", default=None,
                        help="path to the timeline store "
                             "(default: kit.config.json paths.timeline, else <repo>/timeline.json)")
    parser.add_argument("--repo", type=Path, default=None,
                        help="repo root for the git append-only check "
                             "(default: kit.config.json dir, else CWD)")
    parser.add_argument("--chapter", default=None,
                        help='chapter selector for events/render: "8", "1-6", or "1,3,5"')
    parser.add_argument("--format", choices=("text", "json", "md"), default="text",
                        help="output format for events/render")
    parser.add_argument("--fail-on", choices=("error", "warn", "never"), default="error",
                        help="exit non-zero threshold for check/validate (default: error)")
    args = parser.parse_args()

    binding, base = load_binding()
    paths = binding.get("paths", {})
    repo = args.repo or base or Path.cwd()
    timeline_path = _resolve_timeline(args.timeline, base, repo, paths)

    # All commands need the parsed events.
    if not timeline_path.exists():
        if args.command in ("check", "validate"):
            print(render_report(args.command, [Finding(
                ERROR, "Timeline file",
                f"not found: {timeline_path} - create it or pass --timeline")]))
            sys.exit(exit_code([Finding(ERROR, "x", "x")], args.fail_on))
        print(f"(timeline not found: {timeline_path})")
        sys.exit(0)

    try:
        events = load_events(timeline_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        if args.command in ("check", "validate"):
            print(render_report(args.command, [Finding(
                ERROR, "Parse", f"{timeline_path.name}: {exc}")]))
            sys.exit(exit_code([Finding(ERROR, "x", "x")], args.fail_on))
        print(f"(timeline unparseable: {exc})")
        sys.exit(2)

    if args.command in ("events", "render"):
        rows = select(events, parse_chapter_range(args.chapter))
        if args.format == "json":
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        elif args.format == "md" or args.command == "render":
            print(render_markdown(rows))
        else:
            print(render_events_text(rows))
        sys.exit(0)

    # check / validate
    findings = validate_events(events)
    if args.command == "check":
        findings = [f for f in findings if f.severity != OK]  # keep OK only once, below
        findings.extend(check_append_only(timeline_path, repo, events))
        if not any(f.severity in (BREACH, ERROR, WARN) for f in findings):
            findings.append(Finding(OK, "Timeline",
                                    f"{len(events)} event(s) valid and sealed history intact"))
    print(render_report(args.command, findings))
    sys.exit(exit_code(findings, args.fail_on))


if __name__ == "__main__":
    main()
