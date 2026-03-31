# The Decoupled Brain & Obsidian Transport Layer

> ⚠️ **STATUS: CONCEPTUAL ARCHITECTURE (PHASE 33)**
> *This document outlines the architectural pivot from a monolithic local agent to a distributed cognitive system utilizing Obsidian as a zero-API transport layer.*

## The Monolithic Bottleneck

Currently, A.I.M. is a **monolithic architecture**. The "Hands" (the active coding agent manipulating the terminal) and the "Brain" (the 5-Tier Memory Refinement Pipeline) run on the exact same machine, within the same event loops, and draw from the same API quotas and rate limits.

This creates several fatal bottlenecks:
1. **API Exhaustion:** If the background Scribe attempts to summarize 50 turns of history, it can trigger a `MODEL_CAPACITY_EXHAUSTED` (429) rate limit, instantly paralyzing the active coding agent in the primary terminal.
2. **Compute Contention:** Running heavy vector embedding models or complex summarization prompts drains local GPU/CPU resources, slowing down the active development environment.
3. **The Cleanup Problem:** The active RAG database (`engram.db`) suffers from "ghost context" because deleting specific concepts from a compiled vector database is incredibly difficult without wiping the entire table.

## The Paradigm Shift: Decoupling Control & Data

To scale, A.I.M. must decouple the **Control Plane** (The coding agent) from the **Data Plane** (The memory pipeline). 

We will offload the Brain to a dedicated background server (e.g., a spare Mac Mini, a Raspberry Pi, or a cheap Cloud VPS), allowing it to process memory 24/7 on separate API keys without ever interrupting the developer.

### The Problem of Networking (The Merge Conflict)
Decoupling introduces a major networking challenge. If Machine A (The Hands) and Machine B (The Brain) are constantly reading and writing to the same `MEMORY.md` file or SQLite database, we will encounter severe race conditions and merge conflicts. 

Building a custom REST API, WebSocket server, or managing firewall rules and SSL certificates to handle this synchronization introduces massive, unnecessary overhead.

## The Solution: The Obsidian Transport Layer

Rather than building a custom networking layer, A.I.M. will use **Obsidian Sync** (or an automated Git backend) as a secure, "Zero-API" transport layer.

By structuring the A.I.M. memory system to output strictly as flat `.md` files, we gain the ability to use third-party folder-syncing tools to pass data between the physical machines.

### The Cross-Machine Workflow:

1. **The Hands (Machine A):** 
   The developer finishes a coding session. The A.I.M. CLI dumps the raw `session.json` chat log and a skeletal `.md` trace into a designated folder inside an Obsidian Vault (e.g., `Vault/AIM_Inbox/`).

2. **The Transport:** 
   Obsidian Sync (or a background Git hook) automatically encrypts the new files, pushes them to the cloud, and syncs them down to the secondary machine.

3. **The Brain (Machine B):** 
   A headless A.I.M. daemon runs continuously on the server, using a file-watcher (`watchdog`) on `Vault/AIM_Inbox/`. When a new session file arrives, the daemon triggers the 5-Tier Memory Pipeline (Scribe -> Archivist).

4. **The Ephemeral Subconscious:** 
   Instead of updating a monolithic database directly, the Brain writes the final distilled facts as hundreds of tiny, individual `.md` files into a hidden directory: `Vault/.engrams/`. It also updates the main `Vault/MEMORY.md`, which now serves purely as an "Index Card" pointing to those files.

5. **The Return:** 
   Obsidian Sync automatically pushes the newly generated `.engrams/` and updated `MEMORY.md` back to the developer's primary coding machine.

6. **The Rebuild:** 
   When the coding agent wakes up on Machine A, it runs `aim index`. This command drops the local `engram.db` tables and instantly rebuilds the vector database from the fresh `.md` files in `.engrams/`.

### Why this architecture wins:
* **Zero Custom Networking:** No open ports, no complex API routing, no auth tokens to manage between devices.
* **Effortless Cleanup:** Because the `engram.db` is now treated as an ephemeral, instantly-rebuildable cache, "deleting a memory" simply means deleting the `.md` file in the `.engrams/` folder.
* **The Visual Graph:** As a free byproduct of this architecture, the user can open their A.I.M. workspace in the Obsidian application and see a beautiful, interactive, real-time graphical representation of their project's entire subconscious memory.