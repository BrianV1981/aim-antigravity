---
description: Reincarnation protocol, context handoff, and continuity pipeline
---

# /reincarnate <Commander's Intent>

**TRIGGER:** When the user explicitly types `/reincarnate` followed by an intent string in the chat, you **MUST** natively execute the Continuity Pipeline without relying on external Python scraping scripts.

You are the active agent preparing to self-terminate. You MUST mechanically execute the following 4 steps sequentially:

1. **Execute Zero-Token Python Pipeline:** Natively execute `python src/handoff_pulse_generator.py "<Commander's Intent>"` in the OS terminal. This single command mechanically parses the `.system_generated/logs/` string without spending any LLM API cost. It autonomously writes `continuity/LAST_SESSION_FLIGHT_RECORDER.md`, scrapes the tail-end metrics into `continuity/CURRENT_PULSE.md`, and natively formats `continuity/REINCARNATION_GAMEPLAN.md`.
2. **Handoff (The Terminal Splice):** After the Python pipeline succeeds, your response output MUST conclude by explicitly instructing the user to: **"Close this IDE tab, open a completely fresh Antigravity session window, and wake up the incoming agent."** Do not proceed with any other coding actions or attempt to manually read the generated documents.
