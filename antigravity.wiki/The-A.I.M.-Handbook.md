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
- **Clean Sweep:** Allows the user to independently wipe Project Docs (Roadmap, Changelog) and/or the AI Brain (Engram DB).
- **The TUI Updater:** The Operator can hot-swap the AI's personality and rules dynamically using the `aim tui` cockpit.

---

## SECTION 2: THE ENGRAM DB (SUBCONSCIOUS)
The core of A.I.M.'s memory lives in a local SQLite database (`archive/engram.db`). It uses a **Hybrid RAG** engine, blending dense Vector Embeddings (Cosine Similarity) with FTS5 Lexical matching (BM25) to provide recall of abstract concepts and exact variable names.

### 2.1 The Pre-Born Brain
During initialization, A.I.M. indexes this Handbook and core project directives. This provides the agent with "Day Zero" technical knowledge.

### 2.2 Foundry Ingestion
The `foundry/` folder is a dedicated intake zone. Any technical references dropped here are recursively indexed as `expert_knowledge`.

### 2.3 The Cartridge Exchange (`aim exchange`)
Expertise is portable. A.I.M. can `export` its indexed knowledge into compressed `.engram` packs, allowing you to share pre-trained brains with other machines without re-indexing.

---

## SECTION 3: THE WATERFALL MEMORY ENGINE
Memory is refined through a 5-stage, self-cleaning hierarchy to prevent knowledge decay and token burn.

### 3.1 Tier 1: The Harvester (`hooks/session_summarizer.py`)
- **Interval:** 1 Hour (Adjustable).
- **Function:** Converts raw terminal deltas into technical ARC reports (Adds/Removes/Contradicts).
- **Output:** Concise narratives saved to `memory/hourly/`.

### 3.2 Tier 2: The Proposer (`src/memory_proposer.py`)
- **Interval:** 12 Hours (Adjustable).
- **Function:** Consolidates Tier 1 reports into a structured Delta Proposal.

### 3.3 Tier 3: The Refiner (`src/daily_refiner.py`)
- **Interval:** 1 Day (Adjustable).
- **Function:** Distills multiple Tier 2 proposals into a cohesive Daily State.

### 3.4 Tier 4: The Consolidator (`src/weekly_consolidator.py`)
- **Interval:** 3 Days (Adjustable).
- **Function:** Elevates Daily States into macro project milestones.

### 3.5 Tier 5: The Archivist & Failsafe (`src/monthly_archivist.py`)
- **Interval:** 6 Days / 144h (Adjustable).
- **Function:** Solidifies Weekly Milestones into dense, factual axioms.
- **Auto-Apply:** Automatically triggers the Master Merger to update `core/MEMORY.md` and executes the **Full Purge** of scaffolding files.

---

## SECTION 4: ETERNAL RECALL (HISTORY)

### 4.1 The History Scribe (`src/history_scribe.py`)
- **Role:** Parallel Persistence.
- **Function:** Event-driven processor that scrubs raw IDE arrays by natively parsing exported session `.md` files directly from the Windows `Downloads/` directory, rather than relying on legacy daemon JSON polling.
- **The 2000-Line Rule:** Automatically splits massive sessions into manageable chunks to prevent file-size bloat.
- **Search:** Full-text search across all historical sessions via `aim search-sessions`.

---

## SECTION 5: SAFETY & SOVEREIGNTY

### 5.1 The Reincarnation Gameplan
- **Function:** Before context fills, A.I.M. prompts the user for a Gameplan and teleports state to a fresh terminal session.
- **Directive:** Passing "Will" instead of just "Memory" to prevent agent hallucination at high token counts.

### 5.2 The Obsidian Bridge
- **Role:** Sovereign Mirror.
- **Function:** Mirroring of Daily Logs, Core Memory, and **Clean Session History** to an external vault for 100% recovery.

---

## SECTION 6: SYSTEM MAINTENANCE

### 6.1 The Sovereign Update (`aim update`)
- **Role:** High-Fidelity Sync.
- **Function:** Performs source pulls, hook refreshes, and personality preservation.

---

"I believe I've made my point." — **A.I.M.**
