#!/usr/bin/env python3
"""Refresh the known-entities cache from the forge Codex database on nova.

Connects to nova via SSH, queries the forge SQLite database directly,
and writes a flat JSON cache file that check-proper-nouns.py reads
at hook time.

Usage:
    python refresh-entity-cache.py              # Default: SSH to nova
    python refresh-entity-cache.py --db-path /custom/path/forge.db
    python refresh-entity-cache.py --verbose

The cache file (.forge-known-entities.json) is written next to this script.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".forge-known-entities.json"
DEFAULT_DB_PATH = "/mnt/c/Services/forge-mcp/data/forge.db"
NOVA_SSH_HOST = "nova"

# Python snippet that runs on nova via SSH + WSL
REMOTE_SCRIPT = """\
import sqlite3, json
c = sqlite3.connect("{db_path}")
rows = c.execute("SELECT name, type FROM forge_entities ORDER BY type, name").fetchall()
print(json.dumps([dict(name=r[0], type=r[1]) for r in rows]))
"""


def run_remote_query(db_path: str, verbose: bool = False) -> list[dict[str, str]]:
    """SSH to nova, pipe a Python script via stdin, return entity list."""
    script = REMOTE_SCRIPT.format(db_path=db_path)

    # Pipe script through SSH → WSL → python3 via stdin (avoids quoting hell)
    cmd = [
        "ssh",
        NOVA_SSH_HOST,
        "wsl -d Ubuntu -e bash -c 'cat > /tmp/_forge_q.py && python3 /tmp/_forge_q.py'",
    ]
    if verbose:
        print(f"  Piping query script via stdin to {NOVA_SSH_HOST}...")

    result = subprocess.run(
        cmd,
        input=script,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"SSH query failed (exit {result.returncode}):\n"
            f"  stderr: {result.stderr.strip()}\n"
            f'  Check: ssh nova "wsl -d Ubuntu -e sudo systemctl status forge-mcp"'
        )

    # Filter out SSH warnings (post-quantum key exchange, etc.)
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("["):
            return json.loads(line)

    raise RuntimeError(f"No JSON output from remote query. Raw output:\n{result.stdout[:500]}")


def extract_name_tokens(entity_name: str) -> list[str]:
    """Break an entity name into individual searchable tokens.

    "Nathan 'Nate' Hall" → ["Nathan", "Nate", "Hall", "Nathan Hall"]
    "F.L.I.N.T." → ["F.L.I.N.T.", "Flint", "FLINT"]
    "Josie Pickett — The Loot Goblin" → ["Josie", "Pickett", "Josie Pickett", "Loot Goblin"]
    """
    tokens = []

    # Strip em-dash suffixes (descriptive subtitles)
    # "Briarknight — Tutorial Boss" → main = "Briarknight", subtitle = "Tutorial Boss"
    parts = re.split(r"\s*[\u2014\u2013]\s*", entity_name, maxsplit=1)
    main_name = parts[0].strip()
    subtitle = parts[1].strip() if len(parts) > 1 else ""

    # Add the full main name
    tokens.append(main_name)

    # Extract quoted nicknames: "Nate", 'Nate'
    for match in re.finditer(r'["\u201c\u201d\']([\w\s.-]+)["\u201c\u201d\']', main_name):
        tokens.append(match.group(1))

    # Clean name (remove quotes) and split into words
    clean = re.sub(r'["\u201c\u201d\'\u2018\u2019]', "", main_name)
    words = [w for w in clean.split() if len(w) > 1]
    tokens.extend(words)

    # Multi-word combinations (first + last, etc.)
    cap_words = [w for w in words if w[0].isupper()]
    if len(cap_words) >= 2:
        tokens.append(f"{cap_words[0]} {cap_words[-1]}")

    # Handle acronyms like F.L.I.N.T.
    for word in words:
        if re.match(r"^[A-Z](\.[A-Z])+\.?$", word):
            # F.L.I.N.T. → Flint, FLINT
            letters = word.replace(".", "")
            tokens.append(letters)
            tokens.append(letters.capitalize())

    # Add subtitle tokens (capitalized words only)
    if subtitle:
        tokens.append(subtitle)
        for word in subtitle.split():
            if word[0].isupper() and len(word) > 1:
                tokens.append(word)

    return tokens


def build_cache(entities: list[dict[str, str]], verbose: bool = False) -> dict:
    """Build the cache structure from raw entity data."""
    all_names: set[str] = set()
    by_type: dict[str, list[str]] = {}

    for entity in entities:
        name = entity["name"]
        etype = entity["type"]

        by_type.setdefault(etype, []).append(name)

        # Extract all searchable tokens from this entity name
        tokens = extract_name_tokens(name)
        all_names.update(tokens)

        if verbose:
            print(f"  [{etype}] {name} -> {tokens}")

    return {
        "last_refreshed": datetime.now(UTC).isoformat(),
        "source": f"ssh://{NOVA_SSH_HOST} → {DEFAULT_DB_PATH}",
        "entity_count": len(entities),
        "token_count": len(all_names),
        "by_type": {k: sorted(v) for k, v in by_type.items()},
        "all_names": sorted(all_names),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh forge entity cache from Codex DB on nova")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="Path to forge.db on nova WSL")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug info")
    args = parser.parse_args()

    print(f"Querying forge Codex on nova ({NOVA_SSH_HOST})...")

    try:
        entities = run_remote_query(args.db_path, verbose=args.verbose)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"  Found {len(entities)} entities")

    cache = build_cache(entities, verbose=args.verbose)

    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    print(f"Cache written: {CACHE_FILE}")
    print(f"  {cache['token_count']} name tokens from {cache['entity_count']} entities")


if __name__ == "__main__":
    main()
