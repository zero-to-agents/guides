![Zero to Agents](../../assets/banner.png)

# EP10 · Claude Code hooks: a rule your AI agent can't ignore

**Zero to Agents** · Level 3 · Mac · (video link added when the episode goes live)

> Claude Code hooks run your own script before a tool runs. Block files written in the wrong place, and the agent fixes itself, even on a free local model with Ollama.

## What you'll have at the end

A Claude Code hook that checks every file write and blocks the ones that break your project's rules, working even on a small local model.

## Before you start

- Finish [EP07](../ep07-claude-code-local/) first.
- Finish [EP09](../ep09-agents-md/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, claude_code 2.1.332, model qwen3.5:9b

## Steps

### 1. Write the hook

Make a project, with a dot claude folder for hooks. The hook is five lines of Python. It reads the file path from the tool call, and if it's a Python file outside src, it prints why and exits with code two. Then tell Claude Code to run it before every Write or Edit, in dot claude slash settings dot json. A quick check that the JSON is valid.

```zsh
mkdir -p ~/hooks-demo/.claude/hooks && cd ~/hooks-demo && git init -q
cat > .claude/hooks/src_only.py <<'EOF'
import json, sys
path = json.load(sys.stdin)["tool_input"].get("file_path", "")
if path.endswith(".py") and "/src/" not in path:
    print("Blocked: Python files go in the src/ folder.", file=sys.stderr)
    sys.exit(2)
EOF
cat > .claude/settings.json <<'EOF'
{"hooks": {"PreToolUse": [{"matcher": "Write|Edit",
  "hooks": [{"type": "command", "command": "python3 .claude/hooks/src_only.py"}]}]}}
EOF
python3 -m json.tool .claude/settings.json
```

### 2. Blocked and fixed

Start Claude Code in the project, in accept edits mode, so it can write files on its own. It asks whether you trust this folder. That matters: trusting a folder is what lets its hooks run, so only trust your own projects. Now ask for the greeting script, without mentioning src. The first answer takes a few minutes, so we skip ahead. Claude Code tries to write greet dot py in the wrong folder. The hook blocks it, and the agent reads the reason. Then it writes the file into src instead, and asks before running anything.

```zsh
ollama launch claude --model qwen3.5:9b -- --permission-mode acceptEdits
```

Then type this into Claude Code:

> Create greet.py: it prints a friendly greeting for the name given as the first argument.

### 3. Check

Check the result. The only Python file outside the hooks folder is in src, exactly where the rule says.

```zsh
find . -name "*.py" -not -path "./.claude/*"
```

## Quick reference

**How hooks work**

- Before a tool runs, your script checks it
- Exit code 2 = blocked
- The reason goes back to the agent
- No AI involved: it always runs

**Limits**

- A hook checks only the tools it matches
- Hooks run your code: trust only your own
- Codex: sandbox + approvals
- OpenCode: permission rules

## The mistake almost everyone makes

**Watch an AI agent get blocked, then fix itself**

Start Claude Code in the project, in accept edits mode, so it can write files on its own. It asks whether you trust this folder. That matters: trusting a folder is what lets its hooks run, so only trust your own projects. Now ask for the greeting script, without mentioning src. The first answer takes a few minutes, so we skip ahead. Claude Code tries to write greet dot py in the wrong folder. The hook blocks it, and the agent reads the reason. Then it writes the file into src instead, and asks before running anything.

## Troubleshooting

- The hook never runs: Claude Code only uses a project's hooks after you trust the folder. Start it in the project folder and choose Yes, I trust this folder.
- `python3 -m json.tool` shows an error: settings.json isn't valid JSON (a missing comma or bracket). Fix it before starting Claude Code.
- The agent gets around the rule another way: a hook only checks the tools its matcher names. This one checks Write and Edit, not shell commands.
- Blocked writes don't reach the agent: the hook must exit with code 2 and print the reason to stderr.

## Next

Continue with [EP11](../ep11-mcp-servers/).

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
