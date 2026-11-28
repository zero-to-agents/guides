![Zero to Agents](../../assets/banner.png)

# EP06 · A private ChatGPT on your Mac with Open WebUI

**Zero to Agents** · Level 1 · Mac · (video link added when the episode goes live)

> Run your own private ChatGPT on a Mac: install Open WebUI with uv, connect it to Ollama, keep it private to your machine, and fix the one setting that makes small models painfully slow.

## What you'll have at the end

Open WebUI running on your Mac on top of Ollama: a ChatGPT-style chat for your local models, private to your machine, with thinking turned off so small models answer in about a second.

## Before you start

- Finish [EP04](../ep04-ollama/) first.
- Finish [EP05](../ep05-model-fit/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, uv 0.13.10, open_webui 0.13.5, model qwen3.5:2b

## Steps

### 1. Install

The easiest way to run Open WebUI is with uv, a fast tool for Python apps. Install it with Homebrew. Then one command downloads and starts Open WebUI. Data dir keeps your chats in a folder in your home directory. And host 127.0.0.1 keeps it private to this Mac. Without it, anyone on your Wi-Fi could reach the login page. The first start downloads a lot, so it takes a few minutes. Keep this terminal window open while you use it.

```zsh
brew install uv
DATA_DIR=~/.open-webui uvx --python 3.12 open-webui@latest serve --host 127.0.0.1
```

### 2. Create account

Now open localhost 8080 in your browser. The first account you create becomes the admin. It's stored only on your Mac, in that data folder, and no email is sent anywhere.

- Open http://localhost:8080
- Click Get started
- Name: "Demo User"
- Email: "demo@example.com"
- Password: a password
- Click Create Admin Account
- Click Okay, Let's Go!

### 3. First chat

Open WebUI found Ollama on its own, and picked our Qwen model. Ask it something. And wait. Nothing yet. Behind the scenes, the model is thinking before it writes, and a small model like this can think for minutes, even for a simple question. That's what makes local AI feel slow. Stop it, and let's fix that.

- Open http://localhost:8080
- Click Message box
- Message: "Give me three tips for a better night's sleep."
- Press Enter
- Click Stop

### 4. Turn off thinking

Here's the fix. Open the admin settings, at slash admin, slash settings, slash models. Click the pencil next to the model, then Advanced Params. Find think, for Ollama, and click it until it says Off. Then save. Now this model answers right away, in every chat.

- Open http://localhost:8080/admin/settings/models
- Click Pencil next to qwen3.5:2b
- Click Advanced Params
- Set think (Ollama) to Off
- Click Save & Update

### 5. Fast chat

Same question, in a new chat. This time the answer starts in about a second. Your chats are saved in the sidebar, and they stay on your Mac.

- Open http://localhost:8080
- Click Message box
- Message: "Give me three tips for a better night's sleep."
- Press Enter

## Quick reference

**How it fits**

- Your browser
- -> Open WebUI   localhost:8080
- -> Ollama   localhost:11434
- -> the model, on your Mac

**Keep it private**

- 127.0.0.1: only this Mac can open it
- Chats live in ~/.open-webui
- Stop it: Control+C in its terminal
- Update: run the same command again

## The mistake almost everyone makes

**The setting that makes local AI answer in seconds**

Here's the fix. Open the admin settings, at slash admin, slash settings, slash models. Click the pencil next to the model, then Advanced Params. Find think, for Ollama, and click it until it says Off. Then save. Now this model answers right away, in every chat.

## Troubleshooting

- `Address already in use`: something else uses port 8080. Add `--port 3000` to the serve command and open localhost:3000.
- No models in the model picker: Ollama isn't running. Run `brew services start ollama` (EP04), then reload the page.
- Answers take minutes: thinking is on. Admin settings → Models → pencil → Advanced Params → think (Ollama) → Off → Save & Update.
- The page stopped working after you closed the terminal: Open WebUI runs only while that window is open. Run the same command again.
- Locked out of the admin account: stop the server and delete the `~/.open-webui` folder to start over. This deletes your chats too.

## Next

Continue with [EP07](../ep07-claude-code-local/).

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
