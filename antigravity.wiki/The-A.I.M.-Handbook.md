# A.I.M. Technical Handbook (Master Schema)

This document is the definitive architectural map for the A.I.M. platform. It defines the modular components of the brain and the protocols that ensure continuity and sovereignty within the Google Antigravity ecosystem.

---

## SECTION 1: THE ROOT ARCHITECTURE

### 1.1 `GEMINI.md` (The Index & Soul)
- **Role:** Lean Orchestrator & Cognitive Baseline.
- **Function:** It is an explicit **Table of Contents**. Instead of holding massive walls of text, it directs the agent to query the Knowledge Item (KI) system or background **Engram DB** for technical policies.
- **Cognitive Guardrails:** It permanently encodes the Operator's chosen execution mode (Autonomous vs Cautious), GitOps workflow, and the "Token-Saver" conciseness mandate.

### 1.2 The Initialization Workflow (`/init`)
- **Function:** A dynamic, decoupled scaffolding wizard native to Antigravity.
- **Mechanism:** By typing `/init` in the IDE chat, the system parses the `GEMINI.md` rules and formally registers them into your persistent `aim_master_directives` Knowledge Item, securing the architectural boundaries for all future operations.
- **The GUI Updater:** To hot-swap the AI's personality and routing rules, operators simply edit their Knowledge Items or adjust Antigravity's native settings panels (eliminating the legacy `aim tui` terminal cockpit).

---

## SECTION 2: THE ENGRAM DB (SUBCONSCIOUS)
The core of A.I.M.'s advanced memory lives in an optional local SQLite database (`archive/engram.db`) managed by background Python daemons. It uses a **[Hybrid RAG](Feature-Hybrid-RAG.md)** engine, blending dense Vector Embeddings with exact FTS5 Lexical matching. 

*Note: For lightweight projects, Antigravity's native Knowledge Items completely replace the need to run the Engram DB logic.*

### 2.1 The Pre-Born Brain
During complex initializations, A.I.M. indexes this Handbook and core project directives into the `.engram` file, providing the agent with "Day Zero" technical knowledge.

### 2.2 Foundry Ingestion
The `foundry/` folder is a dedicated intake zone. Any technical references dropped here are recursively indexed as `expert_knowledge`.

### 2.3 The Cartridge Exchange
Expertise is portable. A.I.M. can export its indexed knowledge into compressed `.engram` packs, allowing you to share pre-trained brains with other workspaces directly via standard file sharing.

---

## SECTION 3: THE WATERFALL MEMORY ENGINE
If the background Python daemons are enabled, memory is refined through a 5-stage, self-cleaning hierarchy to prevent knowledge decay.

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

## SECTION 4: PROGRESSION & SOVEREIGNTY

### 4.1 The [Reincarnation](Feature-Reincarnation-Gameplan.md) Gameplan (`/reincarnate`)
- **Function:** Before the context window fills up, A.I.M. prompts the user for a Gameplan and teleports state to a fresh Antigravity chat window.
- **Directive:** Passing "Will" instead of just "Memory" to prevent agent hallucination at high token counts.

### 4.2 The Obsidian Bridge
- **Role:** Sovereign Mirror.
- **Function:** Mirroring of Daily Logs, Core Memory, and Clean Session History to an external vault for 100% offline recovery natively accessible by human operators.

---

## SECTION 5: SYSTEM MAINTENANCE

### 5.1 The Sovereign Update
- **Role:** High-Fidelity Sync.
- **Function:** Because A.I.M. is built on GitOps, standard `git pull origin main` commands perform source pulls and hook refreshes while preserving your local `.ignore` state and Knowledge Items. (Replacing the legacy `aim update` bash alias).

---

"I believe I've made my point." — **A.I.M.**
