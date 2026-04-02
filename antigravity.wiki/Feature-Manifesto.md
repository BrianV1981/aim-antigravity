# The Pragmatic Approach: A.I.M. Feature Manifesto

This document provides a comprehensive, deep-dive index of every feature built into the A.I.M. (Actual Intelligent Memory) Operating System. 

## The Core Philosophy: Defeating "Needle in a Haystack"
The AI industry is currently obsessed with the "Needle in a Haystack" (NIAH) benchmark—brute-forcing 1-million or 2-million token context windows to see if a model can remember a single fact hidden deep inside a massive prompt. 

**This is a fundamentally flawed architecture for memory.** It treats data retrieval as a neural network problem when it is actually a solved *data engineering* problem. 

Force-feeding an LLM the entire 1,000-page Bible or a massive codebase just to find the word "Rosebud" is computationally wasteful, slow, and prone to hallucination (Context Rot). A.I.M. takes a pragmatic, engineering-first approach: A simple Python script chunks massive texts based on semantic Markdown headers, compresses them, and injects them into a highly structured `engram.db` SQLite system. 

When the A.I.M. agent needs to find the "needle," it doesn't read the whole haystack. It executes a deterministic Hybrid RAG (FTS5 + Semantic Vector) database query. The database instantly returns the exact 3 paragraphs needed. **It costs zero API tokens, runs in milliseconds, and it will never fail to find the needle.** A.I.M. replaces the need for massive context windows with structured, deterministic memory retrieval.

---

## 1. The Core Operating System (Exoskeleton)

*   **The CLI Router (`aim_cli.py`)**
    *   *What it is:* The primary entry point and nervous system of the OS. It routes commands, manages execution paths, and acts as the bridge between the user's terminal and the underlying Python architecture.
    *   *Why it is important:* It provides a unified, predictable interface. You don't have to remember 20 different Python scripts; you just type `aim <command>`.

*   **The Sovereign Cockpit / TUI (`aim_config.py`)**
    *   *What it is:* A rich, interactive Terminal User Interface (TUI) built with `questionary` and `rich`. It allows operators to configure LLM providers, set cognitive routing, adjust memory retention, and manage API keys without manually editing JSON files.
    *   *Why it is important:* It transforms A.I.M. from a collection of scripts into a polished, production-ready product that any developer can easily configure.

*   **The Hook Engine (`aim_router.py`)**
    *   *What it is:* An execution sandbox that aggressively catches exceptions and captures `stderr` and `stdout` from experimental background scripts.
    *   *Why it is important:* It implements the "SafeLoad" pattern. If an experimental memory hook or sub-module crashes, the Hook Engine catches the failure, logs it silently, and returns a safe fallback. The core agent session will *never* crash due to a broken plugin.

*   **The Background Daemon (`daemon.py` & `heartbeat.py`)**
    *   *What it is:* A persistent background process that maintains the A.I.M. heartbeat, manages execution loops, and monitors the environmental state of the workspace.
    *   *Why it is important:* It allows A.I.M. to perform asynchronous work (like memory distillation) while the main agent is actively coding in the terminal.

## 2. The Cascading Memory Engine

*   **Tier 1: Hourly Summarizer (`session_summarizer.py`)**
    *   *What it is:* A background process that constantly watches the native Gemini CLI chat logs. It extracts the raw conversational JSON, filters out noise, and writes technical narrative summaries of the agent's immediate actions.
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

## 3. The Engram Database & DataJack

*   **Hybrid RAG Retrieval (`retriever.py` & `forensic_utils.py`)**
    *   *What it is:* A local SQLite database utilizing the `sqlite-vec` extension. When the agent uses `aim search`, it queries the database using both Dense Vectors (Nomic Cosine Similarity for abstract concepts) and FTS5 (BM25 Lexical matching for exact variable names).
    *   *Why it is important:* It guarantees perfect recall. If an agent needs to know why a specific function was written 3 months ago, it finds it instantly.

*   **The DataJack Foundry (`aim_bake.py` & `aim_exchange.py`)**
    *   *What it is:* A mechanism for exporting specific cross-sections of the Engram database into compressed, immutable `.engram` files (Cartridges).
    *   *Why it is important:* It allows developers to infinitely share knowledge. You can bake a `django-best-practices.engram` cartridge and share it with the community. When another user "jacks in," their agent instantly inherits that exact knowledge.

*   **The SafeLoad Plugin Architecture (`datajack_plugin.py`)**
    *   *What it is:* An isolation layer around the heavy SQLite and vector embedding dependencies.
    *   *Why it is important:* If the local Ollama embedding engine goes offline or the database locks, the core OS gracefully degrades instead of hard-crashing.

## 4. Continuity & Failsafes

*   **The Failsafe Context Snapshot (`failsafe_context_snapshot.py`)**
    *   *What it is:* A hook that fires after every single tool call. It aggressively dumps the raw JSON array of the current conversation to a fallback file.
    *   *Why it is important:* If the terminal crashes mid-session, or your laptop dies, you don't lose the last hour of autonomous coding.

*   **The Handoff Pulse Generator (`handoff_pulse_generator.py`)**
    *   *What it is:* Generates a highly dense `CURRENT_PULSE.md` file when an agent reaches its context limit. It summarizes the exact technical state and explicitly lists the "Immediate Next Step."
    *   *Why it is important:* It acts as the "baton" passed between instances. A new agent waking up reads the Pulse and instantly resumes work without missing a beat.

*   **The Context Injector (`context_injector.py`)**
    *   *What it is:* An awakening protocol. It forcefully injects the `CURRENT_PULSE.md` and pending memory proposals into the AI's system prompt before it is allowed to speak.
    *   *Why it is important:* It establishes Epistemic Certainty. The agent cannot hallucinate its state because the OS forces it to read the truth before it boots.

## 5. Security & GitOps Deployment

*   **The GitOps Bridge (`aim_push.sh` & `aim_batch_merge.py`)**
    *   *What it is:* A strict workflow that physically prevents the agent from writing code on the `main` branch. It forces the use of `aim bug`, `aim fix <id>`, and atomic deployments via `aim push`.
    *   *Why it is important:* Autonomous agents will destroy codebases if left unconstrained. This ensures every change is isolated, reviewed, and cleanly merged.

*   **Decoupled Sovereign Sync (`sovereign_sync.py`)**
    *   *What it is:* Translates the binary SQLite database into plain-text JSONL files so the agent's memory can be committed to GitHub and synced across machines. This process spawns as a non-blocking background daemon.
    *   *Why it is important:* It prevents database locks from freezing deployments, ensuring you can push your code to GitHub instantly while the OS manages memory backups in the background.

*   **The Secret Shield (`secret_shield.py`)**
    *   *What it is:* A Data Loss Prevention (DLP) hook that scans execution pathways and outputs for accidental exposure of API keys or credentials.
    *   *Why it is important:* Prevents autonomous agents from accidentally logging your production database passwords to a public GitHub repo.

## 6. Integrations & Extensions

*   **The Universal MCP Server (`mcp_server.py`)**
    *   *What it is:* A Model Context Protocol server that runs in the background. It allows IDEs like Cursor or VS Code Copilot to natively query the A.I.M. Engram database.
    *   *Why it is important:* It breaks A.I.M. out of the terminal. If you prefer to write code by hand in VS Code, your IDE's AI assistant can still access your project's permanent memory.

*   **The Obsidan Bridge (`obsidian_sync.py`)**
    *   *What it is:* Synchronizes local A.I.M. data directly into a local Obsidian vault.
    *   *Why it is important:* Allows human operators to read, search, and visualize the AI's memories in a beautiful markdown interface.

*   **The "Clean Sweep" Installer (`aim_init.py`)**
    *   *What it is:* A robust setup utility that can bootstrap a new project or perform a "Clean Sweep" to safely strip away internal A.I.M. meta-documentation when dropping the OS into a fresh repository.
    *   *Why it is important:* Ensures A.I.M. doesn't suffer an identity crisis when deployed as a template.