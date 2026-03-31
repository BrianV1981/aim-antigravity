---
description: Reincarnation protocol, context handoff, and continuity pipeline
---

# /reincarnate <Commander's Intent>

**TRIGGER:** When the user explicitly types `/reincarnate` followed by an intent string in the chat, you **MUST** natively execute the Continuity Pipeline without relying on external Python scraping scripts.

You are the active agent preparing to self-terminate. You MUST mechanically execute the following 4 steps sequentially:

1. **Extract Signal (The Flight Recorder):** Dynamically summarize the *entire* context and technical iterations of your current conversation session. Write this summary gracefully as a formatted Markdown log to `.agents/continuity/LAST_SESSION_FLIGHT_RECORDER.md`. Filter out colloquial fluff.
2. **Determine Project Edge (The Pulse):** Synthesize the immediate technical delta—what was explicitly finished, what is currently broken, and what is the exact next step. Write this exclusively to `.agents/continuity/CURRENT_PULSE.md`.
3. **Execute Gameplan (The Mandate):** Combine the context above with the user's explicit `<Commander's Intent>` parameter. Formulate a highly prescriptive, 3-step numbered battle plan for the *incoming* agent. Write this rigid instruction set to `.agents/continuity/REINCARNATION_GAMEPLAN.md`.
4. **Handoff (The Terminal Splice):** Your response output MUST conclude by explicitly instructing the user to: **"Close this IDE tab, open a completely fresh Antigravity session window, and wake up the incoming agent."** Do not proceed with any other coding actions.
