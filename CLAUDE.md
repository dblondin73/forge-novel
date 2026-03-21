# Forge Novel — Claude Code Build Plan

This file is the master instruction set for Claude Code. Run it from VS Code or the CLI to
build the `git-forge` MCP server on Nova and wire up all clients. Everything in this file
reflects decisions already made — Claude Code should execute, not re-design.

---

## Context & Goals

**What already exists:**
- `forge-novel` repo cloned at `C:\Workbench\dev\forge-novel` (Alienware / Windows)
- Five files committed: `README.md`, `REFERENCE.md`, `SESSIONS.md`, `characters/MC.md`, `CLAUDE.md`
- Nova headless server (ASUS ROG) running WSL2, reachable via Tailscale as `nova` (`100.92.123.31`)
- Existing Forge MCP server on Nova (`forge-mcp.service`, port 8765, FastMCP streamable-HTTP)
- Tailscale Funnel active: `https://nova.taild7cf8c.ts.net/` → `http://127.0.0.1:8765`
- Tailscale CLI runs on **Windows side** of Nova, not inside WSL

**What we are building:**
A dedicated `git-forge` MCP server that:
- Lives on Nova (WSL2), always-on via systemd
- Owns a clone of `dblondin73/forge-novel` on Nova's filesystem
- Exposes read/write/commit/push tools over Streamable HTTP
- Is accessible from Claude Desktop, Claude Code CLI, and Claude.ai web (phone/browser)
- Uses Tailscale Funnel path-based routing alongside forge-mcp (same hostname, different path)
- Port: **8093** (local), exposed at `https://nova.taild7cf8c.ts.net/git-forge`

---

## Phase 1 — Nova: Clone the Repo

SSH into Nova and clone the repo into WSL2.

```bash
ssh nova "wsl -d Ubuntu -e bash -c 'git clone https://github.com/dblondin73/forge-novel.git ~/forge-novel && cd ~/forge-novel && git status'"
```

Verify the five existing files are present: `README.md`, `REFERENCE.md`, `SESSIONS.md`,
`characters/MC.md`, `CLAUDE.md`.

Configure git identity for commits from Nova:

```bash
ssh nova "wsl -d Ubuntu -e bash -c 'cd ~/forge-novel && git config user.email \"dblondin73@gmail.com\" && git config user.name \"David Blondin\"'"
```

For push access, Nova needs a GitHub PAT stored in the credential helper:

```bash
ssh nova "wsl -d Ubuntu -e bash -c 'cd ~/forge-novel && git config credential.helper store'"
# Then do one manual push — enter your GitHub PAT as the password. It caches permanently.
```

> **Manual step:** The PAT entry requires you to type the password once. Everything else
> can be automated.

---

## Phase 2 — Nova: Write the MCP Server

Create the server directory and file on Nova. Source is version-controlled in
`Personal/infra/nova/git_forge/` and deployed via scp/pipe.

### File: `~/git-forge-server/server.py`

```python
"""
git-forge MCP Server
Exposes forge-novel repo read/write/git operations over Streamable HTTP.
Port: 8093
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

REPO_PATH = Path.home() / "forge-novel"

mcp = FastMCP(
    name="git-forge",
    instructions="Read, write, and commit files in the forge-novel repository.",
)


def _resolve_safe(path: str) -> Path:
    """Resolve a relative path within the repo. Raises ValueError on traversal."""
    resolved = (REPO_PATH / path).resolve()
    if not resolved.is_relative_to(REPO_PATH.resolve()):
        raise ValueError(f"Path '{path}' escapes repo boundary")
    return resolved


def _git(cmd: list[str]) -> str:
    """Run a git command in the repo and return stdout."""
    result = subprocess.run(
        ["git"] + cmd,
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(cmd)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


# ── File Tools ───────────────────────────────────────────────────────────


@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from the forge-novel repo. Path is relative to repo root."""
    target = _resolve_safe(path)
    if not target.exists():
        raise FileNotFoundError(f"{path} does not exist in forge-novel repo")
    return target.read_text(encoding="utf-8")


@mcp.tool()
def list_files(subdir: str = "") -> str:
    """List files in the forge-novel repo or a subdirectory."""
    target = _resolve_safe(subdir) if subdir else REPO_PATH
    if not target.exists():
        raise FileNotFoundError(f"Directory '{subdir}' not found")
    files = []
    for f in sorted(target.rglob("*")):
        if f.is_file() and ".git" not in f.parts:
            files.append(str(f.relative_to(REPO_PATH)))
    return "\n".join(files) if files else "(no files found)"


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write or overwrite a file in the forge-novel repo. Path relative to repo root."""
    target = _resolve_safe(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Written: {path} ({len(content)} chars)"


@mcp.tool()
def append_file(path: str, content: str) -> str:
    """Append content to an existing file in the forge-novel repo."""
    target = _resolve_safe(path)
    if not target.exists():
        raise FileNotFoundError(f"{path} does not exist — use write_file to create it")
    existing = target.read_text(encoding="utf-8")
    target.write_text(existing + "\n" + content, encoding="utf-8")
    return f"Appended {len(content)} chars to {path}"


@mcp.tool()
def delete_file(path: str) -> str:
    """Delete a file from the forge-novel repo. Path relative to repo root."""
    target = _resolve_safe(path)
    if not target.exists():
        raise FileNotFoundError(f"{path} does not exist")
    target.unlink()
    return f"Deleted: {path}"


@mcp.tool()
def search_repo(query: str, file_pattern: str = "*.md") -> str:
    """Search repo files for a text string. Returns file:line matches.

    Args:
        query: Text to search for (case-insensitive)
        file_pattern: Glob pattern for files to search (default: *.md)
    """
    results = []
    for f in sorted(REPO_PATH.rglob(file_pattern)):
        if ".git" in f.parts:
            continue
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines, 1):
                if query.lower() in line.lower():
                    rel = f.relative_to(REPO_PATH)
                    results.append(f"{rel}:{i}: {line.strip()}")
        except Exception:
            pass
    return "\n".join(results) if results else f"No matches for '{query}'"


# ── Git Tools ────────────────────────────────────────────────────────────


@mcp.tool()
def git_status() -> str:
    """Show working tree status."""
    return _git(["status", "--short"]) or "(clean)"


@mcp.tool()
def git_log(n: int = 10) -> str:
    """Show last n commit messages with dates."""
    return _git(["log", f"-{n}", "--oneline", "--decorate"])


@mcp.tool()
def git_diff(staged: bool = False) -> str:
    """Show uncommitted changes. Set staged=True for staged-only diff."""
    cmd = ["diff", "--staged"] if staged else ["diff"]
    return _git(cmd) or "(no changes)"


@mcp.tool()
def git_pull() -> str:
    """Pull latest changes from GitHub (origin main)."""
    return _git(["pull", "origin", "main"])


@mcp.tool()
def git_commit(message: str, paths: Optional[list[str]] = None) -> str:
    """Stage specific files and commit. Paths are required — no implicit add-all.

    Args:
        message: Commit message
        paths: List of file paths to stage (relative to repo root). Required.
    """
    if not paths:
        raise ValueError("paths is required — specify which files to commit")
    # Validate all paths are within repo
    for p in paths:
        _resolve_safe(p)
    _git(["add"] + paths)
    try:
        result = _git(["commit", "-m", message])
        return result
    except RuntimeError as e:
        if "nothing to commit" in str(e):
            return "Nothing to commit — working tree clean."
        raise


@mcp.tool()
def git_push() -> str:
    """Push committed changes to GitHub (origin main)."""
    return _git(["push", "origin", "main"])


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8093)
```

Deploy to Nova:

```bash
ssh nova "wsl -d Ubuntu -e mkdir -p ~/git-forge-server"
cat server.py | ssh nova "wsl -d Ubuntu -e bash -c 'cat > ~/git-forge-server/server.py'"
```

---

## Phase 3 — Nova: Install Dependencies

FastMCP is already installed on Nova (used by forge-mcp). Verify:

```bash
ssh nova "wsl -d Ubuntu -e python3 -c 'import fastmcp; print(fastmcp.__version__)'"
```

If missing:

```bash
ssh nova "wsl -d Ubuntu -e pip install fastmcp --break-system-packages"
```

---

## Phase 4 — Nova: Create systemd Service

Create the systemd unit file so the server survives reboots.

```bash
ssh nova "wsl -d Ubuntu -e sudo tee /etc/systemd/system/git-forge-mcp.service" << 'EOF'
[Unit]
Description=git-forge MCP Server (forge-novel repo)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=david
WorkingDirectory=/home/david/git-forge-server
ExecStart=/usr/bin/python3 /home/david/git-forge-server/server.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF
```

Enable and start:

```bash
ssh nova "wsl -d Ubuntu -e bash -c 'sudo systemctl daemon-reload && sudo systemctl enable git-forge-mcp && sudo systemctl start git-forge-mcp'"
```

Verify it's running:

```bash
ssh nova "wsl -d Ubuntu -e sudo systemctl status git-forge-mcp --no-pager"
```

---

## Phase 5 — Nova: Expose via Tailscale Funnel

Tailscale runs on the **Windows side** of Nova. Use path-based routing to coexist with
the existing forge-mcp server.

Current state:
- `https://nova.taild7cf8c.ts.net/` → `http://127.0.0.1:8765` (forge-mcp)

Add the git-forge path:

```bash
ssh nova "tailscale serve --bg --set-path /git-forge http://127.0.0.1:8093"
```

Verify both routes:

```bash
ssh nova "tailscale serve status"
```

Expected output:
```
https://nova.taild7cf8c.ts.net (Funnel on)
|-- /           proxy http://127.0.0.1:8765
|-- /git-forge  proxy http://127.0.0.1:8093
```

Ensure Funnel is still on:

```bash
ssh nova "tailscale funnel 443 on"
```

The public endpoint is: `https://nova.taild7cf8c.ts.net/git-forge`

---

## Phase 6 — Claude Desktop: Add git-forge Connection

On the Alienware, edit `claude_desktop_config.json`:
`%APPDATA%\Claude\claude_desktop_config.json`

Add inside `"mcpServers"`:

```json
"git-forge": {
  "type": "url",
  "url": "https://nova.taild7cf8c.ts.net/git-forge/mcp",
  "note": "forge-novel repo MCP server on Nova — git read/write/commit/push"
}
```

Restart Claude Desktop. Verify `git-forge` tools appear.

---

## Phase 7 — Claude.ai Web: Add git-forge Connection

On any device (phone, browser):

1. Go to **claude.ai → Settings → Integrations**
2. Click **Add Integration**
3. Paste: `https://nova.taild7cf8c.ts.net/git-forge/mcp`
4. Name it: `git-forge`
5. Save

This enables web/mobile sessions to read and write directly to forge-novel without the
Alienware being involved.

---

## Phase 8 — Verify End-to-End

From Claude Desktop or Claude.ai web, test each tool:

```
git_pull()                                → syncs with GitHub
list_files()                              → should show README.md, REFERENCE.md, etc.
read_file("SESSIONS.md")                  → should return session log content
write_file("test.md", "hello world")      → creates test file
git_status()                              → should show test.md as untracked
git_diff()                                → shows uncommitted changes
git_commit("test commit", ["test.md"])    → stages test.md and commits
git_push()                                → pushes to GitHub
git_log(5)                                → shows last 5 commits
search_repo("hello")                      → finds match in test.md
```

Cleanup:

```
delete_file("test.md")
git_commit("remove test file", ["test.md"])
git_push()
```

---

## Phase 9 — Add to forge-novel .mcp.json (Claude Code)

Create `.mcp.json` in the `forge-novel` repo root so Claude Code auto-connects:

```json
{
  "mcpServers": {
    "git-forge": {
      "type": "url",
      "url": "https://nova.taild7cf8c.ts.net/git-forge/mcp"
    }
  }
}
```

> **Note:** Tailscale Funnel URLs require Tailscale auth, so this is safe to commit.
> If you prefer, add `.mcp.json` to `.gitignore`.

---

## File Inventory (What Exists in This Repo)

| File | Purpose |
|------|---------|
| `README.md` | Series overview, repo structure, core concept |
| `REFERENCE.md` | Locked worldbuilding decisions — edit deliberately |
| `SESSIONS.md` | Running log of creative sessions — append each chat |
| `characters/MC.md` | Main character sheet (Codex ID: 1) |
| `CLAUDE.md` | This file — build plan and instructions for Claude Code |

---

## Workflow After Setup

Once the server is running, every creative session follows this pattern:

1. Start chat (web, desktop, or CLI — doesn't matter)
2. `git_pull()` to sync latest
3. Load `SESSIONS.md` and `REFERENCE.md` for context
4. Work — brainstorm, design, write
5. At end of session: `append_file("SESSIONS.md", <session log>)` + `git_commit` + `git_push`
6. History is preserved in git, current state always in the files

---

## Troubleshooting

**Claude.ai web connector schema stale (tools show old params):**
Toggle the affected connector off/on in Claude.ai Settings → Connected Apps to force a
schema refresh. Do this after any server-side tool signature changes (e.g. adding params).
- git-forge connector URL: `https://nova.taild7cf8c.ts.net/git-forge/mcp`
- forge-mcp connector URL: `https://nova.taild7cf8c.ts.net/mcp`

**git-forge intermittent drop/recover (Claude.ai web):**
Individual tool calls occasionally error with no pattern — this is a known quirk of the
Streamable HTTP transport over Tailscale Funnel. Retry; recovers within 1-2 attempts.
If repeated failures persist across multiple tools, kill orphan PIDs:
```bash
ssh nova "wsl -d Ubuntu -e bash -c 'pkill -f git-forge || true && sudo systemctl restart git-forge-mcp'"
```

**read_file on large files (e.g. CLAUDE.md at 518 lines):**
`read_file` supports `offset` (0-based line number) and `limit` (max lines) params.
Use `search_repo` first to find relevant line numbers, then page in with offset/limit.
- First 50 lines:  `offset=0, limit=50`
- Lines 454-518:   `offset=454, limit=65`

**Server not responding:**
```bash
ssh nova "wsl -d Ubuntu -e sudo systemctl status git-forge-mcp --no-pager"
ssh nova "wsl -d Ubuntu -e sudo journalctl -u git-forge-mcp -n 50 --no-pager"
```

**Funnel dropped or path missing:**
```bash
ssh nova "tailscale serve status"
# Re-add if missing:
ssh nova "tailscale serve --bg --set-path /git-forge http://127.0.0.1:8093"
ssh nova "tailscale funnel 443 on"
```

**Git push fails (auth):**
Nova needs a GitHub PAT cached in the credential helper.
```bash
ssh nova "wsl -d Ubuntu -e bash -c 'cd ~/forge-novel && git config credential.helper store'"
# Do one manual push — enter PAT as password. Cached permanently after that.
```

**Nova clone is stale:**
```bash
ssh nova "wsl -d Ubuntu -e bash -c 'cd ~/forge-novel && git pull origin main'"
```
Or use the `git_pull()` MCP tool at the start of each session.

**Port conflict with forge-mcp:**
They use different ports — forge-mcp on 8765, git-forge on 8093. Both coexist via
Tailscale path-based routing on the same Funnel hostname.

---

## Architecture Reference

```
┌─────────────────────────────────────────────────────────────┐
│  Clients                                                     │
│  ├── Claude Desktop  ──→ https://nova.../git-forge/mcp      │
│  ├── Claude.ai Web   ──→ https://nova.../git-forge/mcp      │
│  └── Claude Code CLI ──→ https://nova.../git-forge/mcp      │
└────────────────┬────────────────────────────────────────────┘
                 │ Tailscale Funnel (HTTPS)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Nova (Windows + WSL2)                                       │
│  tailscale serve:                                            │
│  ├── /           → http://127.0.0.1:8765  (forge-mcp)       │
│  └── /git-forge  → http://127.0.0.1:8093  (git-forge-mcp)   │
│                                                              │
│  WSL2 systemd services:                                      │
│  ├── forge-mcp.service     → port 8765                       │
│  └── git-forge-mcp.service → port 8093                       │
│       └── ~/forge-novel/   (local git clone)                 │
└─────────────────────────────────────────────────────────────┘
                 │ git push/pull
                 ▼
┌──────────────────────────┐
│  GitHub                   │
│  dblondin73/forge-novel   │
└──────────────────────────┘
```


---

## Publishing Pipeline — Prose Polish

After drafting chapters in the Forge workflow, prose goes through **NovelCrafter**
(novelcrafter.com) for polishing before final commit:

1. Draft chapter in Forge (Claude.ai web / Cowork / Claude Code)
2. Export draft `.md` to NovelCrafter project
3. Connect Anthropic API key (BYOK — Bring Your Own Key)
4. Use NovelCrafter's prose editing modes to tighten, refine voice, catch inconsistencies
5. Final polished chapter back into `drafts/` → `git_commit` + `git_push`

NovelCrafter pricing: $8/mo Hobbyist tier (BYOK) + API usage costs.
Also supports OpenRouter, local models via Ollama/LM Studio.
Capture #75 on Nova records this decision.