# Feature: Cascading Memory Engine (The Waterfall)

> ⚠️ **STATUS: UPDATED (v1.41.0)**
> *The legacy 4-tier system has been decommissioned. A.I.M. now utilizes the **5-Stage Waterfall Pipeline** with configurable intervals and the **Consume & Clean** protocol.*

## 1. Overview
The **Cascading Memory Engine** is the digestive system of A.I.M. It takes the "Raw mind" (JSON terminal logs) and processes it through multiple filters until it becomes "Durable Truth" (the `MEMORY.md` file).

## 2. The 5-Stage Waterfall
The refinement process is governed by time-based triggers. Each stage only processes the "unrefined" output of the stage below it.

1.  **Tier 1 (Harvester):** Runs every **1 hour**. Extracts the "Signal Skeleton" and produces reasoning-backed ARC reports (Adds/Removes/Contradicts).
2.  **Tier 2 (Proposer):** Runs every **12 hours**. Consolidates the hourly reports into a structured Delta.
3.  **Tier 3 (Refiner):** Runs every **24 hours**. Synthesizes multiple proposals into a single Daily State.
4.  **Tier 4 (Consolidator):** Runs every **72 hours (3 Days)**. Distills the daily states into macro architectural milestones.
5.  **Tier 5 (Archivist):** Runs every **144 hours (6 Days)**. Converts the weekly milestones into dense, factual axioms and **automatically applies them** to the durable memory file.

## 3. The "Consume & Clean" Protocol
To prevent redundancy and token burn, each stage "consumes" its inputs.
*   Once Tier 2 has successfully refined the Tier 1 reports, it immediately **Archives** or **Deletes** those reports.
*   This ensures that every refinement turn is only looking at **new data**.

## 4. Manual Override (`aim commit`)
The operator does not have to wait for the waterfall. You can run `aim commit` at any time to instantly trigger an AI-driven merge of the latest refinement proposal into your durable memory.

## 5. Configuration
All intervals and the cleanup mode (Archive vs Delete) are live-configurable via:
```bash
aim tui  # Option 13: Configure Waterfall Pipeline
```

---
*For the complete technical breakdown, see: [[Waterfall Memory Architecture]]*
