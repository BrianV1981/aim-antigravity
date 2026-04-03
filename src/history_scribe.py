#!/usr/bin/env python3
"""
history_scribe.py — Event-Driven Markdown Chunker (Issues #22 + #26)

Stateless chunker that receives a complete, static .md transcript and splits it
into 10-turn chunk files written to memory/hourly/. No daemon, no JSON, no LLM calls.

Public API:
    scribe_session(transcript_path)   — Chunk a single transcript
    scribe_all_sessions()             — Batch-process all un-scribed transcripts in archive/raw/
"""
import sys
import json
import os
import glob
from datetime import datetime

# --- DYNAMIC ROOT DISCOVERY ---
def find_aim_root():
    """Dynamically discovers the A.I.M. root directory."""
    current = os.path.abspath(os.path.dirname(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "core", "CONFIG.json")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
sys.path.insert(0, os.path.join(AIM_ROOT, "scripts"))

try:
    from extract_signal import parse_markdown_transcript
except ImportError:
    parse_markdown_transcript = None

# --- CONFIGURABLE PATHS (patchable by tests) ---
HOURLY_DIR = os.path.join(AIM_ROOT, "memory", "hourly")
RAW_DIR = os.path.join(AIM_ROOT, "archive", "raw")
STATE_FILE = os.path.join(AIM_ROOT, "archive", "scribe_state.json")

# --- CONSTANTS ---
CHUNK_SIZE = 10  # turns per chunk


def _load_state():
    """Load the idempotency state ledger."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def _save_state(state):
    """Persist the idempotency state ledger."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def _parse_turns(transcript_text):
    """Parse a Markdown transcript into structured turns.
    Uses extract_signal.parse_markdown_transcript if available,
    otherwise falls back to a minimal inline parser."""
    if parse_markdown_transcript:
        return parse_markdown_transcript(transcript_text)

    # Fallback inline parser for Antigravity-style transcripts
    import re
    turns = []
    blocks = re.split(r'### (User Input|Planner Response)', transcript_text)
    current_role = "SYSTEM"
    for block in blocks:
        if block == "User Input":
            current_role = "USER"
        elif block == "Planner Response":
            current_role = "A.I.M."
        elif block.strip():
            text = block.strip()
            if turns and turns[-1]['role'] == current_role:
                turns[-1]['text'] += f"\n\n{text}"
            else:
                turns.append({"role": current_role, "text": text})
    return [t for t in turns if t['role'] in ['USER', 'A.I.M.']]


def scribe_session(transcript_path):
    """
    Primary entry point. Takes a path to a static .md transcript,
    parses it into turns, chunks them into CHUNK_SIZE-turn windows,
    and writes each chunk to HOURLY_DIR.

    Idempotent: won't re-process a file that's already in the state ledger.
    """
    basename = os.path.basename(transcript_path)

    # Idempotency check
    state = _load_state()
    if basename in state:
        return 0

    # Read and parse
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except (IOError, OSError) as e:
        print(f"[SCRIBE ERROR] Cannot read {transcript_path}: {e}")
        return 0

    turns = _parse_turns(raw_text)
    if not turns:
        # Mark as scribed even if empty, to prevent re-processing
        state[basename] = {"scribed_at": datetime.now().isoformat(), "chunks": 0}
        _save_state(state)
        return 0

    # Chunk into CHUNK_SIZE-turn windows
    os.makedirs(HOURLY_DIR, exist_ok=True)
    timestamp_slug = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Derive a short session tag from the filename
    session_tag = basename.replace(".md", "").replace("session_", "")[:16]

    chunk_count = 0
    for i in range(0, len(turns), CHUNK_SIZE):
        chunk_turns = turns[i:i + CHUNK_SIZE]
        chunk_num = (i // CHUNK_SIZE) + 1

        # Build the chunk Markdown
        chunk_md = f"# Session Chunk {chunk_num} — {session_tag}\n"
        chunk_md += f"**Turns:** {i+1}–{i+len(chunk_turns)} of {len(turns)}\n"
        chunk_md += f"**Scribed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n"

        for turn in chunk_turns:
            role_label = "👤 USER" if turn['role'] == "USER" else "🤖 A.I.M."
            chunk_md += f"## {role_label}\n{turn['text']}\n\n"

        # Write the chunk file
        chunk_filename = f"{timestamp_slug}_{session_tag}_chunk{chunk_num}.md"
        chunk_path = os.path.join(HOURLY_DIR, chunk_filename)
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk_md)

        chunk_count += 1

    # Update state ledger
    state[basename] = {
        "scribed_at": datetime.now().isoformat(),
        "chunks": chunk_count,
        "turns": len(turns),
    }
    _save_state(state)

    print(f"[SCRIBE] ✅ {basename} → {chunk_count} chunk(s) written to memory/hourly/")
    return chunk_count


def scribe_all_sessions():
    """
    Batch mode. Scans archive/raw/*.md for any un-scribed transcripts
    and processes each one via scribe_session().
    """
    md_files = glob.glob(os.path.join(RAW_DIR, "*.md"))
    if not md_files:
        print("[SCRIBE] No transcripts found in archive/raw/.")
        return 0

    total_chunks = 0
    for md_path in md_files:
        total_chunks += scribe_session(md_path)

    print(f"[SCRIBE] Batch complete: {total_chunks} total chunk(s) from {len(md_files)} transcript(s).")
    return total_chunks


if __name__ == "__main__":
    scribe_all_sessions()
