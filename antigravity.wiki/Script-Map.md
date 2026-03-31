# The Codebase Map (A.I.M. v1.38.1)

This document is the literal map of every internal script running the A.I.M. OS. Use it to understand where business logic lives.

---

## 1. Core Source (`src/`)
*The pure Python engines driving the backend architecture.*

*   **`bootstrap_brain.py`**: The initialization engine. Re-indexes `GEMINI.md`, `aim.wiki/`, and `core/` into the `engram.db`.
*   **`config_utils.py`**: The single source of truth for loading, validating, and auto-repairing `core/CONFIG.json` paths.
*   **`daemon_brain.py`**: The continuous background process loop for the agent.
*   **`daemon.py`**: The overarching background service orchestrator.
*   **`datajack_plugin.py`**: The interface layer for DataJack Swarm Cartridges.
*   **`handoff_pulse_generator.py`**: The engine that distills the current terminal JSON into `CURRENT_PULSE.md` and generates the `LAST_SESSION_FLIGHT_RECORDER.md` full history.
*   **`heartbeat.py`**: The zero-token diagnostic tool. Verifies the integrity of the Engram DB, hooks, and sync folders.
*   **`maintenance.py`**: The automated janitor. Purges old logs, cleans the workspace, and manages retention policies.
*   **`mcp_server.py`**: The Model Context Protocol server, enabling external IDEs (Cursor/VS Code) to query the Engram DB and read memories.
*   **`memory_utils.py`**: Helper functions for applying proposals to the Core Memory block.
*   **`reasoning_utils.py`**: The universal LLM client. Dynamically routes API calls based on the Tiers defined in `CONFIG.json` (Google vs Anthropic vs Local).
*   **`retriever.py`**: The search engine. Handles vector embeddings (Nomic) and lexical search (FTS5) against `archive/engram.db`.
*   **`sovereign_sync.py`**: The outbound transport layer. Converts the SQLite tables into human-readable `.jsonl` files in `archive/sync/`.
*   **`back-populator.py`**: The inbound transport layer. Rebuilds a corrupted or empty SQLite database natively from the `.jsonl` backup files.

### 1.1 The Cascading Memory Engine
*   **`memory_proposer.py`** [Tier 2]: Distills raw hourly transcripts into structured Add/Remove deltas for Core Memory.
*   **`daily_refiner.py`** [Tier 3]: Consolidates the hourly states into a single daily summary.
*   **`weekly_consolidator.py`** [Tier 4]: Compresses 7 days of daily summaries into high-level milestones.
*   **`monthly_archivist.py`** [Tier 5]: The final compression layer for long-term project architecture.

### 1.2 DataJack Plugins (`src/plugins/datajack/`)
*   **`aim_bake.py`**: Compiles a directory of text/markdown files into a portable `.engram` ZIP cartridge.
*   **`aim_exchange.py`**: Handles the ingestion and decryption of `.engram` files back into the local database.
*   **`forensic_utils.py`**: The SQLite database wrapper. Manages all `INSERT` and `SELECT` queries for the Engram DB.

---

## 2. CLI Router & Scripts (`scripts/`)
*The front-end commands accessible via the `aim` global alias.*

*   **`aim_cli.py`**: The central router. Parses `aim search`, `aim commit`, `aim update`, etc., and dispatches the corresponding script.
*   **`aim_config.py`**: The Interactive TUI (Cockpit). Modifies `CONFIG.json` using the `questionary` library.
*   **`aim_crash.py`**: The recovery script. Safely extracts the signal from a corrupted V8 heap crash without losing context.
*   **`aim_delegate.py`**: The sub-agent spin-up protocol for distributed background processing.
*   **`aim_doctor.py`**: Validates the operating environment, dependencies, and configuration.
*   **`aim_init.py`**: The setup wizard. Executed upon first repository installation to build the database and hooks.
*   **`aim_reincarnate.py`**: The Context Pruning teleport script. Asks for a Gameplan, spawns a new Tmux agent, and assassinates the bloated one.
*   **`aim_router.py`**: Handles dynamic routing algorithms.
*   **`aim_torrent.py`**: The P2P DataJack Swarm daemon for sharing cartridges.
*   **`aim_vault.py`**: The encrypted local key-store for holding API keys securely without putting them in plaintext configs.
*   **`aim_push.sh`**: The GitOps validation wrapper. Prevents direct pushes to `main` and enforces the branch/issue protocol.
*   **`aim_batch_merge.py`**: Utility for merging multiple pull requests or memory deltas simultaneously.
*   **`deep_forensic_restore.py`**: Advanced database recovery script used if `back-populator` fails.
*   **`extract_signal.py`**: The Zero-Token Scribe. Uses pure Python logic to strip 85% of JSON noise from native CLI transcripts.
*   **`methodical_rebuild.py`**: A clean-sweep script that wipes the database and memory folders, forcing a total rebuild from scratch.
*   **`migrate_roadmap.py`**: Utility to shift legacy roadmap files into the new markdown structure.
*   **`obsidian_sync.py`**: The Outbound Obsidian Bridge. Mirrors A.I.M.'s memory files into a local Obsidian Vault.
*   **`obsidian_pull.py`**: The Inbound Obsidian Bridge (`aim ingest`). Pulls manual edits from the vault back into the workspace.
*   **`poc_tmux.py`**: A proof-of-concept for the "Phantom Keyboard" (terminal multiplexing integration).
*   **`run_test_init.py`**: Triggers a fast initialization process specifically for the test suite.
*   **`scrape_github_issues.py`**: Parses the remote GitHub repo and downloads issue text into the local ledger.
*   **`session_porter.py`**: Moves or merges isolated session transcripts between branches or agents.
*   **`sync_issue_tracker.py`**: The local synchronization engine for `ISSUE_TRACKER.md`.
*   **`telemetry_scrubber.py`**: Privacy filter. Scrubs API keys and IP addresses from logs before they are synced to the archive.
*   **`total_reconstruction.py`**: *WARNING: Currently hijacked by an unrelated Arma 3 web scraper (See Ticket #187).*
*   **`verify_order.py`**: Ensures the cascading memory logic ran sequentially (Tier 1 -> Tier 2 -> Tier 3).

---

## 3. Benchmarks (`scripts/benchmarks/`)
*Automated, repeatable testing harnesses for the platform.*

*   **`setup_environments.sh`**: Creates the `django_control` and `django_matrix` boilerplate folders for A/B testing.
*   **`calculate_economics.py`**: Parses the resulting JSON transcripts to calculate exact token usage and API costs.
*   **`recover_json_logs.py`**: Extracts the `.gemini/tmp/` logs from the benchmark folders so they can be committed to the repo for proof.
*   **`run_amnesia_killer.py`**: The harness for the Long-Horizon Memory Test.
*   **`run_vibe_killer.py`**: The harness for the 60-Turn Vibe Coding Trap Test.