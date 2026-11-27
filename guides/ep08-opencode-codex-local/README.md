![Zero to Agents](../../assets/banner.png)

# EP08 · OpenCode and Codex for free, on your own Mac (with Ollama)

**Zero to Agents** · Level 2 · Mac · (video link added when the episode goes live)

> Run OpenCode and Codex for free on your Mac with Ollama and a local Qwen model: give the model a 64K context window, make OpenCode ask before it acts, and compare them with Claude Code.

## What you'll have at the end

Two more free coding agents running on a local model: OpenCode (set to ask before edits and commands) and Codex, plus the 64K-context model copy they both need.

## Before you start

- Finish [EP07](../ep07-claude-code-local/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, opencode 1.19.6 (installed by ollama launch), codex 0.172.0 (Homebrew cask), model qwen3.5:9b-64k

## Steps

### 1. Bigger context

Write a two-line Modelfile. Start from Qwen 3.5 nine B, and set the context to sixty four thousand tokens. Then create a copy under a new name. It reuses the same download, so it takes no extra space. Now both models are listed.

```zsh
printf 'FROM qwen3.5:9b\nPARAMETER num_ctx 65536\n' > Modelfile
ollama create qwen3.5:9b-64k -f Modelfile
ollama list
```

### 2. Opencode

First, OpenCode. Make a project folder. By default OpenCode edits files and runs commands without asking, so add a small config file that tells it to ask first. Then ollama launch opencode, with the sixty four K model. Ollama offers to install it. Give it the same task as last time. It asks before creating the file. Allow once. And again before running it. Done in well under a minute.

```zsh
mkdir -p ~/oc-demo && cd ~/oc-demo && git init -q
echo '{"permission": {"edit": "ask", "bash": "ask"}}' > opencode.json
ollama launch opencode --model qwen3.5:9b-64k
```

Then type this into OpenCode:

> Create greet.py: it prints a friendly greeting for the name given as the first argument, plus the current date. Then run it with python3, for the name Sam.

### 3. Codex

Now Codex, from OpenAI. Ollama doesn't install this one, so use Homebrew. Make another folder, then ollama launch codex with the same model. Codex asks whether you trust the folder. Then the same task. Codex runs commands freely inside the project folder, and asks before anything outside it. About half a minute later, there's our greeting.

```zsh
brew install codex
mkdir -p ~/cx-demo && cd ~/cx-demo && git init -q
ollama launch codex --model qwen3.5:9b-64k
```

Then type this into Codex:

> Create greet.py: it prints a friendly greeting for the name given as the first argument, plus the current date. Then run it with python3, for the name Sam.

## Quick reference

**Context window**

- OpenCode and Codex need a big context
- Ollama's default here: about 4K tokens
- Agents' instructions: 7K and up
- Fix: a 64K copy of the model

**Compared**

- Claude Code: first answer ~6 min, asks every step
- OpenCode: under a minute, asks if you tell it to
- Codex: under a minute, free inside the folder
- All three: free, local, no account

## The mistake almost everyone makes

**Why your local AI coding agent keeps forgetting things**

Write a two-line Modelfile. Start from Qwen 3.5 nine B, and set the context to sixty four thousand tokens. Then create a copy under a new name. It reuses the same download, so it takes no extra space. Now both models are listed.

## Troubleshooting

- The agent keeps saying it has no context, or keeps 'compacting': the model's context window is too small. Use the 64K copy (`qwen3.5:9b-64k`) from step 1.
- `codex is not installed`: install it first with `brew install codex`. `ollama launch` installs OpenCode and Claude Code itself, but not Codex.
- OpenCode changes files without asking: add the `opencode.json` from step 2 to the project folder.
- Codex asks for approval: it runs commands freely only inside the project folder (its workspace); anything outside needs your OK.

## Next

Continue with [EP09]().

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
