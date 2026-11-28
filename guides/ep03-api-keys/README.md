![Zero to Agents](../../assets/banner.png)

# EP03 · API keys without leaking them

**Zero to Agents** · Level 0 · Mac · (video link added when the episode goes live)

> Stop leaking API keys: keep them in the macOS Keychain, load them per project with direnv, and block any commit that contains a secret with a global gitleaks hook.

## What you'll have at the end

API keys kept out of your code: stored in the macOS Keychain, loaded per project with direnv, and a global git hook that blocks any commit containing a secret.

## Before you start

- Finish [EP02](../ep02-base-layer/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 2.38.2 8.30.1 2.50.1  (Apple silicon)

## Steps

### 1. The wrong way

This is the mistake. A config file with the key written right in it. It works, and that's the problem. The moment this file is committed, the key is in git forever. The token you'll see in this video is fake.

```zsh
mkdir -p ~/api-demo && cd ~/api-demo && git init -q
cat config.sh
```

### 2. Env and gitignore

Step one. Put secrets in a file git ignores. We rename it to dot env, and add dot env to dot gitignore. Then commit an example file with the names but no values, so teammates know what to fill in. Git status no longer lists the secret file.

```zsh
mv config.sh .env
echo '.env' >> .gitignore
printf 'GITHUB_TOKEN=\n' > .env.example
git status --short
```

### 3. Keychain

Step two. Better than a file is the macOS Keychain, the same encrypted store your passwords live in. This command saves the token under a name you choose. It asks for the value twice, and nothing shows while you type. To read it back, use find generic password. Now the key lives in the Keychain, so we can delete the dot env file.

```zsh
security add-generic-password -a "$USER" -s demo-github-token -w
security find-generic-password -a "$USER" -s demo-github-token -w
rm .env
```

### 4. Direnv

Step three. Load the key only when you're working in this project. That's what direnv does. Install it, and type y when Homebrew asks to confirm. Then hook it into your shell, and create a dot envrc file that reads the key from the Keychain. Notice the file has no secret in it, just the command to fetch it. Run direnv allow to approve it. Inside the project, the token is set. Step out of the folder and it's gone. Step back in and it loads again.

```zsh
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc && source ~/.zshrc
echo 'export GITHUB_TOKEN="$(security find-generic-password -a "$USER" -s demo-github-token -w)"' > .envrc
direnv allow
```

### 5. Gitleaks global hook

Step four, the safety net. Gitleaks scans for secrets. We install it and add one global git hook, so every repo on your Mac runs it before each commit. One thing to know. A global hooks path replaces each repo's own hooks folder. If a project relies on its own hooks, add them to this one script.

```zsh
brew install gitleaks
mkdir -p ~/.config/git/hooks
printf '#!/bin/sh\nexec gitleaks git --pre-commit --staged --redact --no-banner\n' > ~/.config/git/hooks/pre-commit
chmod +x ~/.config/git/hooks/pre-commit
git config --global core.hooksPath ~/.config/git/hooks
```

### 6. The block

Now let's try to leak a key on purpose. Write the token into a file, add it, and commit. Gitleaks finds it and the commit is blocked. Nothing was saved. Unstage and delete the file, and commit the safe files instead.

```zsh
git add leaked.txt && git commit -m "oops"
git rm --cached -q leaked.txt && rm leaked.txt
git add .gitignore .env.example .envrc && git commit -m "Keep secrets out of git"
```

## The mistake almost everyone makes

**This git hook stops you from leaking API keys**

Now let's try to leak a key on purpose. Write the token into a file, add it, and commit. Gitleaks finds it and the commit is blocked. Nothing was saved. Unstage and delete the file, and commit the safe files instead.

## Troubleshooting

- `direnv: error .envrc is blocked`: run `direnv allow` in that folder. direnv only loads files you approved.
- The variable is empty after `direnv allow`: check the Keychain item name matches (`security find-generic-password -a "$USER" -s <name> -w`).
- The hook doesn't run: check `git config --global core.hooksPath` and that the hook file is executable (`chmod +x`).
- You already pushed a key: rotate it at the provider first. Removing it from git history does not make it safe again.

## Next

Continue with [EP04](../ep04-ollama/).

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
