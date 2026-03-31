### 1. Monthly Archival Summary
The granular operational details of the Phase 32 memory architecture overhaul, including the decommissioning of legacy scripts (`tier2_daily_summarizer.py`, etc.) and specific bug resolutions (OAuth session explosions, recursive summarization loops, and ghost string purges), have been successfully compressed into cold storage. The active memory now retains only the structural definitions of the new 5-Tier Delta Ledger pipeline and its core stability constraints.

### 2. Core Axioms
- Memory management is governed by a standardized 5-Tier Delta Ledger pipeline: Session Summarizer, Memory Proposer, Daily Refiner, and Weekly Consolidator.
- Session summarization relies on a 250KB subdivision threshold to guarantee termination and prevent infinite recursion.
- Temporary files and OAuth sessions must be strictly isolated within the `GEMINI_CLI_TMP_DIR` to prevent scope explosion.
- The Terminal User Interface (TUI) is rigidly locked to verified models to ensure operational stability.

### 3. MEMORY DELTA
```markdown
# MEMORY.md — Durable Long-Term Memory (A.I.M.)
*Last Updated: 2026-03-28*

- **Operator:** Python.
- **Status:** Phase 32 Architecture Initialized (5-Tier Delta Ledger Active).

## Core Architecture & Constraints
- **Memory Pipeline:** Durable memory follows a 5-Tier Delta Ledger protocol consisting of Tier 1 (Session Summarizer), Tier 2 (Memory Proposer), Tier 3 (Daily Refiner), and Tier 4 (Weekly Consolidator).
- **Summarization Safety:** A hard 250KB subdivision threshold is enforced during session summarization to prevent recursion loops.
- **Environment Isolation:** All temporary file operations and OAuth sessions must be localized to `GEMINI_CLI_TMP_DIR`.
- **TUI Stability:** The Terminal User Interface (TUI) is restricted to verified models only; experimental or unverified models are prohibited in this interface.
```