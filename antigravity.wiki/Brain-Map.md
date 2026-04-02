# A.I.M. Brain Map (Cognitive Architecture)

This document maps the complete anatomical structure of the A.I.M. "Brain." 

## 1. The Failsafe Snapshot Layer
*   **Trigger:** Executed silently in the background on every turn by `hooks/failsafe_context_snapshot.py`.
*   **Function:** Saves a rolling JSON backup to `continuity/INTERIM_BACKUP.json` and a markdown tail to `continuity/FALLBACK_TAIL.md`.
*   **Purpose:** Session rescue during crashes.

## 2. The Continuity Pulse (The Handoff)
*   **Trigger:** Executed by `aim reincarnate`.
*   **Function:** Generates `CURRENT_PULSE.md` (the State) and writes the executive directive to `continuity/REINCARNATION_GAMEPLAN.md`.
*   **Purpose:** To teleport context to a fresh agent before "System Prompt Fade" occurs.

## 3. The Waterfall Refinement Pipeline (Active Memory)
*   **Trigger:** Waterfall intervals (1h to 30d).
*   **Storage:** `core/MEMORY.md` (Durable Core).
*   **Mechanism:** ARC-only model (Adds/Removes/Contradicts) to minimize token burn.
*   **Consume & Clean:** Higher tiers automatically archive/delete consumed reports from lower tiers to keep the workspace pristine.

## 4. The Central Engram DB (The Subconscious)
*   **Trigger:** Automatic re-indexing via `src/bootstrap_brain.py` and `aim ingest`.
*   **Storage:** `archive/engram.db` (Local SQLite).
*   **Function:** Hybrid RAG (Semantic Vectors + Lexical FTS5).

## 5. Eternal Recall (History Search)
*   **Trigger:** Event-driven native parsing of `.md` exports in the `Downloads/` folder via `src/extract_signal.py` (The Scribe).
*   **Storage:** `archive/history/` (Markdown) and `archive/history.db` (SQLite).
*   **Splitting:** Massive sessions are split at the 2000-line threshold.
*   **Function:** Dedicated keyword search across the entire project history.

## 6. Sovereign Synchronization (The Export Layer)
*   **Trigger:** `src/sovereign_sync.py` running during `aim push`.
*   **Function:** Translates the `engram.db` into deterministic `.jsonl` files in `archive/sync/`.
*   **Purpose:** Git-friendly, mergeable brain backups.
