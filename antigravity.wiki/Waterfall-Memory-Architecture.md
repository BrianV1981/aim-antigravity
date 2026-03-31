# Architecture: The Waterfall Memory Refinement Pipeline

## 1. Intent: Precision vs. Noise
The **Waterfall Memory Pipeline** is designed to solve the "Knowledge Drift" and "Token Burn" problems inherent in autonomous AI agents. 

Instead of an agent carrying its entire sprawling history into every turn, A.I.M. utilizes a tiered, self-cleaning hierarchy. This ensures that the agent's **Active Context** remains lean and focused on architectural truth, while its **Eternal Recall** is safely offloaded to a separate, searchable historical database.

---

## 2. The 5-Stage Waterfall (Intervals)

Refinement happens in logical waves. Each tier only fires once its specific "Wait Interval" has been met since its last execution. These intervals are fully adjustable via the `aim tui` (Option #13).

| Tier | Name | Default Interval | Objective |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Harvester** | 1 Hour | Convert raw JSON terminal deltas into technical ARC reports (Adds/Removes/Contradicts). |
| **Tier 2** | **Proposer** | 12 Hours | Consolidate Tier 1 reports into a structured Delta Proposal. |
| **Tier 3** | **Refiner** | 1 Day | Distill Tier 2 proposals into a cohesive Daily State. |
| **Tier 4** | **Consolidator** | 3 Days | Elevate Tier 3 achievements into macro project milestones. |
| **Tier 5** | **Archivist** | 6 Days (144h) | Solidify Tier 4 milestones into dense, factual axioms and **Auto-Apply** to `core/MEMORY.md`. |

---

## 3. The "Consume & Clean" Protocol

To keep the pipeline efficient, A.I.M. enforces a strict **Consumption Rule**. When a higher tier successfully processes data from a lower tier, it "consumes" that data.

*   **Logic:** If Tier 2 (Proposer) consolidates reports from Tier 1, those hourly reports are immediately archived or deleted.
*   **Benefits:**
    1.  **Zero Redundancy:** Agents never review the same data twice.
    2.  **Stateless Tiers:** Each script only looks for "new" files in its target folder.
    3.  **Automatic Cleanup:** The `memory/` directory does not bloat over time. Once a fact is committed to the "Durable Core" (`MEMORY.md`), the intermediate scaffolding is purged.

---

## 4. History vs. Memory (Decoupling)

A.I.M. treats "What happened" and "What we learned" as two different systems.

### 4.1 Durable Memory (The Exoskeleton)
The 5-Tier pipeline described above is strictly for updating `core/MEMORY.md`. It uses an **ARC-only model** (Add/Remove/Contradict) to save tokens. Only the final commit operation performs a full rewrite of the memory file.

### 4.2 Eternal Recall (The History Scribe)
A separate process, `src/history_scribe.py`, runs in the background to preserve the full record of every session.
*   **The 2000-Line Rule:** To prevent massive file bloat that chokes LLMs and editors, the Scribe automatically splits sessions into multiple parts if they exceed 2000 lines.
*   **Searchable DB:** Cleaned Markdown sessions are indexed in `archive/history.db` and searchable via `aim search-sessions`.

---

## 5. TUI Configuration
The entire pipeline is user-configurable. Through the `aim tui`, the operator can:
1.  **Set Intervals:** Change how frequently each tier fires.
2.  **Toggle Cleanup:** Choose between `ARCHIVE` mode or `DELETE` mode for consumed files.
