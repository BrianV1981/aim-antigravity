# Architecture: The Waterfall Memory Refinement Pipeline

## 1. Intent: Precision vs. Noise
The **Waterfall Memory Pipeline** is the core operational mechanism of the **Tier 5 Autonomic Nervous System**. It is designed to solve the "Knowledge Drift" and "Token Burn" problems inherent in autonomous AI agents. 

Instead of an agent carrying its entire sprawling history into every turn, A.I.M. utilizes a self-cleaning autonomic hierarchy. This ensures that the agent's **Active Context** remains lean and focused on architectural truth, while its **Deep Memory** is safely offloaded and synthesized into axioms.

---

## 2. The 5-Stage Waterfall (Intervals)

Refinement happens in logical background waves. Each stage only fires once its specific "Wait Interval" has been met since its last execution. These intervals are fully adjustable via `core/CONFIG.json`.

> 💡 **Note on Terminology:** Do not confuse these Pipeline *Stages* with the 5 *Tiers* of the Cognitive Architecture. This entire timeline represents the internal machinations of Tier 5 (Autonomic).

| Stage | Name | Default Interval | Objective |
| :--- | :--- | :--- | :--- |
| **Stage 1** | **Harvester** | 1 Hour | Convert raw chat export deltas into structured technical reports. |
| **Stage 2** | **Proposer** | 12 Hours | Consolidate Stage 1 reports into a structured Delta Proposal. |
| **Stage 3** | **Refiner** | 1 Day | Distill Stage 2 proposals into a cohesive Daily State. |
| **Stage 4** | **Consolidator** | 3 Days | Elevate Stage 3 achievements into macro project milestones. |
| **Stage 5** | **Archivist** | 6 Days (144h) | Solidify Stage 4 milestones into dense, factual engrams and **Auto-Apply** to Deep memory/KIs. |

---

## 3. The "Consume & Clean" Protocol

To keep the pipeline efficient, A.I.M. enforces a strict **Consumption Rule**. When a higher stage successfully processes data from a lower stage, it "consumes" that data.

*   **Logic:** If Stage 2 (Proposer) consolidates reports from Stage 1, those hourly reports are immediately archived or deleted.
*   **Benefits:**
    1.  **Zero Redundancy:** The agent's background processor never reviews the same data twice.
    2.  **Stateless Execution:** Each script only looks for "new" files in its target folder.
    3.  **Automatic Cleanup:** The `memory/` directory does not bloat over time. Once a fact is committed, the intermediate scaffolding is purged.

---

## 4. History vs. Memory (Decoupling)

A.I.M. treats "What happened" and "What we learned" as two completely different systems.

### 4.1 Durable Memory (The Exoskeleton)
The Waterfall pipeline described above is strictly for updating long-term state. It uses an **ARC-only model** (Add/Remove/Contradict) to save tokens. Only the final commit operation performs a full rewrite of the memory files.

### 4.2 Eternal Recall (The Flight Recorder)
A separate mechanism runs during the handoff process to preserve the full record of every session.
*   During `/reincarnate`, the `LAST_SESSION_FLIGHT_RECORDER.md` captures an exact trace of the workflow history to provide deep searchability if an agent later realizes it forgot how an implementation occurred.

---

## 5. System Configuration
The entire pipeline is user-configurable natively inside Antigravity by altering `core/CONFIG.json` (replacing the legacy `aim tui` cockpit menu).
1.  **Set Intervals:** Change how frequently each Stage fires.
2.  **Toggle Cleanup:** Choose between `ARCHIVE` mode or `DELETE` mode for consumed files.
