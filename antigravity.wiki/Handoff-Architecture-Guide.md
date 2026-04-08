# Architecture: The Handoff & Continuity Pipeline

A.I.M. solves the **Amnesia Problem** by ensuring that no technical progress is lost when an agent's context window fills. The system utilizes a dual-layered continuity approach: **Executive Hand-off** (Immediate Action) and **Eternal Recall** (Historical Context).

> **⚠️ Antigravity-Native Architecture:** This pipeline has been fully adapted to operate within the Antigravity IDE. The legacy `tmux`-based terminal splicing and raw JSON scraping have been replaced by a **human-in-the-loop Export mechanism** combined with zero-token Python parsing. See [Reincarnation Map](Reincarnation-Map.md) for the full step-by-step sequence.

---

## 1. Layer 1: Executive Hand-off (MANDATORY)

When an agent reaches the 30% context threshold, the Operator initiates the **[Reincarnation](Feature-Reincarnation-Gameplan.md) Protocol** by typing `/reincarnate <Commander's Intent>`.

### 1.1 The `/reincarnate` Workflow
The dying agent immediately halts and displays a mandatory Export prompt:
> *"⚠️ Please click the **Export** button at the top of this chat window to download the transcript. Reply **Proceed** or **Cancel**."*

Once the Operator clicks Export and replies `Proceed`, the agent executes `python src/handoff_pulse_generator.py "<Intent>"`. This is a **100% zero-token** Python pipeline that mechanically generates all continuity artifacts without spending LLM API tokens.

### 1.2 The [Reincarnation](Feature-Reincarnation-Gameplan.md) Gameplan
The Python pipeline writes `REINCARNATION_GAMEPLAN.md` from the Commander's Intent parameter.
- **Intent:** Passing "Will" instead of "Memory." 
- **Content:** Explicit, rigid directives for the next agent (e.g., "1. Fix the SQL trigger in Tier 5. 2. Verify with pytest. 3. Do not refactor the CLI.")
- **Benefit:** Bypasses the need for the new agent to analyze the previous agent's conversational drift.

### 1.3 The Context Pulse & Issue Sync
Simultaneously, the pipeline creates `CURRENT_PULSE.md`.
- **Function:** Extracts the **last 5 conversational turns** from the exported transcript — the immediate technical "Edge" of the session.
- **Filtering:** Pure Python string parsing on the exported `.md` file. Zero API cost.

**Autonomous Sync:** The `handoff_pulse_generator.py` uses the `sync_issue_tracker.py` tool to silently pull the active GitHub tickets into `continuity/ISSUE_TRACKER.md`. This gives the reincarnated agent a flawless view of what is natively assigned to it.


### 1.4 The Flight Recorder
The full exported `.md` transcript is copied directly to `continuity/LAST_SESSION_FLIGHT_RECORDER.md`.
- **Function:** Complete, pristine forensic archive of the entire session.
- **Usage:** Only consulted when the Operator explicitly asks about a granular detail (a "NITH" — Needle In The Haystack) from the prior session.

---

## 2. Layer 2: Eternal Recall (OPTIONAL)

While the new agent is born with a clean context, it retains access to the entire history of the project through the **History Search System**.

### 2.1 The Dual-Extraction Pipeline (`src/handoff_pulse_generator.py`)
Every exported session transcript is simultaneously processed through two pipelines:
1. **Pipeline 1 (Archive):** Full raw transcript → `archive/raw/session_<timestamp>.md`.
2. **Pipeline 2 (Engram DB):** Row-by-row ingestion of all conversational turns into `history/session_engram.db` (SQLite, columns: `id, session_id, timestamp, role, content`).

### 2.2 Global History Search
The cleaned session data is indexed in `history/session_engram.db` utilizing SQLite FTS5.
- **Command:** `aim search <query>`
- **Usage:** The new agent only accesses this layer if the Gameplan explicitly requires historical context extraction (e.g., "Recall the regex used in the legacy parser from 3 sessions ago").

---

## 3. The Wake-up Sequence

When the new agent boots in a fresh Antigravity chat window, it is governed by a strict **Continuity Protocol** defined in `HANDOFF.md`:

1.  **Read `GEMINI.md`**: Acknowledge core constraints and GitOps rules (auto-loaded via KI system).
2.  **Read `continuity/REINCARNATION_GAMEPLAN.md`**: Ingest immediate executive directives (The "Will").
3.  **Read `continuity/CURRENT_PULSE.md`**: Locate the current technical edge (last 5 turns).
4.  **Read `continuity/ISSUE_TRACKER.md`**: Locate all Git-level tickets and assignments.
5.  **(Optional) Morning Report**: The agent may fire `/morning` (via `hooks/morning_report.py`) to automatically generate and ingest `MORNING_REPORT.md` containing Git branch status, MEMORY.md deltas, and the tracker inside one briefing.

This sequence ensures that the fresh agent achieves **Epistemic Certainty** before taking its first action.

