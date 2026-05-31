#!/usr/bin/env python3
"""PostToolUse hook: advisory prose-lint on forge-novel chapter drafts.

Claude Code delivers the tool call as JSON on stdin. This wrapper extracts the
edited file path and, if it is a chapter draft, prints the prose_lint report
into the transcript so the model sees its own slop immediately after a Write or
Edit. It is purely advisory — it always exits 0 and never blocks an edit.

prose_lint applies its own chapter-draft path guard, so edits to any other file
produce no output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prose_lint import main as lint_main


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if data.get("tool_name") not in ("Write", "Edit"):
        return 0
    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0
    lint_main([file_path, "--format", "text", "--fail-on", "never"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
