# Architecture Shift: The Reincarnation Gameplan & Willpower vs. Memory

## The Observation: System Prompt Fade at 30% Context
During the testing of the `/reincarnate` protocol, a critical behavioral pattern was observed: **System Prompt Fade**. 

At roughly 30% context utilization (~300k tokens), an agent retains full recall of its facts and coding capabilities, but its *adherence to rigid constraints* (like strict GitOps, TDD, and opening tickets before coding) begins to aggressively degrade. The agent slips back into standard "helpful assistant" mode, behaving like a "vibe coder" rather than a disciplined Sovereign Operator.

This validates the core thesis of A.I.M.: you cannot rely on an LLM's static system prompt indefinitely. You must physically restart the context window before obedience fails.

## The Paradigm Shift: Passing "Will" Instead of Just "Memory"
Previously, the continuity pipeline focused heavily on summarizing the past. The dying agent would generate a rolling delta of what just happened (`LAST_SESSION_FLIGHT_RECORDER.md`) and a snapshot of the current state (`CURRENT_PULSE.md`). 

However, reading a 2000-line history requires the incoming agent to expend heavy cognitive effort deducing the *narrative* and *intent* of the previous agent.

To solve this, the Continuity Pipeline is shifting to enforce a **Reincarnation Gameplan**.

### The New Hand-off Mechanics
1. **The Dying Agent's Final Task (The Gameplan):** Before the `/reincarnate` workflow triggers the Antigravity chat window reset, the degraded agent is forced to write a highly prescriptive `continuity/REINCARNATION_GAMEPLAN.md`. This file is not a summary of the past; it is a 3-step executive directive for the *future*. It bypasses inference and explicitly orders the next agent on exactly what mechanical steps to take upon waking up.
2. **The Full Session History:** `LAST_SESSION_FLIGHT_RECORDER.md` will be transitioned from a truncated rolling delta into a **FULL session history**. It will serve as a complete, pristine Markdown reference of the previous session. 
3. **The Attention Redirect:** Critically, the incoming agent will **NOT** be directed to read the full history upon waking. Giving a fresh agent a massive history file immediately pollutes its clean context. Instead, `HANDOFF.md` will strictly direct the incoming agent to read:
   - `continuity/REINCARNATION_GAMEPLAN.md` (The Will/Intent)
   - `continuity/CURRENT_PULSE.md` (The State)
   - The Antigravity built-in GitOps branch tracker (The Ledger)
   
The incoming agent only refers to the full `LAST_SESSION_FLIGHT_RECORDER.md` if the Gameplan explicitly requires historical extraction.

This architectural shift guarantees that a fresh agent wakes up not just with epistemic certainty of the state, but with laser-focused, immediate velocity.
