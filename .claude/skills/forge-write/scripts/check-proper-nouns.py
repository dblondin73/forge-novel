#!/usr/bin/env python3
"""PreToolUse hook: flag unmarked proper nouns in forge-novel drafts.

Receives Claude Code tool call JSON on stdin. Inspects Write/Edit calls
targeting forge-novel draft files. Extracts proper noun candidates and
warns about any that are:
  - Not in the known-entities cache
  - Not wrapped in [INVENTED:] markers

Returns a soft warning (permissionDecision: "allow" + additionalContext)
so the write still proceeds but Claude sees the flag.

Source: Phase 4 of the forge-write skill build plan.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".forge-known-entities.json"

# Patterns that identify a forge-novel draft file
DRAFT_PATH_PATTERNS = [
    r"forge-novel[/\\]drafts[/\\].*\.md$",
    r"forge-novel[/\\]ch\d+.*\.md$",
]

# Common English words that appear capitalized (sentence start, titles, etc.)
# These are NOT proper nouns in the forge-novel context
COMMON_CAPS = {
    # Sentence-start artifacts
    "The",
    "A",
    "An",
    "He",
    "She",
    "It",
    "They",
    "We",
    "His",
    "Her",
    "Its",
    "Their",
    "Our",
    "My",
    "Your",
    "This",
    "That",
    "These",
    "Those",
    "But",
    "And",
    "Or",
    "So",
    "Yet",
    "For",
    "Nor",
    "If",
    "When",
    "While",
    "As",
    "In",
    "On",
    "At",
    "To",
    "From",
    "With",
    "By",
    "Of",
    "Up",
    "Out",
    "Into",
    "Then",
    "Now",
    "Here",
    "There",
    "Where",
    "What",
    "Who",
    "How",
    "Why",
    "Not",
    "No",
    "Yes",
    "All",
    "Each",
    "Every",
    "Some",
    "Any",
    "Much",
    "Many",
    "Most",
    "More",
    "Less",
    "Just",
    "Only",
    "Even",
    "Still",
    "Also",
    "Too",
    "Very",
    "Back",
    "Down",
    "Over",
    "After",
    "Before",
    "About",
    "Around",
    "Through",
    "Between",
    "Under",
    "Again",
    "Once",
    "Twice",
    "Never",
    "Always",
    "Maybe",
    "Perhaps",
    "Almost",
    "Already",
    "Enough",
    "Away",
    "Far",
    "Near",
    "Off",
    "Along",
    # Days, months
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    # Common brands / real-world nouns that appear in prose
    "Chevrolet",
    "Ford",
    "Toyota",
    "God",
    "Bible",
    "Jesus",
    "Christ",
    "American",
    "America",
    "English",
    "Iowa",
    "Midwest",
    # Dog breeds (real-world)
    "Border",
    "Collie",
    "Heeler",
    "Australian",
    "Blue",
    # Texas / Earth real-world references
    "Bermudagrass",
    "Carrizo",
    "Wilcox",
    "Henderson",
    "Christmas",
    # Software / hardware brands
    "Commodore",
    "DOS",
    "Windows",
    # Markdown / formatting artifacts
    "INVENTED",
    "TODO",
    "NOTE",
    "WARNING",
    "FIXME",
    # Prose-common verbs/adjectives that start paragraphs
    "Something",
    "Nothing",
    "Everything",
    "Anything",
    "Someone",
    "Nobody",
    "Everyone",
    "Somewhere",
    "Nowhere",
    "Everywhere",
}

# ---------------------------------------------------------------------------
# Entity cache
# ---------------------------------------------------------------------------


def load_entity_cache() -> set[str]:
    """Load known entity names from cache file. Returns empty set if missing."""
    if not CACHE_FILE.exists():
        return set()
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return set(data.get("all_names", []))
    except (json.JSONDecodeError, KeyError):
        return set()


# ---------------------------------------------------------------------------
# Proper noun extraction
# ---------------------------------------------------------------------------

# Matches capitalized words (including hyphenated: "Half-Orc")
PROPER_NOUN_RE = re.compile(r"\b([A-Z][a-z]+(?:[-'][A-Z]?[a-z]+)*)\b")

# Matches [INVENTED: "...", ...] blocks
INVENTED_RE = re.compile(r'\[INVENTED:\s*"([^"]+)"[^\]]*\]')


def extract_proper_nouns(text: str) -> set[str]:
    """Extract capitalized words that are likely proper nouns.

    Filters out:
    - Words at the very start of a sentence (after .!? + space)
    - Words in the COMMON_CAPS set
    - Words inside [INVENTED:] markers
    """
    # First, collect all invented names so we can exclude them
    invented_names: set[str] = set()
    for match in INVENTED_RE.finditer(text):
        # Split multi-word names into individual words too
        full_name = match.group(1)
        invented_names.add(full_name)
        for word in full_name.split():
            invented_names.add(word)

    # Find all capitalized words
    candidates: set[str] = set()
    for match in PROPER_NOUN_RE.finditer(text):
        word = match.group(1)
        pos = match.start()

        # Skip common caps
        if word in COMMON_CAPS:
            continue

        # Skip words in [INVENTED:] markers
        if word in invented_names:
            continue

        # Skip sentence-start words (preceded by .!?\n + optional whitespace)
        if pos > 0:
            before = text[max(0, pos - 3) : pos]
            # Check if this word starts a sentence or paragraph
            if re.search(r"[.!?\n]\s*$", before):
                # Still keep it if it's a known proper noun pattern
                # (multi-caps like "Nate" appearing mid-paragraph elsewhere)
                # For now, skip — we'll catch it if it appears mid-sentence too
                continue
        elif pos == 0:
            continue

        candidates.add(word)

    return candidates


def find_multi_word_names(text: str, invented_names: set[str], known: set[str]) -> set[str]:
    """Find multi-word capitalized sequences (e.g., 'Marcus Webb').

    Skips phrases where every word individually qualifies as known
    (in COMMON_CAPS, in the entity cache, or in invented names) —
    this catches sentence-starters glued to character names like
    "Where Rex" or "When Nate".
    """
    pattern = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b")
    names: set[str] = set()
    for match in pattern.finditer(text):
        full = match.group(1)
        words = full.split()
        if all(w in COMMON_CAPS or w in known or w in invented_names for w in words):
            continue
        if full in invented_names:
            continue
        names.add(full)
    return names


# ---------------------------------------------------------------------------
# Main hook logic
# ---------------------------------------------------------------------------


def main() -> None:
    # Read tool call JSON from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Can't parse input — pass through silently
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only inspect Write and Edit
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    # Only inspect forge-novel draft files
    is_draft = any(re.search(pattern, file_path, re.IGNORECASE) for pattern in DRAFT_PATH_PATTERNS)
    if not is_draft:
        sys.exit(0)

    # Extract text content to inspect
    if tool_name == "Write":
        text = tool_input.get("content", "")
    else:  # Edit
        text = tool_input.get("new_string", "")

    if not text or len(text) < 20:
        sys.exit(0)

    # Load known entities
    known = load_entity_cache()

    # Collect invented names from the text
    invented_names: set[str] = set()
    for match in INVENTED_RE.finditer(text):
        full_name = match.group(1)
        invented_names.add(full_name)
        for word in full_name.split():
            invented_names.add(word)

    # Extract proper noun candidates
    single_nouns = extract_proper_nouns(text)
    multi_nouns = find_multi_word_names(text, invented_names, known)

    # Filter against known entities
    unknown_singles = {n for n in single_nouns if n not in known}
    unknown_multis = {
        n
        for n in multi_nouns
        if n not in known and not any(n in inv or inv in n for inv in invented_names)
    }

    unknowns = unknown_singles | unknown_multis

    if not unknowns:
        # All clear — pass through
        sys.exit(0)

    # Build soft warning
    noun_list = ", ".join(sorted(unknowns)[:15])
    if len(unknowns) > 15:
        noun_list += f" (+{len(unknowns) - 15} more)"

    warning = (
        f"[forge-write hook] {len(unknowns)} proper noun(s) not in Codex cache "
        f"and not marked [INVENTED:]: {noun_list}. "
        'Add [INVENTED: "name", category] markers for new entities, '
        "or run `python scripts/refresh-entity-cache.py` to update the cache."
    )

    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": warning,
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
