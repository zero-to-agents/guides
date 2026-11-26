![Zero to Agents](../../assets/banner.png)

# EP02 · Terminal, Homebrew and git: the base layer

**Zero to Agents** · Level 0 · Mac · [Watch the video](https://youtu.be/jTy4HypfxoQ)

> Set up a new Mac for development: Homebrew, git, the GitHub CLI and an SSH key, step by step, with the PATH mistake everyone hits.

## What you'll have at the end

Homebrew installed, git configured, GitHub CLI signed in, SSH key on GitHub

## Before you start

- Nothing. This is a starting point.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon), Homebrew 7.0.16, git 2.56.1, GitHub CLI 2.106.0

## Steps

### 1. Open terminal

Open Terminal. Press Command and Space, type Terminal, and press Return. The window you see is a shell called Z shell (zsh). It's the default on every Mac since 2019. You type a command, press Return, and it runs. The first command shows which shell you're using. The second shows your macOS version. Nothing here changes your system.

```zsh
echo $SHELL
sw_vers
```

### 2. Brew install

Install Homebrew, the package manager most Mac developers use. Copy the current install command from [brew.sh](https://brew.sh) and paste it into Terminal. It asks for your Mac password (nothing shows while you type, which is normal), then asks you to press Return. If your Mac doesn't have Apple's command line developer tools yet, the installer downloads them too, which can take several minutes.

```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 3. Brew path

Here's the mistake almost everyone makes. The install finishes, you type brew in the same window, and you get "command not found." That window was opened before Homebrew existed, so it doesn't know where Homebrew lives yet. The fix is in the Next steps section the installer printed. The first line adds Homebrew's setup to your shell's startup file. The second applies it to this window right now. Run `brew --version` again, and it works. New terminal windows would find brew on their own, because the installer also adds it to the system path, but these two lines set up the rest of Homebrew's environment too, so run them anyway.

```zsh
brew --version
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
brew --version
```

### 4. Brew doctor

Two commands worth knowing from day one. Brew doctor checks your setup for problems. On a brand new Mac right now, it shows one warning, about root certificates, with a link to an Apple support page that explains it. It's advice, not an error, and Homebrew keeps working. Read it, and decide later. Then brew update and brew upgrade keep everything current. Run them about once a week.

```zsh
brew doctor
brew update && brew upgrade
```

### 5. Install git gh

Now install git and the GitHub command line tool. macOS comes with an older git from Apple. The Homebrew one is newer and updates with everything else. Homebrew lists what it's about to install, including the small libraries git needs, and asks you to confirm. Type y and press Return. Which git should point to /opt/homebrew. Here it still shows Apple's git in /usr/bin. That's because your shell remembers where commands were when the window opened. Type rehash, or open a new window, and check again. Now it's Homebrew's git.

```zsh
brew install git gh
which git
rehash
which git && git --version
gh --version
```

### 6. Git config

Tell git who you are. This name and email go on every commit you make. If you want your email kept private, GitHub gives you a no-reply address in your email settings. Use that here. We also set the default branch name to main, and told git to merge when you pull. That avoids a confusing prompt later.

```zsh
git config --global user.name "Demo User"
git config --global user.email "361407752+zerotoagents-demo@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global --list
```

### 7. Ssh key

Next, an SSH key. It's how your Mac proves to GitHub that it's you, with no password. We'll use the ed25519 type, which is short, fast and secure. Press Return to accept the default location, and set a passphrase. You now have two files. The one ending in `.pub` is public, and you can share it. The other one is private. Never share it, never paste it anywhere, and never commit it.

```zsh
ssh-keygen -t ed25519 -C "zero-to-agents demo mac"
ls ~/.ssh
```

### 8. Ssh agent

So you don't type the passphrase every time, let macOS remember it in your keychain.

```zsh
printf "Host github.com\n  AddKeysToAgent yes\n  UseKeychain yes\n  IdentityFile ~/.ssh/id_ed25519\n" >> ~/.ssh/config
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### 9. Gh auth login

Now sign in to GitHub from the terminal. Run gh auth login with three options: github.com, SSH for git, and sign in through the web browser. It offers to upload the SSH key we just made. Press Return to accept, and Return again to keep the default title. Then it shows a one-time code and opens your browser. In the browser, sign in, paste the code, and approve. Back in the terminal, it says you're logged in.

```zsh
gh auth login --hostname github.com --git-protocol ssh --web
```

### 10. Verify

Let's prove it all works. First, ask GitHub who we are. Then test the SSH connection. The first time, ssh asks whether you trust github.com. Type yes. Then create a repo, clone it, and push a first commit. That push used your SSH key, with no password. Your Mac can now install anything, track changes, and talk to GitHub.

```zsh
gh auth status
ssh -T git@github.com
gh repo create first-repo --private --clone --add-readme
cd first-repo && echo 'hello from level zero' >> README.md
git add README.md && git commit -m "First commit from the base layer"
git push
```

## The mistake almost everyone makes

**brew: command not found? Here is the fix**

Here's the mistake almost everyone makes. The install finishes, you type brew in the same window, and you get "command not found." That window was opened before Homebrew existed, so it doesn't know where Homebrew lives yet. The fix is in the Next steps section the installer printed. The first line adds Homebrew's setup to your shell's startup file. The second applies it to this window right now. Run `brew --version` again, and it works. New terminal windows would find brew on their own, because the installer also adds it to the system path, but these two lines set up the rest of Homebrew's environment too, so run them anyway.

## Troubleshooting

- `brew: command not found` right after installing: run the two Next steps lines (Step 3), or open a new terminal window.
- `brew doctor` warns about root certificates: it links to an Apple support page. It is advice, not an error; Homebrew keeps working.
- `which git` still shows /usr/bin/git: run `rehash` or open a new window. Your shell cached the old location.
- `ssh -T git@github.com` asks if you trust github.com: type yes. It only asks the first time.
- `Permission denied (publickey)`: run `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` and check the key is on your GitHub account (`gh ssh-key list`).

## Next

Continue with [EP03](../ep03-api-keys/).

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
