# A.I.M. TUI Architecture Map

> 🟡 **STATUS: SUNSET / ORPHANED ARCHITECTURE**
> *The Monolithic Sovereign Cockpit (`aim tui` / `scripts/aim_config.py`) was structurally incompatible with the Antigravity IDE workflow. It has been permanently sunset. This document serves as a historical map of the legacy configuration options, which are now managed either directly via `core/CONFIG.json` or via IDE `/sync` Knowledge Items.*

The **Sovereign Cockpit (TUI)** was the central control plane for the legacy A.I.M. Linux OS. It allowed the operator to configure cognitive routing, behavioral guardrails, and memory retention policies without manually editing JSON files.

Below is the technical mapping of every legacy feature to its associated configuration file (which you can now edit directly).

---

## 1. Run Cognitive Health Check (Test All)
- **Status:** Replaced by IDE `/init` Workflow health checks.
- **Execution:** Calls `generate_reasoning("Respond with 'OK'")` in `src/reasoning_utils.py` for each active tier.
- **Associated Files:** `core/CONFIG.json`, `src/reasoning_utils.py`.

## 2. Manage Secret Vault (API Keys)
- **Status:** Retired. Native IDE Agents manage their own API keys via the IDE Settings interface.

## 3 & 4. Configure Brain / Cognitive Pipeline (T1-T5)
- **Status:** Edited natively in `core/CONFIG.json`.
- **Logic:** Configures the `provider`, `model`, `endpoint`, and `auth_type` for the reasoning engine.
- **Tiers:** 
  - `default_reasoning`: The primary brain for interactive tasks.
  - `tier1`: Tier 1: Harvester (`hooks/session_summarizer.py`)
  - `tier2`: Tier 2: Proposer (`src/memory_proposer.py`)
  - `tier3`: Tier 3: Refiner
  - `tier4`: Tier 4: Weekly Consolidator
  - `tier5`: Tier 5: Archivist

## 5. Manage MCP Server (IDE Integration)
- **Status:** FastMCP still active (`src/mcp_server.py`), but managed natively via Antigravity `run_command` tools rather than a TUI menu.

## 6. Update Operator Profile & Behavior
- **Status:** Replaced by **Tier 3 Knowledge Items (KIs)**.
- **Execution:** `aim_operator_profile` is synchronized effortlessly via the `/sync` slash workflow.

## 7. Update Obsidian Vault Path
- **Status:** Edited natively in `core/CONFIG.json` under `["settings"]["obsidian_vault_path"]`.

## 8. Archive Retention
- **Status:** Edited natively in `core/CONFIG.json` under `["settings"]["archive_retention_days"]`.

## 9. Auto-Memory Distillation
- **Status:** Edited natively in `core/CONFIG.json` under `["settings"]["auto_distill_tier"]`.

## 10. Set Agent Persona (Specialty Mandate)
- **Status:** Replaced by `aim_project_architecture` KI rules and direct `GEMINI.md` system prompts.

## 11. Configure Cognitive Mantra (Anti-Drift)
- **Status:** Edited natively in `core/CONFIG.json`.

## 12. Configure Handoff Context Tail
- **Status:** Handled via the `/reincarnate` IDE Slash Workflow.

## 13. Configure Waterfall Pipeline
- **Status:** Edited natively in `core/CONFIG.json`.
- **Logic:** Manages the "Consume & Clean" memory refinement hierarchy by editing Tier Intervals and Cleanup Mode (`ARCHIVE` vs `DELETE`).

## 14. Reincarnation Protocol
- **Status:** Legacy Terminal multiplexing (tmux) has been eliminated. Reincarnation is explicitly triggered via manual `/reincarnate` IDE Workflows.
