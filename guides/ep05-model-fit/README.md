![Zero to Agents](../../assets/banner.png)

# EP05 · Which local AI model fits your Mac?

**Zero to Agents** · Level 1 · Mac · (video link added when the episode goes live)

> Find the biggest local AI model your Mac can run: what parameters and quantization mean, how much memory the GPU gets, a free Ollama speed test, and a chart from 8 GB to 128 GB.

## What you'll have at the end

You know how much memory your Mac can give to local models, how big a model really is, and how fast it runs on your machine, measured with a free speed test.

## Before you start

- Finish [EP04](../ep04-ollama/) first.
- A Mac you can install software on (you'll need your password).

**Tested with:** macOS 26.6.2 (Apple silicon, 16 GB VM), ollama 0.40.18, models qwen3.5:2b (2.2B mxfp8, 3.1 GB), qwen3.5:9b (9.7B nvfp4, 7.6 GB), python 3.9+ (system) or Homebrew 3.15

## Steps

### 1. Your mac

First, what does your Mac have? This shows the chip and the memory. On Apple silicon, the graphics chip shares that memory, and by default it can use roughly two thirds of it for models. On this sixteen gigabyte Mac, Ollama gets about ten and a half. Now look at a model. Ollama show lists its parameters, about two billion here, and its quantization. On a Mac, Ollama picks builds made for Apple's MLX engine.

```zsh
sysctl -n machdep.cpu.brand_string; sysctl -n hw.memsize | awk '{print $1/1073741824 " GB"}'
ollama show qwen3.5:2b | head -8
```

### 2. Speed test

Now measure it. Our free speed test is in the guides repo. Clone it, then run it with a model name. It sends the same three prompts through Ollama's local API, and reports how long the model took to load, how fast it reads your prompt, and how fast it writes, in tokens per second. Anything above about twenty is faster than you can read.

```zsh
git clone -q https://github.com/zero-to-agents/guides ~/zta-guides
python3 ~/zta-guides/tools/ollama-speed.py qwen3.5:2b
```

### 3. Nine billion

Let's step up to the nine billion version. It's seven point six gigabytes, so it fits in our ten and a half gigabyte budget. The download takes a few minutes, so we'll skip ahead. Then test both models side by side. The bigger model takes longer to load the first time, and writes a bit slower, but it's still fast, and bigger models usually give better answers. The GPU column says one hundred percent, so the whole model runs on the graphics chip.

```zsh
ollama pull qwen3.5:9b
python3 ~/zta-guides/tools/ollama-speed.py qwen3.5:2b qwen3.5:9b
```

### 4. Check the size

Here's the mistake. Grabbing the biggest version of a model. This is the same nine billion model at sixteen bits. Ollama shows the size as soon as the download starts. Eighteen gigabytes. That will never fit in this Mac's budget. A model that doesn't fit either fails to load, or runs partly on the CPU and gets painfully slow. Press control C to cancel.

```zsh
ollama pull qwen3.5:9b-bf16
```

## Quick reference

**What sets the size**

- Size = parameters x bits per weight
- 9B at 16-bit: about 18 GB
- 9B at 8-bit: about 10 GB
- 9B at 4-bit: about 7.6 GB

**Fit chart**

- Your Mac -> biggest comfortable model (4-bit)
- 8 GB: 2B to 4B
- 16 GB: up to 9B
- 32 GB: 27B, just
- 48 to 64 GB: 35B-A3B
- 128 GB: 122B

## The mistake almost everyone makes

**Check this number before you download an AI model**

Here's the mistake. Grabbing the biggest version of a model. This is the same nine billion model at sixteen bits. Ollama shows the size as soon as the download starts. Eighteen gigabytes. That will never fit in this Mac's budget. A model that doesn't fit either fails to load, or runs partly on the CPU and gets painfully slow. Press control C to cancel.

## Troubleshooting

- `Ollama isn't running`: start it with `brew services start ollama` (EP04).
- `skipped <model>: model ... not found`: pull it first with `ollama pull <model>`, and use the exact name from `ollama list`.
- GPU column below 100%: the model doesn't fit in the GPU's share of memory, so part runs on the much slower CPU. Pick a smaller model or a 4-bit build.
- The first run of a model is slow: that's the LOAD column, reading the model from disk. Later runs start faster.
- You cancelled a download halfway: Ollama keeps the partial files so a later pull can resume. To free the space, delete the files ending in `-partial` in `~/.ollama/models/blobs`.

## Next

Continue with [EP06]().

---

Made by [Zero to Agents](https://www.youtube.com/@zerotoagents). Narrated by an AI voice and produced with AI agents; every command was run for real on a clean machine. Found a step that no longer works? Open an issue.
