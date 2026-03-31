# A.I.M. Technical Handbook (Master Schema)

This document is the definitive architectural map for the A.I.M. platform. It defines the modular components of the brain and the protocols that ensure continuity and sovereignty.

---

## SECTION 1: THE ROOT ARCHITECTURE

### 1.1 `GEMINI.md` (The Index & Soul)
- **Role:** Lean Orchestrator & Cognitive Baseline.
- **Function:** It is an explicit **Table of Contents**. Instead of holding massive walls of text, it directs the agent to query the **Engram DB** for technical policies.
- **Cognitive Guardrails:** It permanently encodes the Operator's chosen grammar level, execution mode (Autonomous vs Cautious), and the "Token-Saver" conciseness mandate.

### 1.2 The Initialization Overhaul (`aim init`)
- **Function:** A dynamic, decoupled scaffolding wizard.
- **Clean Sweep:** Allows the user to independently wipe Project Docs (Roadmap, Changelog) and/or the AI Brain (Engram DB) when repurposing the A.I.M. template for a new codebase.
- **The TUI Updater:** If behavioral questions are skipped during installation, the Operator can hot-swap the AI's personality and rules dynamically using the `aim tui` cockpit.

---

## SECTION 2: THE ENGRAM DB (SUBCONSCIOUS)
The core of A.I.M.'s memory lives in a local SQLite database (`archive/engram.db`). It uses a **Hybrid RAG** engine, blending dense Vector Embeddings (Cosine Similarity) with FTS5 Lexical matching (BM25) to provide flawless recall of abstract concepts and exact variable names.

### 2.1 The Pre-Born Brain
During initialization, A.I.M. indexes this Handbook and core project directives. This provides the agent with "Day Zero" technical knowledge.

### 2.2 Foundry Ingestion
The `foundry/` folder is a dedicated intake zone. Any technical references dropped here are recursively indexed as `expert_knowledge`.

### 2.3 The Cartridge Exchange (`aim exchange`)
Expertise is portable. A.I.M. can `export` its indexed knowledge into compressed `.aim` packs, allowing you to share a pre-trained "Python Expert" or "Solana Architect" brain with other machines without re-indexing.

---

## SECTION 3: THE CASCADING MEMORY ENGINE (CONSCIOUSNESS)
Memory is refined through a tiered, self-cleaning hierarchy to prevent knowledge decay and file bloat.

### 3.1 Tier 1: The Harvester (`hooks/session_summarizer.py`)
- **Trigger:** Automated via the `failsafe_context_snapshot.py` hook when new technical delta is detected.
- **Function (The Python Sieve):** Uses a 100% free, zero-token Python script to strip raw JSON tool noise and extract a lean "Signal Skeleton."
- **Output:** A concise technical narrative saved to `memory/hourly/`.

### 3.2 Tier 2: The Proposer (`src/memory_proposer.py`)
- **Trigger:** Triggered via `aim memory`.
- **Function:** Squashes the hourly logs into structured Add/Remove deltas for proposals.

### 3.3 Tier 3: Daily Distillation (`src/daily_refiner.py`)
- **Trigger:** Triggered via `aim memory`.
- **Function:** Consolidates multiple Tier 2 memory proposals into a single Daily State.

### 3.4 Tier 4: Weekly Arc (`src/weekly_consolidator.py`)
- **Trigger:** Triggered via `aim memory`.
- **Function:** Synthesizes 7 Daily Proposals into a condensed **Weekly Proposal**.

### 3.5 Tier 5: The Apex Proposer (`src/monthly_archivist.py`)
- **Trigger:** Triggered via `aim memory`.
- **Function:** Synthesizes the Weekly Proposals into definitive architecture axioms and archives stale context.

### 3.6 The Rolling Proposal (`aim commit`)
You can type `aim commit` at *any time*. The command grabs the *most recent, highest-tier proposal available*, applies it to your `core/MEMORY.md`, and instantly deletes all underlying scaffolding.

---

## SECTION 4: SAFETY & SOVEREIGNTY

### 4.1 The Obsidian Bridge (`scripts/obsidian_sync.py`)
- **Role:** Sovereign Mirror.
- **Function:** Mirroring of Daily Logs, Core Memory, and **Raw JSON Transcripts** to an external vault for 100% recovery.

---

## SECTION 5: SYSTEM MAINTENANCE & UPDATES

### 5.1 The Sovereign Update (`aim update`)
- **Role:** High-Fidelity Sync.
- **Function:** Automates the lifecycle of keeping A.I.M. current.
- **Protocol:**
  1. **Source Sync:** Performs a `git pull origin main` to fetch the latest TUI, scripts, and engine logic.
  2. **Hook Refresh:** Re-registers all system hooks to ensure the local Gemini CLI is utilizing the latest architectural guardrails.
  3. **Data Preservation (Safe Update):** The update logic explicitly protects your **Personality Trinity** (`GEMINI.md`, `USER.md`, `MEMORY.md`).

---

## SECTION 6: THE HYBRID SOUL PROTOCOL

A.I.M. maintains technical continuity through a dual-mode ingestion engine within `src/bootstrap_brain.py`.

### 6.1 Foundation Sync (Active Instructions)
- **Scope:** `GEMINI.md`, `core/MEMORY.md`, and all files in `aim.wiki/`.
- **Logic:** These files are **Synchronized**. 
- **The Self-Healing Trigger (JIT):** Every time a new session starts, the `context_injector.py` hook explicitly checks the file modification timestamps against the Engram DB. If it detects that a human operator manually edited `MEMORY.md` or a docs file, it instantly spins up a silent background thread to overwrite the old engrams.

### 6.2 Foundry Ingestion (Permanent Knowledge)
- **Scope:** Everything dropped into the `foundry/` folder.
- **Logic:** This is an **Onramp**.
- **Behavior:** Once a file is indexed from the Foundry, it is **Permanently Persistent** in the Engram DB. The source files on disk can be safely deleted to keep the workspace lean.

### 6.3 Amnesia Protection
- **0-Byte Shield:** The bootstrap engine automatically skips empty or 0-byte files. This prevents accidental "Technical Amnesia".

---

## SECTION 7: UNIVERSAL SOVEREIGNTY (MCP & SYNC)

### 7.1 The Universal Hub (Cockpit)
- **Role:** Centralized configuration for all reasoning models via `aim tui`.

### 7.2 Model Context Protocol (MCP) Server
- **Role:** IDE Integration.
- **Function:** A built-in `fastmcp` server (`src/mcp_server.py`) exposes the A.I.M. Engram DB as a standard tool for Cursor/Claude Desktop.

### 7.3 Sovereign Sync (Git Synchronization)
- **Role:** Binary Conflict Resolution.
- **Function:** SQLite databases (`engram.db`) cause binary merge conflicts in Git. A.I.M. translates the database into deterministic `.jsonl` files (`archive/sync/`) during `aim push`.

### 7.4 The "Index-First" Retrieval Protocol
- **Role:** Token-Efficient Discovery.
- **Command:** `aim map`

### 7.5 The Universal Skills Framework
- **Role:** CLI-Agnostic Action Execution.
- **Function:** The `skills/` directory allows the Operator to drop executable scripts alongside a `SKILL.md` manifest.

---

## SECTION 8: DEVELOPMENT LIFECYCLE (THE PHASE PROTOCOL)
### 8.1 The Branching Strategy
1.  **Ideation & Planning:** The roadmap is updated on `main`.
2.  **Execution Branch:** A new branch is cut (e.g., `dev-phase-21`).
3.  **The Archive Cut:** Before merging, the *current* state of `main` is cloned to a timestamped archive branch.
4.  **The Merge:** The `dev-` branch is merged into `main`.

---

## SECTION 9: TEST-DRIVEN DEVELOPMENT (TDD) POLICY
### 9.1 The Mandate
Every functional change **MUST** be governed by the TDD lifecycle. No code enters the `src/` directory without a verification script.

---

## SECTION 10: GIT-OPS & SEMANTIC RELEASE (THE PUBLIC LEDGER)
### 10.1 Issue-Driven Development (`aim bug` & `aim fix`)
- **`aim bug <description>`:** Automatically creates a structured GitHub Issue via the `gh` CLI.
- **`aim fix <id>`:** Automatically checks out a clean Git branch (`fix/issue-<id>`).

### 10.3 The Atomic Deployment Rule
- **The Rule:** AI agents are strictly forbidden from executing raw `git commit` or `git push` commands. Every single bug fix must be deployed immediately using `aim push`.

### 10.4 Conventional Commits (`aim push`)
The `aim push` command explicitly parses prefixes (Feature, Fix, Docs) to calculate version numbers and generate changelogs.
