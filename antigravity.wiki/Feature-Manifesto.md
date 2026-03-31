# The Pragmatic Approach: A.I.M. Feature Manifesto

This document provides a comprehensive, deep-dive index of every feature built into the A.I.M. (Actual Intelligent Memory) Operating System. 

## The Core Philosophy: Defeating "Needle in a Haystack"
The AI industry is currently obsessed with the "Needle in a Haystack" (NIAH) benchmark—brute-forcing 1-million or 2-million token context windows to see if a model can remember a single fact hidden deep inside a massive prompt. 

**This is a fundamentally flawed architecture for memory.** It treats data retrieval as a neural network problem when it is actually a solved *data engineering* problem. 

Force-feeding an LLM the entire 1,000-page Bible or a massive codebase just to find the word "Rosebud" is computationally wasteful, slow, and prone to hallucination (Context Rot). A.I.M. takes a pragmatic, engineering-first approach: Background Python scripts chunk massive texts based on semantic Markdown headers, compress them, and inject them into a highly structured `engram.db` SQLite system. 

When the A.I.M. agent needs to find the "needle," it doesn't read the whole haystack. It executes a deterministic [Hybrid RAG](Feature-Hybrid-RAG.md) (FTS5 + Semantic Vector) database query. The database instantly returns the exact 3 paragraphs needed. **It costs zero API tokens, runs in milliseconds, and it will never fail to find the needle.** A.I.M. replaces the need for massive context windows with structured, deterministic memory retrieval.

---

## 1. The Core Operating System (Exoskeleton)

*   **[DEPRECATED] The CLI Router (`aim_cli.py`)**
    *   *Previously:* The primary entry point routing terminal commands.
    *   *Now:* Replaced entirely by Google Antigravity. Operations are now native IDE workflow interactions or Slash Commands.

*   **[DEPRECATED] The Sovereign Cockpit / TUI (`aim_config.py`)**
    *   *Previously:* An interactive Terminal User Interface (TUI) for configuring API keys and routing.
    *   *Now:* Replaced by the Antigravity Settings interface. Agents inherently use the workspace's configured model logic without manual JSON text-file hacks.

*   **The Hook Engine (`aim_router.py`)**
    *   *What it is:* An execution sandbox that aggressively catches exceptions and captures `stderr` and `stdout` from experimental background scripts.
    *   *Why it is important:* It implements the "SafeLoad" pattern. If an experimental memory hook or sub-module crashes, the Hook Engine catches the failure, logs it silently, and returns a safe fallback. The core agent session will *never* crash due to a broken plugin.

*   **The Background Daemon (`daemon.py` & `heartbeat.py`)**
    *   *What it is:* A persistent background process that maintains the A.I.M. heartbeat, manages execution loops, and monitors the environmental state of the workspace.
    *   *Why it is important:* It allows A.I.M. to perform asynchronous work (like memory distillation) while the main Antigravity agent is actively coding.

## 2. The [Cascading Memory](Feature-Cascading-Memory.md) Engine

*   **Tier 1: Hourly Summarizer (`session_summarizer.py`)**
    *   *What it is:* A background process that constantly watches chat logs. It extracts the raw conversational JSON, filters out noise, and writes technical narrative summaries of the agent's immediate actions.
    *   *Why it is important:* It prevents the agent from losing its train of thought over a multi-hour session.

*   **Tier 2: Memory Proposer (`memory_proposer.py`)**
    *   *What it is:* Analyzes the hourly summaries and proposes structured delta updates (Adds/Removes/Modifications) to the long-term `MEMORY.md` state file.
    *   *Why it is important:* It translates unstructured chat narratives into actionable, structured architectural facts.

*   **Tier 3 & 4: Daily & Weekly Consolidators (`daily_refiner.py`, `weekly_consolidator.py`)**
    *   *What it is:* Processes that deduplicate and distill days or weeks of tactical debugging into high-level project milestones and permanent architectural shifts.
    *   *Why it is important:* It prevents the long-term memory from bloating. It compresses a 3-day struggle with a CORS error into a single rule: "Always set CORS headers in middleware."

*   **Tier 5: Monthly Archivist (`monthly_archivist.py`)**
    *   *What it is:* Compresses long-term, stable architecture into dense, factual axioms and archives stale context that is no longer relevant.
    *   *Why it is important:* Keeps the active `engram.db` lean, ensuring that search queries remain fast and highly relevant.

## 3. The Engram Database & [DataJack](The-DataJack-Protocol.md)

*   **[Hybrid RAG](Feature-Hybrid-RAG.md) Retrieval (`retriever.py` & `forensic_utils.py`)**
    *   *What it is:* A local SQLite database. The agent can query the database using both Dense Vectors (Cosine Similarity for abstract concepts) and FTS5 (BM25 Lexical matching for exact variable names).
    *   *Why it is important:* It guarantees perfect recall. If an agent needs to know why a specific function was written 3 months ago, it finds it instantly.

*   **The [DataJack](The-DataJack-Protocol.md) Foundry (`aim_bake.py` & `aim_exchange.py`)**
    *   *What it is:* A mechanism for exporting specific cross-sections of the Engram database into compressed, immutable `.engram` files (Cartridges).
    *   *Why it is important:* It allows developers to infinitely share knowledge. You can bake a `django-best-practices.engram` cartridge and share it with the community. When another user "jacks in," their agent instantly inherits that exact knowledge.

*   **The SafeLoad Plugin Architecture (`datajack_plugin.py`)**
    *   *What it is:* An isolation layer around the heavy SQLite and vector embedding dependencies.
    *   *Why it is important:* If the local Ollama embedding engine goes offline or the database locks, the core OS gracefully degrades instead of hard-crashing.

## 4. Continuity & Failsafes

*   **The Failsafe Context Snapshot (`failsafe_context_snapshot.py`)**
    *   *What it is:* A hook that fires after every single tool call. It aggressively dumps the raw JSON array of the current conversation to a fallback file.
    *   *Why it is important:* If the IDE crashes mid-session, or your laptop dies, you don't lose the last hour of autonomous coding.

*   **The Handoff Pulse Generator (`handoff_pulse_generator.py`)**
    *   *What it is:* Generates a highly dense `CURRENT_PULSE.md` file when an agent reaches its context limit. It summarizes the exact technical state and explicitly lists the "Immediate Next Step."
    *   *Why it is important:* It acts as the "baton" passed between instances. A new agent waking up reads the Pulse and instantly resumes work without missing a beat.

*   **The Context Injector (`context_injector.py`)**
    *   *What it is:* An awakening protocol. It forcefully injects the pending memory proposals into the AI's system workspace before it boots up.
    *   *Why it is important:* It establishes Epistemic Certainty. The agent cannot hallucinate its state because the OS forces it to read the truth before it executes.

## 5. Security & GitOps Deployment

*   **The [GitOps Bridge](Feature-GitOps-Bridge.md)**
    *   *What it is:* A strict workflow natively enforced through Antigravity that prevents the agent from writing unreviewed code on the `main` branch. It forces the use of isolated branches for all features and bugs.
    *   *Why it is important:* Autonomous agents will destroy codebases if left unconstrained. This ensures every change is isolated, reviewed, and cleanly merged.

*   **Decoupled Sovereign Sync (`sovereign_sync.py`)**
    *   *What it is:* Translates the binary SQLite database into plain-text JSONL files so the agent's memory can be committed to GitHub and synced across machines.
    *   *Why it is important:* It prevents database locks from freezing deployments.

*   **The Secret Shield (`secret_shield.py`)**
    *   *What it is:* A Data Loss Prevention (DLP) hook that scans execution pathways and outputs for accidental exposure of API keys or credentials.
    *   *Why it is important:* Prevents autonomous agents from accidentally logging your production database passwords.

## 6. Integrations & Extensions

*   **[DEPRECATED] The Universal MCP Server (`mcp_server.py`)**
    *   *Previously:* Exposed A.I.M. data to Cursor or VS Code.
    *   *Now:* Antigravity natively integrates into the workspace files directly, making proxy servers unnecessary.

*   **The Obsidan Bridge (`obsidian_sync.py`)**
    *   *What it is:* Synchronizes local A.I.M. data directly into a local Obsidian vault.
    *   *Why it is important:* Allows human operators to natively read and search the AI's internal databases in a beautiful UI.

*   **[DEPRECATED] The "Clean Sweep" Installer (`aim_init.py`)**
    *   *Previously:* A setup utility running in the terminal.
    *   *Now:* Fully absorbed by the Antigravity `/init` slash command.