# A.I.M. Technical Handbook (Master Schema)

This document is the definitive architectural map for the A.I.M. platform. It defines the modular components of the brain and the protocols that ensure continuity and sovereignty within the Google Antigravity ecosystem.

---

## SECTION 1: THE ROOT ARCHITECTURE

### 1.1 `GEMINI.md` (The Index & Soul)
- **Role:** Lean Orchestrator & Cognitive Baseline.
- **Function:** It is an explicit **Table of Contents**. Instead of holding massive walls of text, it directs the agent to query its native Knowledge Items (KIs) or the background **Engram DB** for technical policies.
- **Cognitive Guardrails:** It permanently encodes the Operator's chosen execution mode (Autonomous vs Cautious), GitOps workflow, and the "Token-Saver" conciseness mandate.

### 1.2 The Initialization Workflow (`/init`)
- **Function:** A dynamic, decoupled scaffolding wizard.
- **Mechanism:** Typing `/init` into the Antigravity chat automatically ingests the `GEMINI.md` file and converts it into the `aim_master_directives` Knowledge Item.
- **Configuration Hot-Swapping:** To adjust model configurations, personalities, or paths, the Operator simply uses Antigravity's native GUI settings or edits their KI directly (replacing the legacy `aim tui` interface).

---

## SECTION 2: THE ENGRAM DB (SUBCONSCIOUS)
The core of A.I.M.'s deep-memory structure lives in an optional local SQLite database (`archive/engram.db`). It uses a **[Hybrid RAG](Feature-Hybrid-RAG.md)** engine, blending dense Vector Embeddings (Cosine Similarity) with FTS5 Lexical matching.

### 2.1 The Pre-Born Brain
During complex initializations, A.I.M. indexes this Handbook and core project directives. This provides the agent with "Day Zero" technical knowledge.

### 2.2 Foundry Ingestion
The `foundry/` folder is a dedicated intake zone. Any technical references dropped here are recursively indexed as `expert_knowledge`.

### 2.3 The Cartridge Exchange
Expertise is portable. A.I.M. can export its indexed knowledge into compressed `.engram` packs, allowing you to share a pre-trained "Python Expert" brain with other machines without re-indexing.

---

## SECTION 3: THE [CASCADING MEMORY](Feature-Cascading-Memory.md) ENGINE (CONSCIOUSNESS)
If the optional background Python daemons are enabled, memory is refined through a tiered, self-cleaning hierarchy to prevent knowledge decay and file bloat.

### 3.1 Tier 1: The Harvester (`hooks/session_summarizer.py`)
- **Function (The Python Sieve):** Uses a 100% free, zero-token Python script to strip raw JSON tool noise and extract a lean "Signal Skeleton."
- **Output:** A concise technical narrative saved to `memory/hourly/`.

### 3.2 Tier 2: The Proposer (`src/memory_proposer.py`)
- **Function:** Squashes the hourly logs into structured Add/Remove deltas for proposals.

### 3.3 Tier 3: Daily Distillation (`src/daily_refiner.py`)
- **Function:** Consolidates multiple Tier 2 memory proposals into a single Daily State.

### 3.4 Tier 4: Weekly Arc (`src/weekly_consolidator.py`)
- **Function:** Synthesizes 7 Daily Proposals into a condensed **Weekly Proposal**.

### 3.5 Tier 5: The Apex Proposer (`src/monthly_archivist.py`)
- **Function:** Synthesizes the Weekly Proposals into definitive architecture axioms and archives stale context.

---

## SECTION 4: SAFETY & SOVEREIGNTY

### 4.1 The Obsidian Bridge
- **Role:** Sovereign Mirror.
- **Function:** Mirroring of Daily Logs, Core Memory, and **Raw Transcripts** to an external vault for 100% offline recovery native to human operators.

---

## SECTION 5: SYSTEM MAINTENANCE & UPDATES

### 5.1 The Sovereign Update
- **Role:** High-Fidelity Sync.
- **Function:** Because A.I.M. relies on GitOps, updates are performed via standard `git pull origin main` commands.
- **Data Preservation (Safe Update):** Performing a standard pull natively protects your local `aim_master_directives` KIs and `.ignore` files.

---

## SECTION 6: THE HYBRID SOUL PROTOCOL

A.I.M. maintains technical continuity through a dual-mode ingestion engine within `src/bootstrap_brain.py`.

### 6.1 Foundation Sync (Active Instructions)
- **Scope:** `GEMINI.md`, `core/MEMORY.md`, and all files in `antigravity.wiki/`.
- **Logic:** These files are **Synchronized**. 
- **The Self-Healing Trigger (JIT):** Every time a new session starts, the framework checks file modification timestamps against the Engram DB.

### 6.2 Foundry Ingestion (Permanent Knowledge)
- **Scope:** Everything dropped into the `foundry/`.
- **Behavior:** Once a file is indexed from the Foundry, it is **Permanently Persistent** in the Engram DB. The source files on disk can be safely deleted to keep the workspace lean.

---

## SECTION 7: UNIVERSAL SOVEREIGNTY

### 7.1 The Native GUI Cockpit
- **Role:** Centralized configuration for all reasoning models is handled directly by the Antigravity IDE UI, completely deprecating manual `CONFIG.json` CLI terminal wizards.

### 7.2 Native File-System Hooks
- **Role:** IDE Integration.
- **Function:** Antigravity natively reads the local directory structure, bypassing any need to run standalone MCP (Model Context Protocol) servers.

### 7.3 The Universal Skills Framework
- **Role:** Standardized Agentic Tooling.
- **Function:** Antigravity inherently supports `.agents/skills/` directories, allowing the Operator to drop executable scripts alongside a `SKILL.md` manifest for the agent to autonomously discover.

---

## SECTION 8: DEVELOPMENT LIFECYCLE (THE PHASE PROTOCOL)
### 8.1 The Branching Strategy
1.  **Ideation & Planning:** The roadmap is updated on `main`.
2.  **Execution Branch:** A new branch is cut (e.g., `dev-phase-21`) using Antigravity's Git integration.
3.  **The Archive Cut:** Before merging.
4.  **The Merge:** The `dev-` branch is merged into `main`.

---

## SECTION 9: TEST-DRIVEN DEVELOPMENT (TDD) POLICY
### 9.1 The Mandate
Every functional change **MUST** be governed by the TDD lifecycle. No code enters the source directory without a verification script that is autonomously executed by the agent until green.

---

## SECTION 10: GIT-OPS & SEMANTIC RELEASE (THE PUBLIC LEDGER)

### 10.1 Issue-Driven Development
- A.I.M. enforces atomic deployments. Agents are forbidden from generic commits. Every single change must be formally tied to an Issue or a tracked goal, executed on an isolated branch within Antigravity, and proven via TDD before being merged to main.
