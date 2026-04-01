# Architecture Shift: The Reincarnation Gameplan & Willpower vs. Memory

## The Observation: System Prompt Fade at 30% Context
During the testing of the `/reincarnate` protocol, a critical behavioral pattern was observed: **System Prompt Fade**. 

At roughly 30% context utilization (~300k tokens), an agent retains full recall of its facts and coding capabilities, but its *adherence to rigid constraints* (like strict GitOps, TDD, and opening tickets before coding) begins to aggressively degrade. The agent slips back into standard "helpful assistant" mode, behaving like a "vibe coder" rather than a disciplined Sovereign Operator.

This validates the core thesis of A.I.M.: you cannot rely on an LLM's static system prompt indefinitely. You must physically restart the context window before obedience fails.

## The Paradigm Shift: Passing "Will" Instead of Just "Memory"
Previously, the continuity pipeline focused heavily on summarizing the past. The dying agent would generate a rolling delta of what just happened (`LAST_SESSION_FLIGHT_RECORDER.md`) and a snapshot of the current state (`CURRENT_PULSE.md`). 

However, reading a 2000-line history requires the incoming agent to expend heavy cognitive effort deducing the *narrative* and *intent* of the previous agent.

To solve this, the Continuity Pipeline is shifting to enforce a **Reincarnation Gameplan**.

### The New Hand-off Mechanics (Antigravity-Native)

> **⚠️ Architecture Note:** The Antigravity IDE locks all conversation data inside proprietary `.pb` (Protocol Buffer) binary files. Zero-token extraction methods (Protobuf decode, MITM proxy, UI automation, LevelDB scraping) were exhaustively tested and all failed. The pipeline now uses a **human-in-the-loop Export mechanism** combined with zero-token Python parsing.

1. **The `/reincarnate` Trigger:** When the Operator types `/reincarnate <Intent>`, the dying agent immediately halts all execution and displays a mandatory Export prompt: *"⚠️ Please click the Export button at the top of this chat window. Reply Proceed or Cancel."*
2. **The Manual Export:** The Operator physically clicks the Export button in the Antigravity GUI. This drops a perfectly clean `.md` transcript into `C:\Users\kingb\Downloads\`.
3. **The Zero-Token Python Pipeline:** Upon receiving `Proceed`, the agent executes `python src/handoff_pulse_generator.py "<Intent>"`. This Python script mechanically:
   - Hunts the newest `.md` file in `Downloads/`.
   - Copies the full transcript to `continuity/LAST_SESSION_FLIGHT_RECORDER.md`.
   - Archives a timestamped copy to `archive/raw/session_<timestamp>.md`.
   - Ingests all conversational turns row-by-row into `history/session_engram.db` (SQLite FTS5).
   - Extracts the **last 5 turns** and writes them to `continuity/CURRENT_PULSE.md`.
   - Formats `continuity/REINCARNATION_GAMEPLAN.md` from the Commander's Intent parameter.
4. **The Gameplan (`REINCARNATION_GAMEPLAN.md`):** This file is not a summary of the past; it is a 3-step executive directive for the *future*. It bypasses inference and explicitly orders the next agent on exactly what mechanical steps to take upon waking up.
5. **The Full Session History (`LAST_SESSION_FLIGHT_RECORDER.md`):** This is the complete, pristine exported Markdown transcript of the previous session. It serves as a forensic archive, only consulted when the Operator explicitly asks about a granular detail (a "NITH" — Needle In The Haystack).
6. **The Attention Redirect:** Critically, the incoming agent will **NOT** be directed to read the full history upon waking. Giving a fresh agent a massive history file immediately pollutes its clean context. Instead, `HANDOFF.md` strictly directs the incoming agent to read:
   - `continuity/REINCARNATION_GAMEPLAN.md` (The Will/Intent)
   - `continuity/CURRENT_PULSE.md` (The State — last 5 turns)
   
The incoming agent only refers to the full `LAST_SESSION_FLIGHT_RECORDER.md` if the Gameplan explicitly requires historical extraction, or if the Operator asks about something specific from the prior session.

This architectural shift guarantees that a fresh agent wakes up not just with epistemic certainty of the state, but with laser-focused, immediate velocity.

