![Zero to Agents](../../assets/banner.png)

# EP09 · AGENTS.md: one file that teaches every coding agent your rules

**Zero to Agents** · Level 3 · Mac · (video link added when the episode goes live)

> Write one AGENTS.md file and Claude Code, Codex and OpenCode all read your project rules. Tested on a local model: what they follow, what they forget, and how to check.

## What you'll have at the end

An AGENTS.md file in your project that Claude Code, Codex and OpenCode all read, and an honest picture of how well small local models follow it.

## Before you start

- Finish [EP07](../ep07-claude-code-local/) first.
- Finish [EP08](../ep08-opencode-codex-local/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, claude_code 2.1.332, codex 0.172.0, opencode 1.19.6, models qwen3.5:9b, qwen3.5:9b-64k

## Steps

### 1. Write the file

Make a project and write two simple rules we can check. Python scripts go in a src folder, and every Python file starts with a specific comment line.

```zsh
mkdir -p ~/rules-demo && cd ~/rules-demo && git init -q
printf '# Project rules\n\n- Put all Python scripts in the src/ folder.\n- Start every Python file with this exact comment line: # Part of the hello project\n' > AGENTS.md
cat AGENTS.md
```

### 2. Codex follows

First, Codex, with the exec command, which runs one task and exits. We don't mention the rules at all. Codex reads agents dot md, puts the script in src, and starts it with our comment line.

```zsh
ollama launch codex --model qwen3.5:9b-64k -- exec --sandbox workspace-write "Create greet.py: it prints a friendly greeting for the name given as the first argument. Then run it with python3 for the name Sam."
head -2 src/greet.py
```

### 3. Claude follows

Now Claude Code. Clear out the folder, and ask for the same script with dash p, which also runs once and exits. Accept edits mode lets it write files, but not run commands. Claude Code reads agents dot md too. Same folder, same comment line.

```zsh
rm -rf src
ollama launch claude --model qwen3.5:9b -- -p --permission-mode acceptEdits "Create greet.py: it prints a friendly greeting for the name given as the first argument."
head -2 src/greet.py
```

### 4. Opencode forgets

And OpenCode. Ask it to quote the rules it was given, without doing anything. It quotes agents dot md word for word, so it definitely read the file. But in our tests, with this small model, it usually ignored those rules while working, even when we reminded it. Reading the rules isn't the same as following them.

```zsh
rm -rf src
ollama launch opencode --model qwen3.5:9b-64k -- run "Without using any tools, quote the project rules from your instructions, word for word."
```

## Quick reference

**What it is**

- AGENTS.md: plain text rules in your project
- Read by Codex, OpenCode and Claude Code
- Short and specific beats long
- Commit it with your code

**Tips**

- Keep rules short and checkable
- Repeat the key rule in your request
- Check the result: small models forget
- Bigger models follow rules better

## The mistake almost everyone makes

**Your AI coding agent read the rules. It still ignored them**

And OpenCode. Ask it to quote the rules it was given, without doing anything. It quotes agents dot md word for word, so it definitely read the file. But in our tests, with this small model, it usually ignored those rules while working, even when we reminded it. Reading the rules isn't the same as following them.

## Troubleshooting

- The agent ignores a rule: small local models often do. Put the most important rule in your request too, and always check the result.
- Claude Code also reads CLAUDE.md. If you have both, keep the shared rules in AGENTS.md and only Claude-specific notes in CLAUDE.md.
- Rules seem to have no effect: start the agent from the project folder (where AGENTS.md is), not from your home folder.

## Next

Continue with [EP10]().

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
