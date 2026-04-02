# The Codebase Map (aim-antigravity OS)

This document is the literal map of every internal script running the A.I.M. exoskeleton inside Antigravity. It explains where business logic lives, and explicitly calls out portions of the architecture that were orphaned or decapitated during the Windows migration.

---

## 1. Core Source (`src/`)
*The pure Python engines driving the backend architecture.*

*   **`bootstrap_brain.py`**: The initialization engine. Re-indexes `GEMINI.md`, `antigravity.wiki/`, and `core/` into `engram.db`.
*   **`config_utils.py`**: The single source of truth for loading, validating, and auto-repairing `core/CONFIG.json` paths. *(Note: Contains Linux root traversal bugs on Windows).*
*   **`daemon.py` & `daemon_brain.py`**: The Tier 5 Autonomic background service orchestrators. *(Note: Currently comatose on Windows due to legacy `nohup` calls).*
*   **`handoff_pulse_generator.py`**: The engine that distills active IDE sessions into `CURRENT_PULSE.md` and generates the `LAST_SESSION_FLIGHT_RECORDER.md` history during `/reincarnate`.
*   **`heartbeat.py`**: Zero-token diagnostic tool. Verifies the integrity of the Engram DB, hooks, and sync folders.
*   **`mcp_server.py`**: The FastMCP server, exposing the Engram DB natively to the Antigravity agent tool suite.
*   **`reasoning_utils.py`**: The universal LLM client. Dynamically routes API calls based on the Tiers defined in `CONFIG.json`.
*   **`retriever.py`**: The search engine. Handles vector embeddings (Nomic) and lexical search (FTS5) against `archive/engram.db`.
*   **`sovereign_sync.py` / `back-populator.py`**: The bi-directional GitOps serialization layer translating SQLite to `.jsonl` for version control.

### 1.1 The Cascading Memory Engine (Tier 5 Organs)
*   **`memory_proposer.py`** [Tier 2]: Distills raw hourly transcripts into structured Add/Remove deltas for Core Memory.
*   **`daily_refiner.py`** [Tier 3]: Consolidates the hourly states into a single daily summary.
*   **`weekly_consolidator.py`** [Tier 4]: Compresses 7 days of daily summaries into high-level milestones.
*   **`monthly_archivist.py`** [Tier 5]: The final compression layer for long-term project architecture.

### 1.2 DataJack Plugins (`src/plugins/datajack/`)
> 🔴 **STATUS: DECAPITATED.** The critical injection script `aim_exchange.py` was lost during the OS migration.
*   **`aim_bake.py`**: Compiles a directory of files into a portable `.engram` ZIP cartridge.
*   **`forensic_utils.py`**: The SQLite database wrapper. Manages all `INSERT` and `SELECT` queries for the Engram DB.

---

## 2. CLI Router & Legacy Scripts (`scripts/`)
*The front-end pipeline. Much of this is being sunset in favor of `.agents/workflows/`.*

### 🟢 Active Components
*   **`aim_cli.py`**: The central cross-platform dispatcher.
*   **`aim_push.sh` / `aim_push.ps1`**: The GitOps validation wrapper. Enforces atomic push cycles.
*   **`obsidian_sync.py` & `obsidian_pull.py`**: The bi-directional Sovereign Mirror connecting A.I.M. to Obsidian local Vaults.
*   **`sync_issue_tracker.py`**: The local synchronization engine for `ISSUE_TRACKER.md`.

### 🟡 Orphaned / Deprecated Components (To Be Sunset)
> The following scripts were designed for standalone terminal operation and are now superseded by File-Based IDE Workflows.
*   **`aim_config.py`**: The 18K monolithic TUI cockpit. Superseded by `/sync` workflows and direct `CONFIG.json` editing.
*   **`aim_init.py`**: The 24K setup wizard. Superseded by `/init` IDE workflows.
*   **`aim_reincarnate.py` / `poc_tmux.py`**: Legacy Linux Terminal Splicing tools. Superseded by manual Export and `/reincarnate` script.
*   **`extract_signal.py`**: Pure terminal JSON scraper. Less relevant now that the IDE natively manages context.

---

## 3. Benchmarks (`scripts/benchmarks/`)
*Automated, repeatable testing harnesses for the platform.*

*   **`calculate_economics.py`**: Parses resulting outputs to calculate exact token usage and API costs.
*   **`run_amnesia_killer.py`**: The harness for the Long-Horizon Memory Test.
*   **`run_vibe_killer.py`**: The harness for the 60-Turn Vibe Coding Trap Test.