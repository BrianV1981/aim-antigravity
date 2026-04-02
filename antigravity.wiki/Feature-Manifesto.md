# The Pragmatic Approach: A.I.M. Feature Manifesto

This document provides a comprehensive index of every feature built into the A.I.M. (Actual Intelligent Memory) Operating System, explicitly tracking the Antigravity integration and the sunset/decapitated features from the 2026 Windows Migration.

## The Core Philosophy: Defeating "Needle in a Haystack"
The AI industry is currently obsessed with the "Needle in a Haystack" (NIAH) benchmark—brute-forcing 1-million or 2-million token context windows.

**This is a fundamentally flawed architecture for memory.** It treats data retrieval as a neural network problem when it is actually a solved *data engineering* problem. 

A.I.M. takes a pragmatic, engineering-first approach: Deterministic Python scripts compress semantic Markdown and inject it into a highly structured `engram.db` SQLite system. When the A.I.M. agent needs the "needle," it executes a Hybrid RAG query. **It costs zero inference tokens, runs instantly, and never hallucinates context.** 

---

## 1. The Core Operating System (Exoskeleton)

*   **The Slash Workflow Engine (`.agents/workflows/`)**
    *   *What it is:* The replacement for monolithic terminal Python scripts. File-based Markdown instructions that the IDE Agent executes natively.
    *   *Why it is important:* It integrates cleanly into the Antigravity environment, replacing legacy Linux `aim_init.py` and `aim_config.py` setups.

*   **The Cockpit / TUI (`aim_config.py`) [🟡 SUNSET]**
    *   *Status:* Retired. The rich interactive terminal UI was structurally incompatible with IDE agent paradigms. Configuration now lives natively in Tier 3 Knowledge Items (KIs).

*   **The Background Daemon (`daemon.py`) [🔴 DECAPITATED]**
    *   *Status:* Comatose. The persistent background process relied heavily on Linux `nohup` execution and daemon polling loops, which broke during the Windows migration (Issue #49). Transitioning to IDE-native event hooks.

## 2. The Cascading Memory Engine (Tier 5 Autonomic)

*   **Tier 1: IDE Extraction Hooks (`session_summarizer.py`)**
    *   *What it is:* Background extraction of chat narratives.
    *   *Status:* Transitioning from native Gemini CLI terminal scrapers to Antigravity IDE JSON ingestion files.

*   **Tier 2: Memory Proposer (`memory_proposer.py`)**
    *   *What it is:* Analyzes the hourly summaries and proposes structured delta updates to the long-term `MEMORY.md`.

*   **Tier 3 & 4: Daily & Weekly Consolidators (`daily_refiner.py`, `weekly_consolidator.py`)**
    *   *What it is:* Compresses a 3-day struggle with a CORS error into a single rule: "Always set CORS headers in middleware."

*   **Tier 5: Monthly Archivist (`monthly_archivist.py`)**
    *   *What it is:* Archives stable architecture into dense, factual engram axioms.

## 3. The Engram Database & DataJack

*   **Hybrid RAG Retrieval (`retriever.py`)**
    *   *What it is:* A local SQLite database using localized Nomic embeddings and FTS5 Lexical matching for flawless recall without exposing keys or code to external vector providers.

*   **The DataJack Foundry (`aim_exchange.py`) [🔴 DECAPITATED]**
    *   *Status:* Missing. The critical mechanism for exporting and decrypting `.engram` cartridges into local databases was lost during the OS migration. Tracked in Issue #42.

## 4. Continuity & Failsafes

*   **The File-Based Checkpoint (`HANDOFF.md`)**
    *   *What it is:* Instead of injecting JSON context payloads directly into the hidden terminal payload, Antigravity physically writes the `HANDOFF.md` to the workspace root.
    *   *Why it is important:* It acts as a Pre-Flight Lockout. The agent cannot act without visually processing its Commander's Intent and the last conversation turns, enforcing Epistemic Certainty.

*   **The Handoff Pulse Generator (`/reincarnate`)**
    *   *What it is:* Replaces the legacy `tmux` agent-splicing script to cleanly extract context from a bloated session, generate a Gameplan, and move to a clean workspace window.

## 5. Security & GitOps Deployment

*   **The GitOps Bridge (`aim_push` wrapper)**
    *   *What it is:* A strict workflow that physically prevents the agent from writing code on the `main` branch. It enforces `aim-antigravity bug`, `aim-antigravity fix <id>`, and atomic deployments.
    *   *Why it is important:* Autonomous agents will destroy codebases if left unconstrained. This ensures every change is isolated and cleanly merged into the ledger.

*   **Decoupled Sovereign Sync (`sovereign_sync.py`)**
    *   *What it is:* Translates SQLite into plain-text JSONL files so memory can be committed to GitHub and synced across machines.

## 6. Integrations & Extensions

*   **The Universal MCP Server (`mcp_server.py`)**
    *   *What it is:* A Model Context Protocol server that natively exposes the A.I.M. Engram database as a local tool for IDE agents.

*   **The Obsidan Bridge (`obsidian_sync.py`)**
    *   *What it is:* Synchronizes local A.I.M. JSONL data directly into a local Obsidian vault.