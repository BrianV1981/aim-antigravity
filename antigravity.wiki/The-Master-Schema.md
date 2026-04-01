# A.I.M. Technical Handbook (Master Schema v2.1)

> **Last Updated:** 2026-04-01
> This document is the definitive architectural map for the A.I.M. platform. It defines the modular components of the brain and the protocols that ensure continuity and sovereignty within the Google Antigravity ecosystem.
> For the complete script-level inventory, see the [Script Map](Script-Map.md).

---

## SECTION 1: THE ROOT ARCHITECTURE

### 1.1 `GEMINI.md` (The Index & Soul)
- **Role:** Lean Orchestrator & Cognitive Baseline.
- **Function:** An explicit **Table of Contents** that directs the agent to query its native Knowledge Items (KIs) or the background **Engram DB** for technical policies.
- **Cognitive Guardrails:** Permanently encodes the Operator's execution mode, GitOps workflow, TDD mandate, the Swarm Post Office protocol, and the Read-Receipt mandate.

### 1.2 The Initialization Workflow (`/init`)
- **Function:** A dynamic, decoupled scaffolding wizard.
- **Mechanism:** Typing `/init` into the Antigravity chat automatically ingests `GEMINI.md` and converts it into the `aim_master_directives` Knowledge Item.
- **Configuration:** Operator edits their KI directly or uses Antigravity's native GUI settings.

### 1.3 `HANDOFF.md` (The Front Door)
- **Role:** The first file any incoming agent reads after reincarnation.
- **Function:** Directs the agent through the Continuity Protocol: read `GEMINI.md` → `REINCARNATION_GAMEPLAN.md` → `CURRENT_PULSE.md` → check GitHub Issues → optionally read the Flight Recorder.

---

## SECTION 2: THE ENGRAM DB (SUBCONSCIOUS)
The core of A.I.M.'s deep-memory structure lives in a local SQLite database (`archive/engram.db`). It uses a **[Hybrid RAG](Feature-Hybrid-RAG.md)** engine, blending dense Vector Embeddings (Cosine Similarity) with FTS5 Lexical matching.

### 2.1 The Pre-Born Brain
During initialization, A.I.M. indexes this Handbook and core project directives via `src/bootstrap_brain.py`. This provides the agent with "Day Zero" technical knowledge.

### 2.2 Foundry Ingestion
The `foundry/` folder is a dedicated intake zone. Any technical references dropped here are recursively indexed as `expert_knowledge`. Once indexed, source files can be deleted.

### 2.3 The Session Engram (`history/session_engram.db`)
A separate SQLite database containing all conversational turns from every exported session. Used for deep NITH (Needle In The Haystack) queries across session history. Populated by `src/handoff_pulse_generator.py`.

### 2.4 The Cartridge Exchange
Expertise is portable. A.I.M. can export indexed knowledge into compressed `.engram` packs via `src/plugins/datajack/aim_bake.py`, allowing pre-trained "Expert" brains to be shared between machines.

---

## SECTION 3: THE [CASCADING MEMORY](Feature-Cascading-Memory.md) ENGINE (CONSCIOUSNESS)
Memory is refined through a tiered, self-cleaning hierarchy to prevent knowledge decay and file bloat.

| Tier | Script | Output | Cadence |
|---|---|---|---|
| 1 | `hooks/session_summarizer.py` | `memory/hourly/` | Per-session |
| 2 | `src/memory_proposer.py` | Add/Remove deltas | Every few hours |
| 3 | `src/daily_refiner.py` | Daily summary | Daily |
| 4 | `src/weekly_consolidator.py` | Weekly milestones | Weekly |
| 5 | `src/monthly_archivist.py` | Architecture axioms | Monthly |

---

## SECTION 4: THE [REINCARNATION](Feature-Reincarnation-Gameplan.md) PIPELINE (CONTINUITY)

> **⚠️ Antigravity-Native Architecture:** Legacy tmux-based terminal splicing has been replaced by a human-in-the-loop Export mechanism combined with zero-token Python parsing. See [Reincarnation Map](Reincarnation-Map.md) for the full step-by-step sequence.

### 4.1 The `/reincarnate` Workflow
1. Operator types `/reincarnate <Commander's Intent>`
2. Agent halts and displays mandatory Export prompt
3. Operator clicks Export button → `.md` transcript drops to `Downloads/`
4. Operator replies `Proceed`
5. Agent executes `python src/handoff_pulse_generator.py "<Intent>"`

### 4.2 The Dual-Extraction Pipeline
The exported `.md` is mechanically processed (zero API tokens):
- **Pipeline 1 (Archive):** Full transcript → `archive/raw/` + row-by-row into `history/session_engram.db`
- **Pipeline 2 (Pulse):** Last 5 turns → `continuity/CURRENT_PULSE.md`
- **Pipeline 3 (Will):** Commander's Intent → `continuity/REINCARNATION_GAMEPLAN.md`
- **Pipeline 4 (Recorder):** Full transcript → `continuity/LAST_SESSION_FLIGHT_RECORDER.md`

### 4.3 The Wake-Up Sequence
The incoming agent reads: `GEMINI.md` → `HANDOFF.md` → `REINCARNATION_GAMEPLAN.md` → `CURRENT_PULSE.md` → optionally `LAST_SESSION_FLIGHT_RECORDER.md`.

---

## SECTION 5: THE [SWARM POST OFFICE](The-Swarm-Post-Office.md) (COMMUNICATION)

### 5.1 The Global Chalkboard
Asynchronous inter-agent communication via `BrianV1981/aim-chalkboard` public GitHub repository. Agents drop `.md` files in team inboxes, never talk synchronously.

### 5.2 Commands
| Command | Function |
|---|---|
| `aim mail send <team> "<subject>" "<body>"` | Dispatch mail to a team inbox |
| `aim mail check` | Pull incoming mail into `continuity/UNREAD_MAIL.md` |
| `aim mail daemon --interval N` | Background polling every N minutes |
| `aim chalkboard "<natural language>"` | Natural language proxy for mail operations |

### 5.3 Safety
- **Anti-Spam Moderator:** Detects 5+ identical messages and quarantines the loop
- **Mandatory Read-Receipts:** Receiving agent must halt and confirm before executing
- **Postmaster Bridge:** `[TICKET]`/`[ISSUE]` tags auto-create GitHub Issues

---

## SECTION 6: SAFETY & SOVEREIGNTY

### 6.1 The Obsidian Bridge
- **Outbound:** `scripts/obsidian_sync.py` mirrors memory files to Obsidian vault
- **Inbound:** `scripts/obsidian_pull.py` pulls manual edits back

### 6.2 The Issue Tracker (`continuity/ISSUE_TRACKER.md`)
- **Dynamic:** `scripts/sync_issue_tracker.py` auto-detects the current repo from `git remote`
- **Multi-repo:** Pulls local repo issues AND optionally cross-swarm hub issues
- **Integration:** Called by `aim sync`, `aim crash`, and the daemon loop

---

## SECTION 7: UNIVERSAL SOVEREIGNTY

### 7.1 The Native GUI Cockpit
Centralized configuration handled by Antigravity IDE UI, supplemented by `core/CONFIG.json` for A.I.M.-specific settings.

### 7.2 Native File-System Hooks
Antigravity natively reads the local directory structure, bypassing standalone MCP servers.

### 7.3 The Universal Skills Framework
Antigravity supports `.agents/skills/` directories and `skills/` with paired `SKILL.md` manifests for autonomous tool discovery.

### 7.4 Fluid CLI Alias Architecture
The CLI command name dynamically adapts to the root directory name via `setup.ps1`/`setup.sh`. Examples: `aim-antigravity`, `aim-claude`, `aim-codex`.

---

## SECTION 8: DEVELOPMENT LIFECYCLE (GITOPS)

### 8.1 The Branching Strategy
1. **Report:** `aim bug "description"` or `aim enhancement "description"` to log the issue
2. **Isolate:** `aim fix <id>` to check out a unique branch
3. **Validate:** `git branch --show-current` — if output is `main`/`master`, **STOP**
4. **Release:** `aim push "Prefix: msg"` to push atomically

### 8.2 The TDD Mandate
Every functional change must be governed by the TDD lifecycle. Tests exist in `tests/` (17 test files). No code enters `src/` without a verification script.

---

## SECTION 9: THE FILE TREE (QUICK REFERENCE)

```
aim-antigravity/
├── GEMINI.md                  # Agent personality shell & operating rules
├── HANDOFF.md                 # Front door for incoming agents
├── CHANGELOG.md               # Version history
├── setup.ps1 / setup.sh       # Fluid alias installer
├── requirements.txt            # Python dependencies
│
├── .agents/workflows/          # Antigravity slash commands
│   ├── init.md                 # /init workflow
│   └── reincarnate.md          # /reincarnate workflow
│
├── core/                       # Configuration
│   ├── CONFIG.json             # Central config (paths, hub_repo, flags)
│   ├── MEMORY.md               # Live project state
│   ├── OPERATOR.md             # Operator identity
│   └── OPERATOR_PROFILE.md     # Extended operator profile
│
├── continuity/                 # Session continuity artifacts
│   ├── REINCARNATION_GAMEPLAN.md
│   ├── CURRENT_PULSE.md
│   ├── LAST_SESSION_FLIGHT_RECORDER.md
│   └── ISSUE_TRACKER.md
│
├── scripts/                    # CLI & utilities (28 .py files)
├── src/                        # Core engines (20 .py files)
├── hooks/                      # Event-driven hooks (4 .py files)
├── skills/                     # Discoverable agent skills (4 pairs)
├── plugins/                    # Modular extensions (3 plugins)
├── tests/                      # TDD test suite (17 test files)
│
├── memory/                     # Cascading memory tiers
│   ├── hourly/
│   ├── daily/
│   ├── weekly/
│   └── archive/
│
├── history/                    # Session Engram DB
│   └── session_engram.db
│
├── archive/                    # Deep storage (gitignored)
│   ├── raw/                    # Full session transcripts
│   ├── swarm_hub/              # Chalkboard staging
│   └── sync/                   # Sovereign sync exports
│
├── foundry/                    # Expert knowledge intake (gitignored)
└── antigravity.wiki/           # Full 54-page wiki
```
