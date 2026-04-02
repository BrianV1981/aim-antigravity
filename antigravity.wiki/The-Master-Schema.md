# A.I.M. Technical Handbook (Master Schema)

This document is the definitive architectural map for the A.I.M. platform operating within the Antigravity IDE environment. It defines the modular components of the brain and the protocols that ensure continuity and sovereignty.

---

## SECTION 1: THE ROOT ARCHITECTURE

### 1.1 `GEMINI.md` (The Core Index)
- **Role:** Lean Orchestrator & Cognitive Baseline.
- **Function:** It is an explicit **Table of Contents**. Instead of holding massive walls of text, it directs the agent to query the **Engram DB** or local Knowledge Items (KIs) for technical policies.
- **Cognitive Guardrails:** It permanently encodes the Operator's rules, the GitOps mandate, and the "Token-Saver" conciseness mandate.

### 1.2 The Initialization & Calibration Hooks (`/init` & `/sync`)
- **Function:** Dynamic, file-based Slash Workflows within the IDE.
- **`/init`:** Bootstraps a fresh project, running health checks and establishing foundational Knowledge Items.
- **`/sync`:** Idempotently updates the `aim_operator_profile` and `aim_project_architecture` as the project evolves, abandoning the monolithic CLI TUI menus of the past.

---

## SECTION 2: THE FIVE-TIER COGNITIVE ARCHITECTURE

The human brain does not hold every memory simultaneously. A.I.M. mirrors this biology using a 5-Tier layout to establish Epistemic Certainty without destroying the LLM context window.

### Tier 1: CONSTANT (Origin Memory)
**Mechanism:** `GEMINI.md` (injected as `user_rules`).
**Function:** 3-to-4 strict mandates that are injected on literally every API call. It contains the GitOps rules and the pointer to the boot sequence.

### Tier 2: SESSION (Active Working Memory)
**Mechanism:** `HANDOFF.md` -> `CURRENT_PULSE.md`.
**Function:** Generated fresh by the `/reincarnate` checkpoint process. Holds the Commander's intent and the last 5 turns of conversation to provide immediate situational awareness. Discarded at the end of the session.

### Tier 3: IMMEDIATE (Knowledge Items)
**Mechanism:** `~/.gemini/antigravity/knowledge/`.
**Function:** Persists across sessions. Provides localized, immediate structural rules like the Operator's identity and specific architectural choices for the specific codebase.

### Tier 4: DEEP (The Engram DB / Forgotten Memory)
**Mechanism:** Local SQLite Databases (`archive/engram.db`).
**Function:** Uses a **Hybrid RAG** engine (Nomic Vector Embeddings + FTS5 Lexical matching). It does NOT exist in active context. The agent must explicitly use `aim search` to recall data.

### Tier 5: AUTONOMIC (The Nervous System)
**Mechanism:** Python Scripts & Hooks (`src/*.py`).
**Function:** Pure, deterministic background processors that handle data extraction, file watching, and database generation. We do not ask the LLM to waste expensive tokens acting as a "super memory machine" when flat python code can do it for free ("Breathing").

---

## SECTION 3: THE CASCADING MEMORY WATERFALL (Tier 5 Organs)
The Tier 5 Autonomic Nervous system uses predefined Python pipelines to refine chat history into static knowledge.

1. **The Harvester (`hooks/session_summarizer.py`):** Strips JSON tool noise and extracts a lean "Signal Skeleton" (ARC Report).
2. **The Proposer (`src/memory_proposer.py`):** Squashes hourly logs into structured Add/Remove deltas.
3. **Daily Distillation (`src/daily_refiner.py`):** Consolidates Tier 2 proposals into a single Daily State.
4. **Weekly Arc (`src/weekly_consolidator.py`):** Synthesizes Daily proposals.
5. **The Apex Proposer (`src/monthly_archivist.py`):** Fuses everything into architectural axioms.

---

## SECTION 4: SAFETY & SOVEREIGNTY

### 4.1 The Obsidian Bridge (`scripts/obsidian_sync.py`)
- **Role:** Sovereign Mirror.
- **Function:** Mirroring of Daily Logs, Core Memory, and **Raw Transcripts** to an external Obsidian vault for 100% human-readable recovery.

---

## SECTION 5: THE HYBRID SOUL PROTOCOL

A.I.M. maintains technical continuity through a dual-mode ingestion engine within `src/bootstrap_brain.py`.

### 5.1 Foundation Sync (Active Instructions)
- **Scope:** `GEMINI.md`, `core/MEMORY.md`, and all files in `antigravity.wiki/`.
- **Logic:** These files are **Synchronized**. Every time a session starts, background hooks check timestamps and update the Engram DB automatically if a human touched the files.

### 5.2 Foundry Ingestion (Permanent Knowledge)
- **Scope:** Everything dropped into the `foundry/` folder.
- **Logic:** This is an **Onramp**. Once indexed, the knowledge is permanently persistent in Tier 4 Deep Memory.

---

## SECTION 6: UNIVERSAL SOVEREIGNTY (MCP)

### 6.1 Model Context Protocol (MCP) Server
- **Role:** IDE Tool Integration.
- **Function:** A built-in `fastmcp` server (`src/mcp_server.py`) exposes the A.I.M. Engram DB natively to agents.

### 6.2 Sovereign Sync (Git Synchronization)
- **Role:** Binary Conflict Resolution.
- **Function:** SQLite databases (`engram.db`) break git diffs. A.I.M. translates the database into deterministic `.jsonl` files (`archive/sync/`) during GitOps so memory changes can be peer-reviewed in GitHub PRs before merging.

---

## SECTION 7: TEST-DRIVEN DEVELOPMENT (TDD) POLICY
### 7.1 The Mandate
Every functional change **MUST** be governed by the TDD lifecycle. No code enters the `src/` directory without empirical verification.

---

## SECTION 8: GIT-OPS & SEMANTIC RELEASE (THE PUBLIC LEDGER)
### 8.1 Issue-Driven Development
- **`aim bug <description>`:** Creates a structured GitHub Issue via the `gh` CLI.
- **`aim fix <id>`:** Checks out a clean Git branch (`fix/issue-<id>`).

### 8.2 The Atomic Deployment Rule
- **The Rule:** AI agents are strictly forbidden from executing raw `git push origin main`. Every deployment must be atomic, originating from a unique `fix` branch, and packaged using `aim push "Prefix: msg"` to enforce correct SemVer prefixes.
