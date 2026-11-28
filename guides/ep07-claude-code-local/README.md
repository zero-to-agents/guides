![Zero to Agents](../../assets/banner.png)

# EP07 · Claude Code for free, on your own Mac (with Ollama)

**Zero to Agents** · Level 2 · Mac · (video link added when the episode goes live)

> Run Claude Code for free on your Mac with a local model: ollama launch installs it, connects it to Qwen 3.5 through Ollama, and it writes and runs code while asking before every change. No account, no API key.

## What you'll have at the end

Claude Code installed and running on a local Qwen model through Ollama: it writes and runs code in your project, asks before every change, and costs nothing.

## Before you start

- Finish [EP04](../ep04-ollama/) first.
- Finish [EP05](../ep05-model-fit/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, claude_code 2.1.332 (installed by ollama launch), model qwen3.5:9b

## Steps

### 1. Install and start

Make a folder for a small project, and start a git repository in it. Then run ollama launch claude, with the model, and two dashes before an option for Claude Code itself: manual permission mode. Ollama sees Claude Code isn't installed and offers to install it. Then three first-run questions. Pick a theme, read the security notes, and trust this folder, since it's your own project.

```zsh
mkdir -p ~/hello-cli && cd ~/hello-cli && git init -q
ollama launch claude --model qwen3.5:9b -- --permission-mode manual
```

### 2. First task

Now give it a real task. Create a script that greets someone by name, with today's date, and run it. The first answer is slow on a local model, because Claude Code sends long instructions with your first message. Here it took almost six minutes, so we'll skip ahead. In manual mode, it asks before it creates a file. Read it, then approve. And it asks again before running a command. Never let an agent run commands you haven't checked. There's the greeting.

```zsh
ollama launch claude --model qwen3.5:9b -- --permission-mode manual
```

Then type this into Claude Code:

> Create greet.py: it prints a friendly greeting for the name given as the first argument, plus the current date. Then run it with the name Sam.

When it asks for permission, read the request, then press 1 (Yes) to approve.

### 3. Follow up

Now that it has read its instructions, follow-ups are quick. Continue the same conversation and ask for a shout option. This time the whole round trip takes seconds. It edits the file, asks to run it, and shows the result.

```zsh
ollama launch claude --model qwen3.5:9b -- --permission-mode manual --continue
```

Then type this into Claude Code:

> Add a --shout option that prints the greeting in capital letters. Then run it for Sam with --shout.

When it asks for permission, read the request, then press 1 (Yes) to approve.

### 4. Review the code

Always look at what an agent wrote before you rely on it. Here's the script, it works with and without shout, and git status shows exactly which files changed.

```zsh
cat greet.py
python3 greet.py Sam && python3 greet.py Sam --shout
git status --short
```

## Quick reference

**How it works**

- Claude Code: reads, writes and runs code
- -> Ollama: speaks Claude Code's API, locally
- -> Qwen 3.5 9B on your Mac
- Free · private · no account

**What to expect**

- First message: slow (minutes)
- Next messages: seconds
- Manual mode: approve every step
- Small models make mistakes: review

## The mistake almost everyone makes

**Never let an AI agent run commands unchecked**

Now give it a real task. Create a script that greets someone by name, with today's date, and run it. The first answer is slow on a local model, because Claude Code sends long instructions with your first message. Here it took almost six minutes, so we'll skip ahead. In manual mode, it asks before it creates a file. Read it, then approve. And it asks again before running a command. Never let an agent run commands you haven't checked. There's the greeting.

## Troubleshooting

- `Claude Code didn't start because this folder isn't trusted`: run the command again and choose Yes, I trust this folder (only for your own code).
- The first answer takes minutes: Claude Code sends long instructions with the first message, and a small local model reads them slowly. Later messages take seconds. A bigger Mac or a smaller task helps.
- `claude: command not found` when you run it directly: add `~/.local/bin` to your PATH (`echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc`), or keep using `ollama launch claude`.
- Commands are blocked with `auto mode's check had no usable answer`: you're in auto mode, which needs a stronger model. Start with `-- --permission-mode manual` and approve each step yourself.
- The warning `Model isn't recognized · context assumed to be 1m tokens` is harmless: Claude Code doesn't know local models by name.

## Next

Continue with [EP08](../ep08-opencode-codex-local/).

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
