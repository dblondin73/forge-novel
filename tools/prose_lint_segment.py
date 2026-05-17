"""Markdown-aware segmentation for the forge-novel prose linter.

Chapter drafts keep each paragraph on a single physical line, separated by
blank lines. This module classifies every line so the detectors only ever
see narrative prose — never System panels, headers, scene-break rules, or
fenced code blocks. One ``Line`` therefore corresponds to one paragraph.

Stdlib only. No third-party dependencies.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# --- line classification --------------------------------------------------

PROSE = "prose"
HEADER = "header"
HRULE = "hrule"
CODE_FENCE = "code_fence"
BLOCKQUOTE = "blockquote"
PANEL = "panel"
BLANK = "blank"

_HEADER_RE = re.compile(r"^#{1,6}\s")
_HRULE_RE = re.compile(r"^-{3,}\s*$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_BLOCKQUOTE_RE = re.compile(r"^\s*>")
# A bracket/keyword test for whole-line italic spans that read like System text.
_SYSTEM_WORD_RE = re.compile(
    r"\[|ERROR|SYSTEM|PROCESSING|WARNING|ALERT|QUEST|NOTICE|LEVEL|SKILL|GRANTED"
)


@dataclass
class Line:
    """One classified physical line (== one paragraph in chapter drafts)."""

    lineno: int
    text: str
    kind: str

    @property
    def in_prose(self) -> bool:
        return self.kind == PROSE


def _is_bold_panel(stripped: str) -> bool:
    """True when the whole line is a single bold span — a System panel/label.

    Narrative prose never wraps an entire paragraph in bold; inline ``**System**``
    proper nouns leave four-plus ``**`` markers on the line, so they stay prose.
    """
    if not (stripped.startswith("**") and stripped.endswith("**")):
        return False
    return stripped.count("**") == 2 and len(stripped) > 4


def _is_italic_panel(stripped: str) -> bool:
    """True for a whole-line italic span that reads like a System message.

    A whole paragraph of italic direct-thought is treated as prose; only
    italic lines carrying brackets or a System keyword are skipped.
    """
    if "**" in stripped:
        return False
    if not (stripped.startswith("*") and stripped.endswith("*")):
        return False
    if stripped.count("*") != 2 or len(stripped) <= 2:
        return False
    return bool(_SYSTEM_WORD_RE.search(stripped.strip("*")))


def segment(raw_text: str) -> list[Line]:
    """Classify every physical line of a chapter draft."""
    lines: list[Line] = []
    in_fence = False
    for idx, raw in enumerate(raw_text.splitlines(), start=1):
        stripped = raw.strip()
        if _FENCE_RE.match(raw):
            in_fence = not in_fence
            lines.append(Line(idx, raw, CODE_FENCE))
            continue
        if in_fence:
            lines.append(Line(idx, raw, CODE_FENCE))
        elif not stripped:
            lines.append(Line(idx, raw, BLANK))
        elif _HRULE_RE.match(stripped):
            lines.append(Line(idx, raw, HRULE))
        elif _HEADER_RE.match(stripped):
            lines.append(Line(idx, raw, HEADER))
        elif _BLOCKQUOTE_RE.match(stripped):
            lines.append(Line(idx, raw, BLOCKQUOTE))
        elif _is_bold_panel(stripped) or _is_italic_panel(stripped):
            lines.append(Line(idx, raw, PANEL))
        else:
            lines.append(Line(idx, raw, PROSE))
    return lines


# --- sentence splitting ----------------------------------------------------

# Abbreviations whose trailing period must not end a sentence.
_ABBREV = {
    "mr", "mrs", "ms", "dr", "lt", "sgt", "st", "ft", "vs", "jr", "sr",
    "no", "co", "inc", "etc", "gen", "col", "capt", "rev",
}
_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")
# A run of terminal punctuation, optional closing quote/bracket, then space.
_SENT_SPLIT_RE = re.compile(r"([.!?…]+)([\"'”’)\]]*)(\s+)")


@dataclass
class Sentence:
    """One sentence inside a prose paragraph."""

    lineno: int
    text: str
    words: int


def word_count(text: str) -> int:
    """Count word tokens, ignoring markdown emphasis markers."""
    return len(_WORD_RE.findall(text))


def split_sentences(line: Line) -> list[Sentence]:
    """Split one prose paragraph into sentences.

    Approximate — good enough for length-variation statistics. Guards against
    abbreviations, single-letter initials, and mid-sentence ellipses.
    """
    text = line.text.strip()
    if not text:
        return []
    pieces: list[str] = []
    last = 0
    for m in _SENT_SPLIT_RE.finditer(text):
        before = text[last:m.start(1)].strip().split()
        tail = before[-1].lower().rstrip(".") if before else ""
        if tail in _ABBREV or (len(tail) == 1 and tail.isalpha()):
            continue
        punct = m.group(1)
        rest = text[m.end():]
        if punct in ("...", "…") and rest[:1].islower():
            continue
        pieces.append(text[last:m.end(2)].strip())
        last = m.end()
    tail_text = text[last:].strip()
    if tail_text:
        pieces.append(tail_text)
    return [
        Sentence(line.lineno, p, word_count(p)) for p in pieces if word_count(p)
    ]
