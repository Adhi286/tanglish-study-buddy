"""Persistent memory: a small JSON file the user owns (private, local)."""
import json
import os

from .config import MEMORY_FILE


def load() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(mem: dict) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)


def remember(key: str, value: str) -> str:
    mem = load()
    mem[key] = value
    save(mem)
    return f"Saved: {key} = {value}"


def forget(key: str) -> str:
    mem = load()
    if mem.pop(key, None) is None:
        return f"Nothing saved under '{key}'."
    save(mem)
    return f"Forgot: {key}"


def as_prompt() -> str:
    mem = load()
    if not mem:
        return "(nothing saved yet)"
    return "\n".join(f"- {k}: {v}" for k, v in mem.items())
