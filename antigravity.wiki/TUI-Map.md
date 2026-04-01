# A.I.M. TUI Architecture Map

> **Status:** Active — The Sovereign Cockpit (`aim tui`) is the primary configuration interface for the A.I.M. cognitive pipeline.
> Launch with: `aim-antigravity tui` or `python scripts/aim_config.py`

The **Sovereign Cockpit (TUI)** is the central control plane for the A.I.M. OS. It allows the operator to configure cognitive routing, behavioral guardrails, and memory retention policies without manually editing JSON files. All settings persist to `core/CONFIG.json` and the OS keyring.

The TUI is implemented in `scripts/aim_config.py` and dispatched via `aim-antigravity tui` or `aim-antigravity config`.

---

## 1. Run Cognitive Health Check (Test All Tiers)
- **Logic:** Iterates through all 6 cognitive tiers (Primary, Harvester, Proposer, Refiner, Consolidator, Archivist) defined in `core/CONFIG.json`.
- **Execution:** Calls `generate_reasoning("Respond with only the word: OK", brain_type=tier)` in `src/reasoning_utils.py` for each active tier. Fails on any response beginning with "Error", "Exception", or error codes.
- **Display:** Live green/red status dots in the tier status table, with full diagnostic message shown for failures.
- **Associated Files:** `core/CONFIG.json`, `src/reasoning_utils.py`, `scripts/aim_config.py`.

## 2. Manage Secret Vault (API Keys)
- **Logic:** Interfaces with the OS keyring to securely store and retrieve API credentials.
- **Execution:** Uses the Python `keyring` library via `scripts/aim_vault.py`.
- **Sub-options:** List Keys (shows SET/NOT SET status for all known keys), Set Key (prompts for service + key name + value).
- **Known Keys:** `google-api-key`, `openrouter-api-key`, `openai-api-key`, `anthropic-api-key`, `reasoning-api-key` — all under service `aim-system`.
- **Associated Files:** `scripts/aim_vault.py`.

## 3 & 4. Configure Brain / Cognitive Pipeline (T1-T5)
- **Logic:** Configures the `provider`, `model`, `endpoint`, and `auth_type` for each reasoning tier.
- **Tiers:**
  - `default_reasoning`: The primary brain for interactive tasks.
  - `tier1`: Tier 1 Harvester (`hooks/session_summarizer.py`)
  - `tier2`: Tier 2 Proposer (`src/memory_proposer.py`)
  - `tier3`: Tier 3 Refiner (`src/daily_refiner.py`)
  - `tier4`: Tier 4 Consolidator (`src/weekly_consolidator.py`)
  - `tier5`: Tier 5 Archivist (`src/monthly_archivist.py`)
- **Supported Providers:** `google`, `anthropic`, `openrouter`, `openai-compat`, `local` (Ollama), `codex-cli`, `disabled`
- **Associated Files:** `core/CONFIG.json`, `src/reasoning_utils.py`.

## 5. Manage MCP Server (IDE Integration)
- **Logic:** Launches the FastMCP server for IDE integration.
- **Execution:** Uses `subprocess` to launch `src/mcp_server.py`. Ctrl+C to stop.
- **Associated Files:** `src/mcp_server.py`.

## 6. Update Operator Profile & Behavior
- **Logic:** Prompts for full name, GitHub handle, and social alias. Updates the `Operator` field in `GEMINI.md`.
- **Note:** After saving, run `/sync` to propagate the change to KI artifacts (`aim_operator_profile`).
- **Associated Files:** `GEMINI.md`, `.agents/workflows/sync.md`.

## 7. Update Obsidian Vault Path
- **Logic:** Sets the absolute path to a local Obsidian Markdown vault.
- **Execution:** Writes the path to `["settings"]["obsidian_vault_path"]` in `core/CONFIG.json`.

## 8. Archive Retention
- **Logic:** Configures how many days raw JSON transcripts and old proposals are kept before cleanup.
- **Execution:** Writes an integer to `["settings"]["archive_retention_days"]` in `core/CONFIG.json`.

## 9. Auto-Memory Distillation
- **Logic:** Selects which tier automatically runs memory compression without operator intervention.
- **Execution:** Writes the target tier string (or "Off") to `["settings"]["auto_distill_tier"]` in `core/CONFIG.json`.

## 10. Set Agent Persona (Specialty Mandate)
- **Logic:** Saves a specialty persona string (e.g., "Senior Backend Architect") that can be injected into the agent's context.
- **Execution:** Writes to `["settings"]["agent_persona"]` in `core/CONFIG.json`.

## 11. Configure Cognitive Mantra (Anti-Drift)
- **Logic:** Sets a persistent anti-drift reminder string.
- **Execution:** Writes to `["settings"]["cognitive_mantra"]` in `core/CONFIG.json`. Used by `hooks/cognitive_mantra.py`.
- **Associated Files:** `core/CONFIG.json`, `hooks/cognitive_mantra.py`.

## 12. Configure Handoff Context Tail
- **Logic:** Determines the maximum number of lines the Continuity Engine preserves during handoff.
- **Special Case:** Setting to `0` enables **Full Session History** (no truncation).
- **Associated Files:** `core/CONFIG.json`, `src/handoff_pulse_generator.py`.

## 13. Configure Waterfall Pipeline
- **Logic:** Manages the "Consume & Clean" memory refinement hierarchy.
- **Sub-Options:**
    - **Tier Intervals:** Sets the wait-time (in Hours) for each of the 5 refinement tiers (default: 1h/12h/24h/72h/144h).
    - **Cleanup Mode:** Toggles between `ARCHIVE` (move files to archive) and `DELETE` (hard purge) for files consumed by the pipeline.
- **Associated Files:** `core/CONFIG.json`, `src/memory_utils.py`.

## 14. Reincarnation Protocol
- **Logic:** Toggles the `auto_rebirth` feature.
- **Execution:** If enabled, A.I.M. will automatically prompt for a Gameplan and spawn a fresh terminal session when context is full.
- **Associated Files:** `core/CONFIG.json`, `scripts/aim_reincarnate.py`.

---

*Cross-reference: [[Antigravity-Initialization-Architecture]] | [[TUI-Handoff-Report]] | [[Feature-Reincarnation-Gameplan]]*
