#!/usr/bin/env python3
"""
Shared configuration loader for vision-skill.

Loads config.txt from the project root, with automatic search
and backward-compatible fallback to .env.
"""

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


def _find_config_file():
    """Find config.txt or fall back to .env. Returns (path, found)."""
    # Priority: config.txt in known locations
    candidates = [
        Path(__file__).parent.parent / "config.txt",      # project root
        Path.cwd() / "config.txt",                         # current dir
        Path.home() / ".claude" / "skills" / "gpt-image2-ppt-skills" / "config.txt",
    ]

    for cand in candidates:
        if cand.exists():
            return str(cand), True

    # Fallback: try .env for backward compatibility
    for cand in [
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
        Path.home() / ".claude" / "skills" / "gpt-image2-ppt-skills" / ".env",
    ]:
        if cand.exists():
            return str(cand), True

    return None, False


def load_config():
    """Load config.txt into environment. Called once at module import time."""
    path, found = _find_config_file()
    if found:
        load_dotenv(path, override=True)
        return str(path)
    return None


# Auto-load on import
_CONFIG_PATH = load_config()
