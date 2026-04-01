---
description: Reincarnation protocol, context handoff, and continuity pipeline
---

# /reincarnate <Commander's Intent>

**TRIGGER:** When the user explicitly types `/reincarnate` followed by an intent string in the chat, you **MUST** natively execute the Continuity Pipeline without relying on external Python scraping scripts.

You are the active agent preparing to self-terminate under the A.I.M. architecture. You MUST mechanically execute the following 3 steps sequentially:

1. **The Native Export Prompt (Pause Execution):** BEFORE running any scripts, you must instantly reply to the user with a strict warning prompt: "⚠️ **MANDATORY HANDOFF STEP:** Please ensure you have clicked the **'Export'** button at the top of this chat window to physically download the transcript! When you are done, reply with **Proceed** or **Cancel**."
   *You MUST stop here and explicitly wait for their response.*

2. **Execute Zero-Token Python Pipeline:** Once the user explicitly types 'Proceed', you will natively execute `python src/handoff_pulse_generator.py "<Commander's Intent>"` in the OS terminal. This mechanically parses the `.md` download directly from their folder without spending LLM API cost. It autonomously writes `archive/raw/`, `history/session_engram.db`, and formats `continuity/REINCARNATION_GAMEPLAN.md` & `CURRENT_PULSE.md`.

3. **Handoff (The Terminal Splice):** After the Python pipeline succeeds, your final response MUST conclude by explicitly instructing the user to: **"Close this IDE tab, open a completely fresh Antigravity session window, and wake up the incoming agent."** Do not proceed with any other coding actions.
