![Zero to Agents](../../assets/banner.png)

# EP11 · MCP servers: give your AI agent new tools (free, local)

**Zero to Agents** · Level 3 · Mac · (video link added when the episode goes live)

> MCP servers give an AI coding agent new tools. Connect the official Git MCP server to Claude Code on a free local model with a project .mcp.json, and allow only the tools that read.

## What you'll have at the end

Claude Code on a free local model connected to the official Git MCP server, answering questions about your history, with only the read-only tools allowed.

## Before you start

- Finish [EP07](../ep07-claude-code-local/) first.
- Finish [EP10](../ep10-claude-code-hooks/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, claude_code 2.1.332, model qwen3.5:9b, uv 0.13.10, mcp_server_git 2026.11.27

## Steps

### 1. Install and try

The official Git server is written in Python. The easiest way to run it is uvx, which comes with uv. Install uv with Homebrew. Then make a small project with two commits, so there's some history to ask about. Run the server once with dash dash help. uvx downloads it and runs it, with nothing else to set up.

```zsh
brew install uv
mkdir -p ~/mcp-demo && cd ~/mcp-demo && git init -q
echo "# Notes" > notes.md && git add . && git commit -qm "Start the notes"
echo "- Buy milk" >> notes.md && git commit -qam "Add a shopping item"
git log --oneline
uvx mcp-server-git --help | head -3
```

### 2. Connect the server

Now tell Claude Code about the server. A file called dot M C P dot json, in the project folder, lists the servers for this project. Ours is called git, and it runs uvx M C P server git, pointed at this folder. Every M C P tool call needs your approval by default. These four tools only read, so we allow them in dot claude slash settings dot json. Tools that commit, reset or switch branches still ask. One more line. Claude Code can also run git in the shell, so we deny that here, and every git action goes through the server and its rules. A quick check that both files are valid JSON.

```zsh
cat > .mcp.json <<'EOF'
{"mcpServers": {"git": {"command": "uvx",
  "args": ["mcp-server-git", "--repository", "."]}}}
EOF
mkdir -p .claude && cat > .claude/settings.json <<'EOF'
{"permissions": {"deny": ["Bash(git:*)"],
  "allow": ["mcp__git__git_status", "mcp__git__git_log",
  "mcp__git__git_show", "mcp__git__git_diff"]}}
EOF
python3 -m json.tool .mcp.json > /dev/null && python3 -m json.tool .claude/settings.json > /dev/null && echo valid
```

### 3. Ask the agent

Start Claude Code in manual mode, so it asks before it changes anything. Answer the first-run questions. The trust screen even lists the four tools this folder pre-approves, so you can check them before you say yes. Then it finds the new server, and warns that M C P servers can run code. The default is to continue without it. We wrote this file ourselves, so choose use this M C P server. Now ask what changed in the most recent commit. The agent tries git in the shell first. Denied. So it switches to the server, and calls git log and git diff, with no prompts, because both only read. A couple of calls fail along the way, and it retries. And there's the answer: one line added to notes dot M D.

```zsh
ollama launch claude --model qwen3.5:9b -- --permission-mode manual
```

Then type this into Claude Code:

> What changed in the most recent commit? Use the git tools.

## Quick reference

**What MCP is**

- MCP = a standard plug for agent tools
- A server is a small program on your Mac
- It tells the agent which tools it has
- The agent calls them, you approve

**Trust rules**

- Install servers you'd install as software
- Allow only the tools you need
- Write tools should still ask
- Tokens: least privilege, never in the file

## Troubleshooting

- `uvx: command not found`: install uv first with `brew install uv`. uvx comes with it.
- Claude Code never asks about the server: it reads `.mcp.json` only from the folder you start it in. Check the file name (with the dot) and that the JSON is valid (`python3 -m json.tool .mcp.json`).
- You chose "Continue without using this MCP server" by mistake: run `/mcp` inside Claude Code to turn it on, or reset the choice with `claude mcp reset-project-choices`.
- Prefer a command to a file? `claude mcp add git -- uvx mcp-server-git --repository .` adds it just for you (local scope); add `--scope project` to write `.mcp.json`. Codex has `codex mcp add`.
- Every git call still asks for approval: the allow list goes in `.claude/settings.json`, and each tool name has the form `mcp__<server>__<tool>`, for example `mcp__git__git_log`.
- The agent runs `git` in the shell instead of the server's tools: that's what the `deny` rule `Bash(git:*)` prevents. Without it, small models often pick the shell.
- Windows: the same files work. Install uv with `winget install astral-sh.uv`, then follow the same steps in PowerShell.

## Next

Continue with [EP12]().

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
