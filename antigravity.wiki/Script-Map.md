# The Codebase Map (A.I.M. v2.1 — Antigravity Edition)

> **Last Updated:** 2026-04-01
> This document is the definitive map of every script in the A.I.M. exoskeleton. Use it to understand where logic lives before writing new code.

---

## 1. Core Source (`src/`)
*The pure Python engines driving the backend architecture.*

### 1.1 Continuity & Handoff
| Script | Role | Status |
|---|---|---|
| `handoff_pulse_generator.py` | **The Strategist.** Parses the exported `.md` transcript from `Downloads/`, then executes the dual-extraction pipeline: archives to `archive/raw/`, ingests into `history/session_engram.db`, extracts last 5 turns into `CURRENT_PULSE.md`, and formats `REINCARNATION_GAMEPLAN.md`. 100% zero-token. | ✅ Active |
| `history_scribe.py` | Converts raw JSON transcripts into clean Markdown session logs. Legacy pipeline — partially superseded by the Export-based handoff. | ⚠️ Legacy |

### 1.2 Engram DB & Retrieval
| Script | Role | Status |
|---|---|---|
| `bootstrap_brain.py` | **The Indexer.** Re-indexes `GEMINI.md`, `antigravity.wiki/`, and `core/` files into the `engram.db` on init. | ✅ Active |
| `retriever.py` | **The Search Engine.** Handles vector embeddings (Nomic) + FTS5 lexical search against `engram.db`. Powers `aim search`. | ✅ Active |
| `reasoning_utils.py` | **The Brain.** Unified multi-provider LLM routing engine. Every memory tier (T1-T5), the session summarizer, aim delegate, deep forensic restore, and aim CLI merge all call `generate_reasoning()` through this. Supports 7 backends: Google (OAuth + API Key), Ollama, Codex CLI, OpenAI-compatible, OpenRouter, and Anthropic. Routes per-tier via `CONFIG.json` `models.tiers.*` config. **Without this, the entire cascading memory engine is dead.** | ✅ Critical |

### 1.3 Background Services
| Script | Role | Status |
|---|---|---|
| `daemon.py` | **The Orchestrator.** Overarching background service loop that schedules memory refinement, heartbeat checks, and sync operations. | ✅ Active |
| `daemon_brain.py` | Continuous background process loop for the agent — manages hot-reload of context files. | ✅ Active |
| `heartbeat.py` | **Zero-token diagnostics.** Verifies integrity of the Engram DB, hooks, and sync folders. | ✅ Active |
| `maintenance.py` | **The Janitor.** Purges old logs, cleans workspace, manages retention policies. | ✅ Active |

### 1.4 [Cascading Memory](Feature-Cascading-Memory.md) Engine
| Script | Tier | Role |
|---|---|---|
| `memory_proposer.py` | Tier 2 | Distills raw hourly transcripts into structured Add/Remove deltas for Core Memory. |
| `daily_refiner.py` | Tier 3 | Consolidates hourly states into a single daily summary. |
| `weekly_consolidator.py` | Tier 4 | Compresses 7 days of daily summaries into high-level milestones. |
| `monthly_archivist.py` | Tier 5 | Final compression layer for long-term project architecture. |

### 1.5 Sync & Transport
| Script | Role | Status |
|---|---|---|
| `sovereign_sync.py` | **Outbound transport.** Converts SQLite tables into human-readable `.jsonl` files in `archive/sync/`. | ✅ Active |
| `back-populator.py` | **Inbound transport.** Rebuilds a corrupted SQLite database from `.jsonl` backup files. | ✅ Active |
| `config_utils.py` | **The Shared Config Loader.** Provides `CONFIG` dict and `AIM_ROOT` path to 14+ scripts across `src/`, `scripts/`, `hooks/`, and `plugins/`. Every script that reads `core/CONFIG.json` goes through this. | ✅ Critical |
| `memory_utils.py` | Helper functions for applying proposals to Core Memory blocks. | ✅ Active |

### 1.6 Plugins & Interfaces
| Script | Role | Status |
|---|---|---|
| `datajack_plugin.py` | Interface layer for [DataJack](The-DataJack-Protocol.md) cartridges. Contains `NullKnowledgeProvider` fallback. | ✅ Active |
| `mcp_server.py` | FastMCP-based Model Context Protocol server. Antigravity reads local files natively, so this is supplementary. | ⚠️ Legacy |

---

## 2. CLI Router & Scripts (`scripts/`)
*The command-line interface and utility scripts.*

### 2.1 Core CLI
| Script | CLI Command | Role | Status |
|---|---|---|---|
| `aim_cli.py` | `[ALIAS]` | **The Central Router.** Routes all `aim *` subcommands to their target scripts. ~40 KB, handles `search`, `map`, `sync`, `push`, `fix`, `bug`, `mail`, `chalkboard`, etc. | ✅ Active |
| `aim_init.py` | `[ALIAS] init` | Bootstraps a new A.I.M. deployment — scaffolds directories, indexes `GEMINI.md` into KIs, and wires the Engram DB. | ✅ Active |
| `aim_config.py` | `[ALIAS] tui` | Interactive TUI cockpit for editing `CONFIG.json` settings. | ✅ Active |
| `aim_push.py` | `[ALIAS] push` | GitOps push wrapper. Validates branch, prevents direct `main` pushes, enforces commit message format. | ✅ Active |
| `aim_crash.py` | `[ALIAS] crash` | Emergency recovery engine. Extracts signal from corrupted V8 heap crashes, rebuilds continuity files, syncs issue tracker. | ✅ Active |
| `aim_doctor.py` | `[ALIAS] doctor` | Environment validator. Checks dependencies, database integrity, and configuration health. | ✅ Active |
| `aim_router.py` | `[ALIAS] route` | Dynamic LLM routing configuration. Selects model providers based on task type. | ⚠️ Legacy |
| `aim_vault.py` | `[ALIAS] vault` | Secure credential storage via Python `keyring`. Manages API keys. | ⚠️ Legacy |
| `aim_delegate.py` | `[ALIAS] delegate` | Multi-agent task delegation using `concurrent.futures`. Calls `generate_reasoning()` per-task with tier-specific routing. Not currently wired in CLI but code is functional. | ✅ Active |
| `aim_batch_merge.py` | `[ALIAS] batch-merge` | Utility for merging multiple pull requests or memory deltas simultaneously. | ✅ Active |
| `aim_torrent.py` | `[ALIAS] torrent` | P2P [DataJack](The-DataJack-Protocol.md) daemon for sharing cartridges via `aria2c`. | ⚠️ Future |

### 2.2 Signal & Continuity
| Script | Role | Status |
|---|---|---|
| `extract_signal.py` | **The Harvester.** Contains `extract_signal()` (JSON), `extract_signal_from_txt()` (Antigravity overview.txt), `extract_signal_from_antigravity_steps()` (mid-session step scraping), `extract_latest_markdown_export()` (Downloads folder), and `parse_markdown_transcript()` (dialogue segmentation). | ✅ Active |
| `auto_export.py` | **UI Hook (Experimental).** Attempts `pywinauto`/`uiautomation` to auto-click the Export button. Fails on Antigravity due to stripped `aria-label` arrays. Falls back gracefully. | ⚠️ Blocked |
| `sync_issue_tracker.py` | **Dynamic Issue Sync.** Auto-detects current repo from `git remote`, pulls open issues, optionally merges cross-swarm hub issues. Writes to `continuity/ISSUE_TRACKER.md`. | ✅ Active |

### 2.3 Obsidian Bridge
| Script | Role | Status |
|---|---|---|
| `obsidian_sync.py` | **Outbound.** Mirrors A.I.M. memory files into a local Obsidian vault. | ✅ Active |
| `obsidian_pull.py` | **Inbound (`aim ingest`).** Pulls manual edits from the vault back into the workspace. | ✅ Active |

### 2.4 Analysis & Diagnostics
| Script | Role | Status |
|---|---|---|
| `analyze_fade.py` | Analyzes system prompt adherence decay over session length. Validates the 30% context fade thesis. | ✅ Active |
| `analyze_sessions.py` | Parses session transcripts for statistical analysis (turn count, token usage, etc.). | ✅ Active |
| `verify_order.py` | Validates that cascading memory tiers ran sequentially (T1→T2→T3). | ✅ Active |
| `telemetry_scrubber.py` | Privacy filter. Scrubs API keys, IP addresses, and PII from logs before archiving. | ✅ Active |
| `run_test_init.py` | Triggers a fast initialization process specifically for the test suite. | ✅ Active |

### 2.5 Migration & Recovery
| Script | Role | Status |
|---|---|---|
| `deep_forensic_restore.py` | Advanced database recovery when `back-populator` fails. | ✅ Active |
| `methodical_rebuild.py` | Clean-sweep script that wipes the database and memory folders, forces total rebuild from scratch. | ✅ Active |
| `total_reconstruction.py` | Extracts notes from messages matching a target date for historical reconstruction. | ✅ Active |
| `session_porter.py` | Moves or merges isolated session transcripts between branches or agents. | ✅ Active |
| `migrate_roadmap.py` | Utility to shift legacy roadmap files into the new markdown structure. | ⚠️ One-time |
| `scrape_github_issues.py` | Parses remote GitHub repo and downloads issue text into local ledger. | ✅ Active |
| `scrub_pivot_receipt.py` | One-time scrubber for migration pivot receipt JSON files. | ⚠️ One-time |

---

## 3. Hooks (`hooks/`)
*Background event-driven scripts that fire on session lifecycle events.*

| Script | Role | Status |
|---|---|---|
| `session_summarizer.py` | **Tier 1 Harvester.** Strips raw JSON noise and extracts the "Signal Skeleton" into `memory/hourly/`. | ✅ Active |
| `context_injector.py` | Injects critical context files (`GEMINI.md`, `HANDOFF.md`, etc.) into the agent's active context window. | ✅ Active |
| `cognitive_mantra.py` | Periodic self-reinforcement hook. Re-reads core directives to combat system prompt fade. | ✅ Active |
| `failsafe_context_snapshot.py` | Emergency snapshot of the current context state to disk if a crash is detected. | ✅ Active |

---

## 4. Skills (`skills/`)
*Discoverable agent skills with paired `SKILL.md` manifests.*

| Script | SKILL.md | Role |
|---|---|---|
| `advanced_memory_search.py` | ✅ | Deep search across memory tiers and the Engram DB with advanced filtering. |
| `export_datajack_cartridge.py` | ✅ | Exports indexed knowledge into portable `.engram` ZIP cartridges. |
| `list_recent_sessions.py` | ✅ | Lists recent session archives with metadata (date, size, turn count). |
| `propose_memory_commit.py` | ✅ | Proposes structured memory deltas (Add/Remove) for operator review. |

---

## 5. Plugins (`plugins/`)
*Modular extensions with their own internal logic.*

| Plugin | Contents | Role |
|---|---|---|
| `plugins/datajack/` | `forensic_utils.py` | SQLite database wrapper. Manages `INSERT`/`SELECT` for the Engram DB. |
| `plugins/run_skill/` | `run.py`, `SKILL.md` | Skill execution engine. Discovers and runs scripts from `skills/`. |
| `plugins/search_engram/` | `SKILL.md` | Skill manifest for searching the Engram DB. |

### 5.1 DataJack Source Plugins (`src/plugins/datajack/`)

| Script | Role |
|---|---|
| `aim_bake.py` | Compiles a directory of text/markdown files into a portable `.engram` ZIP cartridge. |
| `forensic_utils.py` | Full SQLite database wrapper. All `INSERT`, `SELECT`, vector search, and FTS5 queries. (12 KB — the largest single utility.) |

---

## 6. Benchmarks (`scripts/benchmarks/`)
*Automated, repeatable testing harnesses.*

| Script | Role |
|---|---|
| `setup_environments.sh` | Creates `django_control` and `django_matrix` boilerplate folders for A/B testing. |
| `setup_standard_environments.sh` | Simplified environment scaffolding for standard benchmarks. |
| `calculate_economics.py` | Parses resulting transcripts to calculate exact token usage and API costs. |
| `recover_json_logs.py` | Extracts logs from benchmark folders for proof archival. |
| `run_amnesia_killer.py` | Harness for the Long-Horizon Memory Test. |
| `run_vibe_killer.py` | Harness for the 60-Turn Vibe Coding Trap Test. |

---

## 7. Workflows (`.agents/workflows/`)
*Antigravity-native slash command definitions.*

| Workflow | Trigger | Role |
|---|---|---|
| `init.md` | `/init` | Initializes agent brain by ingesting `GEMINI.md` into local KI database. |
| `reincarnate.md` | `/reincarnate <Intent>` | Triggers the mandatory Export prompt → zero-token Python dual-extraction pipeline → self-termination directive. |

---

## 8. Configuration (`core/`)

| File | Role |
|---|---|
| `CONFIG.json` | Central configuration. Paths, model settings, `hub_repo` for cross-swarm sync, feature flags. |
| `MEMORY.md` | Live project state memory. Updated by the cascading memory engine. |
| `OPERATOR.md` | Operator identity and preferences. |
| `OPERATOR_PROFILE.md` | Extended operator profile with technical background and communication style. |

---

## 9. Continuity (`continuity/`)

| File | Role |
|---|---|
| `REINCARNATION_GAMEPLAN.md` | The "Will" — 3-step executive directive for the next agent. Generated by `handoff_pulse_generator.py`. |
| `CURRENT_PULSE.md` | The "Edge" — last 5 conversational turns from the previous session. |
| `LAST_SESSION_FLIGHT_RECORDER.md` | Full exported transcript of the previous session. Forensic archive. |
| `ISSUE_TRACKER.md` | Auto-synced ledger of open GitHub issues from current repo + hub. Generated by `sync_issue_tracker.py`. |
| `README.md` | Documents the continuity folder structure. |