#!/usr/bin/env python3
"""Zero to Agents: local model speed test for Ollama (EP05).

Runs the same three prompts on each model through the local Ollama API and prints
load time, reading speed (prompt tokens/s), writing speed (generated tokens/s), memory
size and how much of the model is on the GPU.

  python3 ollama-speed.py qwen3.5:2b qwen3.5:9b
  python3 ollama-speed.py qwen3.5:9b --ctx 32768     # test a longer context window

Standard library only. Talks to http://localhost:11434 (or $OLLAMA_HOST). Nothing leaves your machine.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

PROMPTS = [
    "Explain what an API is in three sentences.",
    "Write a Python function that checks whether a string is a palindrome.",
    "Give five short tips for keeping a laptop battery healthy.",
]


def ollama_url(raw: str) -> str:
    """OLLAMA_HOST as Ollama reads it: 'host', 'host:port', ':port' or a URL. 0.0.0.0 means this machine.
    Without a port: 11434, or 80/443 when a scheme is given."""
    raw = (raw or "").strip().rstrip("/")
    scheme, default = "http", 11434
    if "://" in raw:
        scheme, raw = raw.split("://", 1)
        default = 443 if scheme == "https" else 80
    host, _, port = raw.rpartition(":") if ":" in raw else (raw, "", "")
    if host in ("", "0.0.0.0", "::", "[::]"):
        host = "127.0.0.1"
    return f"{scheme}://{host}:{port or default}"

HOST = ollama_url(os.environ.get("OLLAMA_HOST", ""))
# Never route through an HTTP proxy: the requests go straight to Ollama.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(HOST + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    try:
        with OPENER.open(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read() or b"{}").get("error") or str(e)
        except ValueError:  # not JSON (e.g. a proxy error page)
            msg = str(e)
        raise RuntimeError(msg) from None


def generate(model: str, prompt: str, ctx: int, think: bool | None) -> dict:
    body = {"model": model, "prompt": prompt, "stream": False, "keep_alive": "5m",
            "options": {"num_ctx": ctx, "temperature": 0, "seed": 42, "num_predict": 256}}
    if think is not None:
        body["think"] = think
    return call("/api/generate", body)


def unload(model: str) -> None:
    call("/api/generate", {"model": model, "keep_alive": 0})


def full_name(model: str) -> str:
    """`ollama ps` lists 'gemma3' as 'gemma3:latest'."""
    return model if ":" in model.rsplit("/", 1)[-1] else model + ":latest"


def bench(model: str, ctx: int) -> dict:
    unload(model)  # start cold: a fair load time, and no cached prompts from an earlier run
    try:
        return _bench(model, ctx)
    finally:
        try:
            unload(model)  # free the memory before the next model, even if this one failed
        except Exception:
            pass


def _bench(model: str, ctx: int) -> dict:
    think: bool | None = False  # quick answers; models without a thinking mode reject the flag
    try:
        first = generate(model, "Hi", ctx, think)  # warm-up: loads the model, measures load time
    except RuntimeError as e:
        if "think" not in str(e):
            raise
        think = None
        first = generate(model, "Hi", ctx, think)
    read_tok = read_ns = write_tok = write_ns = 0
    for p in PROMPTS:
        r = generate(model, p, ctx, think)
        read_tok += r.get("prompt_eval_count", 0)
        read_ns += r.get("prompt_eval_duration", 0)
        write_tok += r.get("eval_count", 0)
        write_ns += r.get("eval_duration", 0)
    want = full_name(model)
    loaded = next((m for m in call("/api/ps").get("models", []) if want in (m.get("name"), m.get("model"))), None)
    size = (loaded or {}).get("size", 0)
    return {
        "model": model,
        "load": first.get("load_duration", 0) / 1e9,
        "read": read_tok / (read_ns / 1e9) if read_ns else 0.0,
        "write": write_tok / (write_ns / 1e9) if write_ns else 0.0,
        "gb": size / 1e9,
        "gpu": round(100 * loaded.get("size_vram", 0) / size) if loaded and size else None,
    }


def verdict(r: dict) -> str:
    if r["gpu"] is None:
        return "couldn't read its memory use"
    if r["gpu"] < 100:
        return "too big: part runs on the CPU"
    if r["write"] >= 20:
        return "fast: great for chat"
    if r["write"] >= 8:
        return "usable: fine for short tasks"
    return "slow: try a smaller model"


def main() -> None:
    ap = argparse.ArgumentParser(description="Ollama speed test (Zero to Agents EP05)")
    ap.add_argument("models", nargs="+", help="model names, as in `ollama list`")
    ap.add_argument("--ctx", type=int, default=4096, help="context window in tokens (default 4096)")
    a = ap.parse_args()
    try:
        call("/api/version")
    except Exception:
        sys.exit(f"Ollama isn't answering at {HOST}. Start it with: brew services start ollama")
    rows = []
    for m in a.models:
        print(f"testing {m} (context {a.ctx})...", flush=True)
        try:
            rows.append(bench(m, a.ctx))
        except Exception as e:
            print(f"  skipped {m}: {e}")
    if not rows:
        sys.exit(1)
    w = max(len("MODEL"), *(len(r["model"]) for r in rows))
    print(f"\n{'MODEL':<{w}}  {'SIZE':>7}  {'GPU':>4}  {'LOAD':>5}  {'READ':>6}  {'WRITE':>5}")
    for r in rows:
        gpu = "  ?" if r["gpu"] is None else f"{r['gpu']:>3}"
        print(f"{r['model']:<{w}}  {r['gb']:>4.1f} GB  {gpu}%  {r['load']:>4.1f}s  {r['read']:>4.0f}/s  {r['write']:>3.0f}/s")
    print("\nREAD and WRITE are tokens per second.")
    for r in rows:
        print(f"{r['model']}: {verdict(r)}")


if __name__ == "__main__":
    main()
