# Map: A.I.M. Prompt Injections

This document catalogs every system instruction and prompt injection hardwired into the A.I.M. OS. Use this map to understand the "Cognitive Persona" of each autonomous script and how they work together to maintain technical integrity.

---

## 1. Reincarnation & Continuity
These prompts manage the transition of "Will" and "State" between agent vessels.

| Script | Injection Point | Persona / Objective |
| :--- | :--- | :--- |
| `src/handoff_pulse_generator.py` | `generate_reincarnation_gameplan` | **The Reincarnation Strategist:** Analyzes the full session history tail (50k chars) to distill the project's heartbeat and draft rigid battle plans. |
| `src/handoff_pulse_generator.py` | `generate_handoff_pulse` | **The Continuity Engine:** Surgical technical scribe that identifies the "Project Edge" (What's finished, broken, or next). |
| `scripts/aim_reincarnate.py` | `wake_up_prompt` | **The Wake-up Mandate:** The first thing a new agent hears. Forces the reading of `GEMINI.md`, `HANDOFF.md`, and the `REINCARNATION_GAMEPLAN.md`. |

---

## 2. The Waterfall Memory Pipeline
These prompts govern the refinement of raw data into Durable Truth.

| Tier | Script | Persona / Objective |
| :--- | :--- | :--- |
| **Tier 1** | `hooks/session_summarizer.py` | **The Memory Proposer:** Analyzes technical deltas turn-by-turn to identify Adds, Removes, and Contradictions for `MEMORY.md`. |
| **Tier 2** | `src/memory_proposer.py` | **The Memory Architect:** Consolidates multiple hourly technical narratives into structured reasoning-backed proposals. |
| **Tier 3** | `src/daily_refiner.py` | **The Daily Cognitive Refiner:** Deduplicates and synthesizes Tier 2 proposals into a cohesive Daily State. |
| **Tier 4** | `src/weekly_consolidator.py` | **The Strategic Consolidator:** Elevates granular tasks into high-level project milestones and macro technical arcs. |
| **Tier 5** | `src/monthly_archivist.py` | **The Final Archivist:** Performs extreme context compaction and solidification of architecture into axioms. |
| **Merge** | `src/monthly_archivist.py` | **The Memory Merger:** Takes an ARC report and the current `MEMORY.md` to produce a full, updated candidate file. |

---

## 3. Executive Guardrails (Anti-Drift)
These prompts are injected *live* during a session to prevent behavioral degradation.

| Hook | Script | Objective |
| :--- | :--- | :--- |
| **Mantra** | `hooks/cognitive_mantra.py` | **The Mantra Protocol:** Forcefully halts execution after 50 actions and requires the agent to recite its full `GEMINI.md` system instructions to clear "Lost in the Middle" decay. |
| **Whisper** | `hooks/cognitive_mantra.py` | **The Subconscious Whisper:** Injects a silent reminder of mandates every 25 actions to nudge the agent back toward GitOps and TDD. |

---

## 4. Specialized Matrix Operations
Temporary personas used for focused sub-tasks.

| Script | Persona / Objective |
| :--- | :--- |
| `scripts/aim_delegate.py` | **The Specialized Sub-Agent:** A zero-filler analyst that provides binary or short-string answers for massive file processing. |
| `hooks/session_summarizer.py` | **The Eureka Protocol:** A hindsight-pruning heuristic that captures the exact moment of technical breakthrough. |

---

## 5. Development Utilities
Prompts used by the operator to setup or maintain the environment.

| Script | Objective |
| :--- | :--- |
| `scripts/aim_init.py` | **The Grok Profiler:** A highly-specific prompt used to scrape and mirror the Operator's personality traits from social history. |
