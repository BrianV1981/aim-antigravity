# A.I.M. TUI Architecture Map

The **Sovereign Cockpit (TUI)** is the central control plane for the A.I.M. OS. It allows the operator to configure the cognitive routing, behavioral guardrails, and memory retention policies without manually editing JSON files.

The TUI is entirely executed via `scripts/aim_config.py`. Below is the technical mapping of every feature to its associated configuration file and system logic.

---

## 1. Run Cognitive Health Check (Test All)
- **Logic:** Iterates through all 6 cognitive tiers (Primary, Harvester, Proposer, Refiner, Consolidator, Archivist) defined in `core/CONFIG.json`.
- **Execution:** Calls `generate_reasoning("Respond with 'OK'")` in `src/reasoning_utils.py` for each active tier.
- **Associated Files:** `core/CONFIG.json`, `src/reasoning_utils.py`, `scripts/aim_config.py`.

## 2. Manage Secret Vault (API Keys)
- **Logic:** Interfaces directly with the underlying Linux/macOS keyring to securely store, retrieve, or delete API credentials. 
- **Execution:** Uses the Python `keyring` library (wrapped in `scripts/aim_vault.py`). 
- **Associated Files:** `scripts/aim_vault.py`.

## 3 & 4. Configure Brain / Cognitive Pipeline (T1-T5)
- **Logic:** Configures the `provider`, `model`, `endpoint`, and `auth_type` for the reasoning engine.
- **Tiers:** 
  - `default_reasoning`: The primary brain for interactive tasks.
  - `tier1`: Tier 1: Harvester (`hooks/session_summarizer.py`)
  - `tier2`: Tier 2: Proposer (`src/memory_proposer.py`)
  - `tier3`: Tier 3: Refiner
  - `tier4`: Tier 4: Weekly Consolidator
  - `tier5`: Tier 5: Archivist
- **Associated Files:** `core/CONFIG.json`, `src/reasoning_utils.py`.

## 5. Manage MCP Server (IDE Integration)
- **Logic:** Manages the FastMCP server for IDE integration (Cursor/VS Code).
- **Execution:** Uses `subprocess` to launch `src/mcp_server.py`.
- **Associated Files:** `src/mcp_server.py`, `skills/*`.

## 6. Update Operator Profile & Behavior
- **Logic:** Asks the user for both operator identity fields and behavioral guardrails.
- **Execution:** Rewrites `core/OPERATOR.md`, `core/OPERATOR_PROFILE.md`, and updates `GEMINI.md`.
- **Associated Files:** `GEMINI.md`, `core/OPERATOR.md`, `core/OPERATOR_PROFILE.md`.

## 7. Update Obsidian Vault Path
- **Logic:** Sets the absolute path to a local Obsidian Markdown vault.
- **Execution:** Writes the path to `["settings"]["obsidian_vault_path"]` in `core/CONFIG.json`. 

## 8. Archive Retention
- **Logic:** Configures how many days the system should keep raw JSON transcripts and old proposals.
- **Execution:** Writes an integer to `["settings"]["archive_retention_days"]`.

## 9. Auto-Memory Distillation
- **Logic:** Determines if the system should automatically condense its own memories without human intervention.
- **Execution:** Writes the target tier (e.g., "tier5") to `["settings"]["auto_distill_tier"]`.

## 10. Set Agent Persona (Specialty Mandate)
- **Logic:** Injects a specialized mandate (e.g., Frontend Architect) into the top of the AI's system prompt.
- **Associated Files:** `GEMINI.md`.

## 11. Configure Cognitive Mantra (Anti-Drift)
- **Logic:** Configures the `cognitive_mantra.py` watchdog timer to prevent behavioral drift.
- **Associated Files:** `core/CONFIG.json`, `hooks/cognitive_mantra.py`.

## 12. Configure Handoff Context Tail
- **Logic:** Determines the maximum number of lines the Continuity Engine preserves during handoff.
- **Special Case:** Setting to `0` enables **Full Session History** (no truncation).
- **Associated Files:** `core/CONFIG.json`, `src/handoff_pulse_generator.py`.

## 13. Configure Waterfall Pipeline
- **Logic:** Manages the "Consume & Clean" memory refinement hierarchy.
- **Sub-Options:**
    - **Tier Intervals:** Sets the wait-time (in Hours) for each of the 6 refinement tiers.
    - **Cleanup Mode:** Toggles between `ARCHIVE` (move files to archive) and `DELETE` (hard purge) for scaffolding files consumed by the pipeline.
- **Associated Files:** `core/CONFIG.json`, `src/memory_utils.py`.

## 14. Reincarnation Protocol
- **Logic:** Toggles the `auto_rebirth` feature.
- **Execution:** If enabled, A.I.M. will automatically prompt for a Gameplan and spawn a fresh terminal session when context is full.
- **Associated Files:** `core/CONFIG.json`, `scripts/aim_reincarnate.py`.
