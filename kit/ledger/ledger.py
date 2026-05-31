#!/usr/bin/env python3
"""ledger - promise/payoff continuity ledger (the "Mercy Engine").

Zero LLM tokens. A setup->payoff tracker that generalizes a revelation
schedule into EVERY kind of planted promise:

    foreshadow / chekhov / mercy / debt / threat / question / vow / reveal

Every planted promise gets a payoff slot. Once paid, it carries the chapter it
paid off in. The whole point is the unpaid sweep: a planted promise that the
story never honors - a Chekhov's gun that never fires, a mercy that never
returns, a mystery posed and forgotten - is a continuity hole. This tool keeps
the ledger honest and SURFACES the open (planted-but-unpaid) threads; the
SEMANTIC judgement - does THIS draft pay off THIS promise? - stays agent-side
(editors-hat Pass 2), exactly as preflight leaves the outline-beats check
agent-side and timeline leaves the continuity diff agent-side.

Unlike the timeline (append-only, sealed), the ledger is MUTABLE STATE: a
promise's status legitimately changes over its life (open -> paid). It is the
revelation-schedule.json analog, not the timeline.json analog - so there is no
git seal here. A thread that is silently dropped shows up as perpetually `open`;
that is the report, not a breach.

This tool does the deterministic half of promise tracking:
  * validate   - the store is well-formed (unique ids, required fields, sane
                 chapter numbers, known statuses)
  * check      - validate + flag OVERDUE open threads (planted, past their
                 due-by chapter, still unpaid) when a frontier chapter is given
  * open       - print the open (planted-but-unpaid) promises - the actionable
                 surface the editor diffs a draft against
  * render     - human-readable markdown of the whole ledger, grouped by status

STANDARDS-LAYER TOOL: it knows nothing of any specific novel. The Novel layer
binds it to its own files via a repo-root kit.config.json that this tool
DISCOVERS (walking up from CWD, then the script dir). Resolution order for the
ledger path is: explicit --promises flag > kit.config.json paths.promises >
portable built-in default (<repo>/promises.json).

Usage:
    python kit/ledger/ledger.py check --through 8
    python kit/ledger/ledger.py validate
    python kit/ledger/ledger.py open --through 8
    python kit/ledger/ledger.py open --through 8 --overdue
    python kit/ledger/ledger.py open --format json
    python kit/ledger/ledger.py render --kind mercy

Exit codes are governed by --fail-on (default: error -> non-zero only on a
structural ERROR). Overdue threads are WARN: advisory, never a hard block - a
7-book series legitimately holds a promise open across volumes; the editor
decides whether an overdue thread is a real drop.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BINDING_FILENAME = "kit.config.json"
DEFAULT_PROMISES_NAME = "promises.json"

# Severity tags (fixed width so the report columns line up).
ERROR = "ERROR "  # the store is structurally invalid (bad json, dup id, missing field, bad status)
WARN = "WARN  "   # a soft issue (overdue open thread, unknown kind, paid-without-chapter)
INFO = "INFO  "   # advisory (open/paid counts, frontier-unknown note)
OK = "  OK  "     # checked and clean

_RANK = {ERROR: 3, WARN: 2, INFO: 1, OK: 0}

# `kind` is a free taxonomy; these are the recognised values (others -> WARN, not blocked).
KNOWN_KINDS = {
    "foreshadow", "chekhov", "mercy", "debt", "threat", "question", "vow", "reveal",
}

# `status` drives the open/paid logic, so an unknown value is a hard ERROR.
KNOWN_STATUSES = {"open", "paid", "abandoned", "subverted"}
CLOSED_STATUSES = {"paid", "abandoned", "subverted"}

REQUIRED_FIELDS = ("id", "kind", "promise", "planted_chapter", "status")


class Finding:
    """One ledger-check result line."""

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


# --- loading ---------------------------------------------------------------


def load_promises(text: str) -> list[dict]:
    """Parse a ledger document's text into its promises list (raises on bad json)."""
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("ledger root must be a JSON object")
    promises = data.get("promises", [])
    if not isinstance(promises, list):
        raise ValueError("ledger `promises` must be a list")
    return promises


def promise_key(p: dict) -> str:
    """The stable identity of a promise (its id)."""
    return str(p.get("id", ""))


def is_open(p: dict) -> bool:
    """A promise is open if its status is not one of the closed states."""
    return str(p.get("status", "")) not in CLOSED_STATUSES


# --- structural validation -------------------------------------------------


def validate_promises(promises: list[dict]) -> list[Finding]:
    findings: list[Finding] = []
    seen_ids: dict[str, int] = {}

    for idx, p in enumerate(promises):
        where = f"promises[{idx}]"
        if not isinstance(p, dict):
            findings.append(Finding(ERROR, "Promise shape", f"{where} is not an object"))
            continue

        # required fields
        for field in REQUIRED_FIELDS:
            if field not in p or p[field] in (None, "", []):
                findings.append(Finding(ERROR, "Required field",
                                        f"{where} missing/empty `{field}`"))

        # id uniqueness
        pid = promise_key(p)
        if pid:
            if pid in seen_ids:
                findings.append(Finding(ERROR, "Duplicate id",
                                        f'id "{pid}" reused ({where} and '
                                        f"promises[{seen_ids[pid]}])"))
            else:
                seen_ids[pid] = idx

        # status taxonomy (load-bearing -> ERROR on unknown)
        status = p.get("status")
        if status is not None and status not in KNOWN_STATUSES:
            findings.append(Finding(ERROR, "Unknown status",
                                    f'{where} status "{status}" not in '
                                    f"({', '.join(sorted(KNOWN_STATUSES))})"))

        # kind taxonomy (advisory -> WARN)
        kind = p.get("kind")
        if kind is not None and kind not in KNOWN_KINDS:
            findings.append(Finding(WARN, "Unknown kind",
                                    f'{where} kind "{kind}" not in the known set '
                                    f"({', '.join(sorted(KNOWN_KINDS))})"))

        # planted_chapter type
        planted = p.get("planted_chapter")
        if planted is not None and (not isinstance(planted, int) or planted < 1):
            findings.append(Finding(ERROR, "Planted chapter",
                                    f"{where} planted_chapter must be an int >= 1 "
                                    f"(got {planted!r})"))

        # due_by_chapter sanity
        due = p.get("due_by_chapter")
        if due is not None:
            if not isinstance(due, int) or due < 1:
                findings.append(Finding(WARN, "Due-by value",
                                        f"{where} due_by_chapter should be an int >= 1 "
                                        f"(got {due!r})"))
            elif isinstance(planted, int) and due < planted:
                findings.append(Finding(WARN, "Due-by order",
                                        f"{where} due_by_chapter {due} is before "
                                        f"planted_chapter {planted}"))

        # paid promises must record a paid_chapter; open ones must not
        paid_ch = p.get("paid_chapter")
        if status == "paid":
            if paid_ch in (None, "", []):
                findings.append(Finding(WARN, "Paid w/o chapter",
                                        f'{where} status "paid" but no paid_chapter recorded'))
            elif isinstance(paid_ch, int) and isinstance(planted, int) and paid_ch < planted:
                findings.append(Finding(WARN, "Paid before planted",
                                        f"{where} paid_chapter {paid_ch} is before "
                                        f"planted_chapter {planted}"))
        elif is_open(p) and paid_ch not in (None, "", []):
            findings.append(Finding(WARN, "Open w/ paid chapter",
                                    f"{where} is open but carries paid_chapter "
                                    f"{paid_ch!r} - mark it paid or clear the field"))

        # list-shaped fields (advisory)
        for listfield in ("reinforced_chapters", "who"):
            val = p.get(listfield)
            if val is not None and not isinstance(val, list):
                findings.append(Finding(WARN, "Field shape",
                                        f"{where} `{listfield}` should be a list"))

    if not promises:
        findings.append(Finding(INFO, "Empty ledger",
                                "no promises recorded yet - plant some as the book grows"))
    if not any(f.severity in (ERROR, WARN) for f in findings):
        findings.append(Finding(OK, "Structure",
                                f"{len(promises)} promise(s), ids unique, fields present"))
    return findings


# --- frontier + overdue ----------------------------------------------------


def overdue_promises(promises: list[dict], frontier: int) -> list[dict]:
    """Open promises whose due_by_chapter has been reached but are still unpaid.

    `frontier` is the latest chapter the story has reached (the caller passes the
    chapter under edit). A promise is overdue when it is open, has a due_by, and
    that due_by is <= frontier. Without a frontier this cannot be computed - the
    ledger legitimately holds future-targeted promises, so an inferred frontier
    would be wrong (hint/reveal chapters are future, not written).
    """
    out = []
    for p in promises:
        if not isinstance(p, dict) or not is_open(p):
            continue
        due = p.get("due_by_chapter")
        if isinstance(due, int) and due <= frontier:
            out.append(p)
    return sorted(out, key=lambda p: (p.get("due_by_chapter") or 0,
                                      p.get("planted_chapter") or 0))


def check_overdue(promises: list[dict], frontier: int | None) -> list[Finding]:
    findings: list[Finding] = []
    open_count = sum(1 for p in promises if isinstance(p, dict) and is_open(p))
    paid_count = sum(1 for p in promises if isinstance(p, dict)
                     and p.get("status") == "paid")

    if frontier is None:
        findings.append(Finding(INFO, "Overdue sweep",
                                "pass --through N (the latest drafted chapter) to flag "
                                "overdue open threads"))
        findings.append(Finding(INFO, "Open threads",
                                f"{open_count} open, {paid_count} paid "
                                f"(of {len(promises)} total)"))
        return findings

    overdue = overdue_promises(promises, frontier)
    for p in overdue:
        findings.append(Finding(WARN, "Overdue thread",
                                f'[{promise_key(p)}] ({p.get("kind", "?")}) due by '
                                f'ch{p.get("due_by_chapter")} still open at ch{frontier}: '
                                f'{p.get("promise", "")}'))
    if not overdue:
        findings.append(Finding(OK, "Overdue sweep",
                                f"no overdue threads through ch{frontier} "
                                f"({open_count} open, {paid_count} paid)"))
    return findings


# --- views: open + render --------------------------------------------------


def select_open(promises: list[dict], through: int | None,
                overdue_only: bool, frontier: int | None) -> list[dict]:
    rows = [p for p in promises if isinstance(p, dict) and is_open(p)]
    if through is not None:
        rows = [p for p in rows if isinstance(p.get("planted_chapter"), int)
                and p["planted_chapter"] <= through]
    if overdue_only and frontier is not None:
        rows = [p for p in rows if isinstance(p.get("due_by_chapter"), int)
                and p["due_by_chapter"] <= frontier]
    return sorted(rows, key=lambda p: (p.get("due_by_chapter") or 10 ** 6,
                                       p.get("planted_chapter") or 0,
                                       promise_key(p)))


def _meta_bits(p: dict) -> list[str]:
    meta = []
    if p.get("who"):
        meta.append("who: " + ", ".join(str(w) for w in p["who"]))
    if p.get("reinforced_chapters"):
        meta.append("reinforced: " + ", ".join(str(c) for c in p["reinforced_chapters"]))
    return meta


def render_open_text(rows: list[dict]) -> str:
    if not rows:
        return "(no open promises for that selection)"
    lines = []
    for p in rows:
        planted = p.get("planted_chapter", "?")
        due = p.get("due_by_chapter")
        span = f"ch{planted:02d}->{due}" if isinstance(planted, int) and due else \
            (f"ch{planted:02d}" if isinstance(planted, int) else f"ch{planted}")
        kind = p.get("kind")
        kindstr = f"({kind}) " if kind else ""
        meta = _meta_bits(p)
        metastr = ("  {" + "; ".join(meta) + "}") if meta else ""
        lines.append(f"[{span}] [{promise_key(p)}] {kindstr}{p.get('promise', '')}{metastr}")
    return "\n".join(lines)


def render_markdown(promises: list[dict], kind_filter: str | None) -> str:
    rows = [p for p in promises if isinstance(p, dict)
            and (kind_filter is None or p.get("kind") == kind_filter)]
    if not rows:
        return "_(no promises)_"
    order = ["open", "paid", "subverted", "abandoned"]
    out: list[str] = []
    for status in order:
        group = sorted([p for p in rows if p.get("status") == status],
                       key=lambda p: (p.get("planted_chapter") or 0, promise_key(p)))
        if not group:
            continue
        out.append(f"\n## {status.capitalize()} ({len(group)})\n")
        for p in group:
            planted = p.get("planted_chapter", "?")
            due = p.get("due_by_chapter")
            paid = p.get("paid_chapter")
            tail = []
            if due and status == "open":
                tail.append(f"due ch{due}")
            if paid and status == "paid":
                tail.append(f"paid ch{paid}")
            if p.get("who"):
                tail.append(", ".join(str(w) for w in p["who"]))
            suffix = f" — {' · '.join(tail)}" if tail else ""
            kind = p.get("kind", "?")
            out.append(f"- **[{promise_key(p)}]** ({kind}, planted ch{planted}) "
                       f"{str(p.get('promise', '')).rstrip('.')}.{suffix}")
    # any status outside the known order (shouldn't happen post-validate)
    leftover = [p for p in rows if p.get("status") not in order]
    if leftover:
        out.append(f"\n## Other ({len(leftover)})\n")
        for p in leftover:
            out.append(f"- **[{promise_key(p)}]** ({p.get('status')!r}) "
                       f"{p.get('promise', '')}")
    return "\n".join(out).lstrip("\n")


# --- report + exit ---------------------------------------------------------


def render_report(command: str, findings: list[Finding]) -> str:
    head = f"ledger {command}"
    lines = [head, "=" * len(head), ""]
    width = max((len(f.check) for f in findings), default=0)
    for f in findings:
        lines.append(f"[{f.severity}]  {f.check.ljust(width)}  {f.detail}")
    lines.append("")

    errors = sum(1 for f in findings if f.severity == ERROR)
    warns = sum(1 for f in findings if f.severity == WARN)
    if errors:
        lines.append(f"RESULT: INVALID - {errors} structural error(s). Fix the store "
                     f"before relying on it for continuity.")
    elif warns:
        lines.append(f"RESULT: PASS with {warns} warning(s). Note them - an overdue "
                     f"thread is a candidate dropped promise; pay it, reinforce it, or "
                     f"mark it abandoned/subverted deliberately.")
    else:
        lines.append("RESULT: PASS. The ledger is well-formed; no overdue threads.")
    return "\n".join(lines)


def exit_code(findings: list[Finding], fail_on: str) -> int:
    worst = max((_RANK[f.severity] for f in findings), default=0)
    if fail_on == "never":
        return 0
    if fail_on == "warn":
        return 3 if worst >= _RANK[WARN] else 0
    return 3 if worst >= _RANK[ERROR] else 0  # fail_on == "error" (default)


# --- main ------------------------------------------------------------------


def _resolve_promises(args_promises: str | None, base: Path | None,
                      repo: Path, paths: dict) -> Path:
    if args_promises:
        return Path(args_promises)
    rel = paths.get("promises")
    if rel and base is not None:
        return base / rel
    return repo / DEFAULT_PROMISES_NAME


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promise/payoff ledger: validate, overdue-check, surface open threads.")
    parser.add_argument("command", choices=("check", "validate", "open", "render"),
                        help="check = validate + overdue sweep; validate = structure only; "
                             "open = list planted-but-unpaid threads; render = markdown")
    parser.add_argument("--promises", default=None,
                        help="path to the ledger store "
                             "(default: kit.config.json paths.promises, else <repo>/promises.json)")
    parser.add_argument("--through", type=int, default=None,
                        help="frontier chapter (latest drafted): flags overdue threads for "
                             "check, filters open by planted<=N")
    parser.add_argument("--overdue", action="store_true",
                        help="for `open`: show only overdue threads (needs --through)")
    parser.add_argument("--kind", default=None,
                        help="for `render`: filter to one kind "
                             f"({', '.join(sorted(KNOWN_KINDS))})")
    parser.add_argument("--format", choices=("text", "json", "md"), default="text",
                        help="output format for open/render")
    parser.add_argument("--fail-on", choices=("error", "warn", "never"), default="error",
                        help="exit non-zero threshold for check/validate (default: error)")
    args = parser.parse_args()

    binding, base = load_binding()
    paths = binding.get("paths", {})
    repo = base or Path.cwd()
    promises_path = _resolve_promises(args.promises, base, repo, paths)

    if not promises_path.exists():
        if args.command in ("check", "validate"):
            print(render_report(args.command, [Finding(
                ERROR, "Ledger file",
                f"not found: {promises_path} - create it or pass --promises")]))
            sys.exit(exit_code([Finding(ERROR, "x", "x")], args.fail_on))
        print(f"(ledger not found: {promises_path})")
        sys.exit(0)

    try:
        promises = load_promises(promises_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        if args.command in ("check", "validate"):
            print(render_report(args.command, [Finding(
                ERROR, "Parse", f"{promises_path.name}: {exc}")]))
            sys.exit(exit_code([Finding(ERROR, "x", "x")], args.fail_on))
        print(f"(ledger unparseable: {exc})")
        sys.exit(2)

    if args.command == "open":
        rows = select_open(promises, args.through, args.overdue, args.through)
        if args.format == "json":
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        elif args.format == "md":
            # markdown of just the open subset, reusing the grouped renderer
            print(render_markdown(rows, None))
        else:
            print(render_open_text(rows))
        sys.exit(0)

    if args.command == "render":
        if args.format == "json":
            rows = [p for p in promises if isinstance(p, dict)
                    and (args.kind is None or p.get("kind") == args.kind)]
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            print(render_markdown(promises, args.kind))
        sys.exit(0)

    # check / validate
    findings = validate_promises(promises)
    if args.command == "check":
        findings = [f for f in findings if f.severity != OK]
        findings.extend(check_overdue(promises, args.through))
        if not any(f.severity in (ERROR, WARN) for f in findings):
            findings.append(Finding(OK, "Ledger",
                                    f"{len(promises)} promise(s) valid; no overdue threads"))
    print(render_report(args.command, findings))
    sys.exit(exit_code(findings, args.fail_on))


if __name__ == "__main__":
    main()
