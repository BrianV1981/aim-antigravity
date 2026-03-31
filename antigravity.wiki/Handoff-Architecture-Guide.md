# Architecture: The Handoff & Continuity Pipeline

A.I.M. solves the **Amnesia Problem** by ensuring that no technical progress is lost when an agent's context window fills. The system utilizes a dual-layered continuity approach: **Executive Hand-off** (Immediate Action) and **Eternal Recall** (Historical Context).

---

## 1. Layer 1: Executive Hand-off (MANDATORY)

When an agent reaches the 30% context threshold, it initiates the **[Reincarnation](Feature-Reincarnation-Gameplan.md) Protocol**. This is a surgical state-transfer designed to give the next agent laser-focused velocity without polluting its context with historical noise.

### 1.1 The [Reincarnation](Feature-Reincarnation-Gameplan.md) Gameplan
Before shutting down, the dying agent is prompted to write a **REINCARNATION_GAMEPLAN.md**.
- **Intent:** Passing "Will" instead of "Memory." 
- **Content:** Explicit, rigid directives for the next agent (e.g., "1. Fix the SQL trigger in Tier 5. 2. Verify with pytest. 3. Do not refactor the CLI.")
- **Benefit:** Bypasses the need for the new agent to analyze the previous agent's conversational drift.

### 1.2 The Context Pulse
Simultaneously, the **Handoff Pulse Generator** creates `CURRENT_PULSE.md`.
- **Function:** Synthesizes the "Project Edge"—exactly what was just finished, what is currently broken, and what the very next step is.
- **Filtering:** Uses the **Zero-Token Harvester** to ignore 85% of terminal noise and focus only on technical logic.

---

## 2. Layer 2: Eternal Recall (OPTIONAL)

While the new agent is born with a clean context, it retains access to the entire history of the project through the **History Search System**.

### 2.1 The History Scribe (`src/history_scribe.py`)
A background process that converts every raw JSON transcript into a clean Markdown session log.
- **The 2000-Line Rule:** To ensure files remain readable for both humans and AIs, any session exceeding 2000 lines is automatically split into parts (e.g., `session_part1.md`).
- **Storage:** `archive/history/`.

### 2.2 Global History Search
The cleaned logs are indexed in a dedicated `archive/history.db` utilizing SQLite FTS5.
- **Command:** `aim search-sessions <query>`
- **Usage:** The new agent only accesses this layer if the Gameplan explicitly requires historical context extraction (e.g., "Recall the regex used in the legacy parser from 3 days ago").

---

## 3. The Wake-up Sequence

When the new agent boots, it is governed by a strict **Continuity Protocol** defined in `HANDOFF.md`:

1.  **Read `GEMINI.md`**: Acknowledge core constraints and GitOps rules.
2.  **Read `continuity/REINCARNATION_GAMEPLAN.md`**: Ingest immediate executive directives.
3.  **Read `continuity/CURRENT_PULSE.md`**: Locate the current technical edge.
4.  **Read `ISSUE_TRACKER.md`**: Synchronize with the active task ledger.

This sequence ensures that the fresh agent achieves **Epistemic Certainty** before taking its first action.
