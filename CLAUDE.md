# Forge Novel — Claude Code Build Plan

This file is the master instruction set for Claude Code. Run it from VS Code or the CLI to
build the `git-forge` MCP server on Nova and wire up all clients. Everything in this file
reflects decisions already made — Claude Code should execute, not re-design.

---

## Context & Goals

**What already exists:**
- `forge-novel` repo cloned at `C:\Workbench\dev\forge-novel` (Alienware / Windows)
- Four files already committed: `README.md`, `REFERENCE.md`, `SESSIONS.md`, `characters/MC.md`
- Nova headless server (ASUS ROG, `david-laptop`) running WSL2, reachable via Tailscale as `nova`
- Existing Forge MCP server on Nova (FastMCP, Streamable HTTP transport, Tailscale Funnel)
- Claude Desktop and Claude.ai web both connect to Nova MCP servers via Tailscale Funnel URLs

**What we are building:**
A dedicated `git-forge` MCP server that:
- Lives on Nova (WSL2), always-on via systemd
- Owns a clone of `dblondin73/forge-novel` on Nova's filesystem
- Exposes read/write/commit/push tools over Streamable HTTP
- Is accessible from Claude Desktop, Claude Code CLI, and Claude.ai web (phone/browser)
- Uses Tailscale Funnel for the public HTTPS endpoint (same pattern as existing Forge MCP)
- Port: **8093**

---

## Phase 1 — Nova: Clone the Repo

SSH into Nova and clone the repo into WSL2.

```bash
ssh nova
# Inside Nova WSL2:
cd ~
git clone https://github.com/dblondin73/forge-novel.git ~/forge-novel
cd ~/forge-novel
git status
```

Verify the four existing files are present: `README.md`, `REFERENCE.md`, `SESSIONS.md`,
`characters/MC.md`.

---

## Phase 2 — Nova: Write the MCP Server

Create the server file at `~/nova/git_forge_server.py` on Nova.

```bash
mkdir -p ~/nova
```

### File: `~/nova/git_forge_server.py`

```python
"""
git-forge MCP Server
Exposes forge-novel repo read/write/git operations over Streamable HTTP.
Port: 8093
"""

import subprocess
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP

REPO_PATH = Path.home() / "forge-novel"

mcp = FastMCP(
    name="git-forge",
    instructions="Read, write, and commit files in the forge-novel repository.",
)


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


@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from the forge-novel repo. Path is relative to repo root."""
    target = REPO_PATH / path
    if not target.exists():
        raise FileNotFoundError(f"{path} does not exist in forge-novel repo")
    return target.read_text(encoding="utf-8")


@mcp.tool()
def list_files(subdir: str = "") -> str:
    """List files in the forge-novel repo or a subdirectory."""
    target = REPO_PATH / subdir if subdir else REPO_PATH
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
    target = REPO_PATH / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Written: {path} ({len(content)} chars)"


@mcp.tool()
def append_file(path: str, content: str) -> str:
    """Append content to an existing file in the forge-novel repo."""
    target = REPO_PATH / path
    if not target.exists():
        raise FileNotFoundError(f"{path} does not exist — use write_file to create it")
    existing = target.read_text(encoding="utf-8")
    target.write_text(existing + "\n" + content, encoding="utf-8")
    return f"Appended {len(content)} chars to {path}"


@mcp.tool()
def git_commit(message: str, paths: Optional[list[str]] = None) -> str:
    """Stage and commit files. If paths is None, stages all changes (git add -A)."""
    if paths:
        _git(["add"] + paths)
    else:
        _git(["add", "-A"])
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


@mcp.tool()
def git_log(n: int = 10) -> str:
    """Show last n commit messages with dates."""
    return _git(["log", f"-{n}", "--oneline", "--decorate"])


@mcp.tool()
def git_status() -> str:
    """Show working tree status."""
    return _git(["status", "--short"])


@mcp.tool()
def search_repo(query: str) -> str:
    """Search all repo files for a text string. Returns file:line matches."""
    results = []
    for f in sorted(REPO_PATH.rglob("*.md")):
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


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8093)
```

---

## Phase 3 — Nova: Install Dependencies

```bash
ssh nova
# In WSL2:
pip install fastmcp --break-system-packages
# Verify:
python3 ~/nova/git_forge_server.py --help 2>/dev/null || python3 -c "import fastmcp; print('fastmcp OK')"
```

---

## Phase 4 — Nova: Create systemd Service

Create the systemd unit file so the server survives reboots and runs without the laptop.

```bash
ssh nova
# Create the service file:
sudo tee /etc/systemd/system/git-forge-mcp.service > /dev/null << 'EOF'
[Unit]
Description=git-forge MCP Server (forge-novel repo)
After=network.target

[Service]
Type=simple
User=david
WorkingDirectory=/home/david
ExecStart=/usr/bin/python3 /home/david/nova/git_forge_server.py
Restart=always
RestartSec=5
Environment=PATH=/usr/local/bin:/usr/bin:/bin
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start:
sudo systemctl daemon-reload
sudo systemctl enable git-forge-mcp
sudo systemctl start git-forge-mcp

# Verify it's running:
sudo systemctl status git-forge-mcp
curl http://127.0.0.1:8093/
```

> **Note:** Replace `User=david` with whatever `whoami` returns in your Nova WSL2 session
> if it differs.

---

## Phase 5 — Nova: Expose via Tailscale Funnel

```bash
ssh nova
# Funnel port 8093 publicly over HTTPS:
tailscale funnel --bg 8093

# Get the public URL:
tailscale funnel status
```

The URL will look like: `https://david-laptop.tail<xxxxx>.ts.net`

Note this URL — you need it for Phase 6.

---

## Phase 6 — Claude Desktop: Add git-forge Connection

On the Alienware, edit `claude_desktop_config.json`. Location is typically:
`%APPDATA%\Claude\claude_desktop_config.json`

Add the following entry inside `"mcpServers"`:

```json
"git-forge": {
  "type": "url",
  "url": "https://david-laptop.tail<xxxxx>.ts.net/mcp",
  "note": "forge-novel repo MCP server on Nova — git read/write/commit/push"
}
```

Replace the Tailscale URL with the actual one from Phase 5.

Restart Claude Desktop. Verify `git-forge` appears in the tools list.

---

## Phase 7 — Claude.ai Web: Add git-forge Connection

On any device (phone, browser, etc.):

1. Go to **claude.ai → Settings → Integrations**
2. Click **Add Integration**
3. Paste the Tailscale Funnel URL from Phase 5:
   `https://david-laptop.tail<xxxxx>.ts.net/mcp`
4. Name it: `git-forge`
5. Save

This is what enables web UI sessions (like driving-to-work mobile chats) to read and
write directly to the forge-novel repo without the laptop being involved at all.

---

## Phase 8 — Verify End-to-End

From Claude Desktop or Claude.ai web, test each tool:

```
list_files()                          → should show README.md, REFERENCE.md, etc.
read_file("SESSIONS.md")              → should return session log content
write_file("test.md", "hello world")  → creates test file
git_status()                          → should show test.md as untracked
git_commit("test commit")             → stages and commits
git_push()                            → pushes to GitHub
git_log(5)                            → shows last 5 commits
```

Then delete the test file and commit the cleanup:

```
write_file is not a delete tool — use git CLI or a future delete_file tool
```

For now, delete via:
```bash
ssh nova
cd ~/forge-novel
rm test.md
git add -A
git commit -m "remove test file"
git push
```

---

## Phase 9 — Add to forge-novel .mcp.json (Claude Code)

To make Claude Code in VS Code aware of the git-forge server automatically, create
`.mcp.json` in the `forge-novel` repo root:

```json
{
  "mcpServers": {
    "git-forge": {
      "type": "url",
      "url": "https://david-laptop.tail<xxxxx>.ts.net/mcp"
    }
  }
}
```

Replace URL with the actual Tailscale Funnel URL. This file is already in `.gitignore`
candidates — consider gitignoring it if the URL is sensitive, or keep it since Tailscale
Funnel URLs require auth anyway.

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
2. I load `SESSIONS.md` and `REFERENCE.md` for context
3. We work — brainstorm, design, write
4. At end of session: `append_file("SESSIONS.md", <new session log>)` + `git_commit` + `git_push`
5. History is preserved in git, current state always in the files

---

## Troubleshooting

**Server not responding:**
```bash
ssh nova
sudo systemctl status git-forge-mcp
sudo journalctl -u git-forge-mcp -n 50
```

**Funnel dropped:**
```bash
ssh nova
tailscale funnel status
tailscale funnel --bg 8093   # re-enable if needed
```

**Git push fails (auth):**
Nova needs a GitHub Personal Access Token or SSH key configured.
```bash
ssh nova
git -C ~/forge-novel config user.email "dblondin73@gmail.com"
git -C ~/forge-novel config user.name "David Blondin"
# For HTTPS auth, use a PAT stored in git credential manager:
git -C ~/forge-novel config credential.helper store
# Then do one manual push and enter your PAT as the password — it will be cached.
```

**Wrong username in systemd:**
```bash
ssh nova
whoami   # use this value for User= in the service file
sudo systemctl edit git-forge-mcp --force   # edit the unit
sudo systemctl daemon-reload && sudo systemctl restart git-forge-mcp
```
