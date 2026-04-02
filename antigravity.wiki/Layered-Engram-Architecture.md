# Layered Engram Architecture: Tier 4 Deep Memory

> 🔴 **STATUS: TARGET ARCHITECTURE (DECAPITATED).** This document maps the advanced features for Tier 4 Knowledge Distribution. Currently, in `aim-antigravity`, the underlying Daemons (`aim watch`) and DataJack Swarm plugins (`aim exchange`) are broken/missing (Issues #42 and #49). This document serves as the target blueprint for rebuilding them in the Antigravity native environment.

## The Architectural Conflict
A.I.M. is driving toward two advanced knowledge-distribution features that are seemingly at odds:

1. **The Decentralized DataJack Registry (Phase 38):** `.engram` cartridges should be immutable, mathematically hashed SQLite binaries shared via a peer-to-peer network. This requires the file to be static.
2. **Self-Upgrading Engrams (Live IDE Polling):** Tier 5 Autonomic Hooks should scrape GitHub and forums to inject new bug fixes into the local knowledge base. This requires the file to be highly mutable.

If local background hooks mutate the shared `.engram` files, they break the cryptographic hash, destroying the swarm and fragmenting the community's knowledge base.

## The Solution: The Base vs. The Delta
To resolve this, Tier 4 Deep Memory must adopt a **Layered RAG Architecture**—operating much like Docker image layers or Linux package managers (LTS core + daily security patches).

### 1. The Immutable Base (The Master Cartridge)
*   Generated via the DataJack `aim bake` workflow.
*   Contains the vast bulk of foundational documentation (e.g., `django-v5-core.engram`).
*   **Read-Only:** Once generated, this local SQLite table/file cannot be modified by the local workspace.
*   **Decentralized:** Because it is static, its hash is permanent, making it perfect for seeding to the decentralized registry.

### 2. The Live Patch Ledger (The Mutable Delta)
*   Managed by the Tier 5 Autonomic processor (formerly the `aim watch` daemon).
*   When the processor scrapes new solutions from GitHub, it does **not** insert them into the core cartridge.
*   Instead, it inserts the vectorized data into a highly mutable, local-only SQLite table called `live_deltas` (or writes them to a designated `synapse/live_feed/` text directory).

### 3. The Query Resolver (Execution Time)
When the active AI agent executes an explicit memory recall (e.g., via the retrieval tools), the script queries **both** layers simultaneously:
1. It searches the `live_deltas` table.
2. It searches the read-only Base Cartridges.
If a conflict or duplicate topic exists, the **Live Delta takes precedence**, effectively "patching" the outdated knowledge in the Base Cartridge at runtime.

## The Community Minting Process
This layered approach naturally creates an open-source lifecycle for knowledge:

1. **The Daily Grind:** 1,000 operators run the autonomic loops locally. Over 6 months, their `live_deltas` databases fill up with hundreds of new bug fixes.
2. **The Minting:** A community maintainer decides it is time for an official release. They execute a merge sequence:
   `aim bake --merge-deltas django-v5.1.engram`
3. **The Fusion:** The script takes the old immutable base, merges all the proven solutions from the `live_deltas` table, and mints a brand-new, officially hashed `.engram` file.
4. **The Reset:** The new cartridge is distributed. Users load it via DataJack injection, which automatically wipes their local `live_deltas` table clean to begin the cycle anew.

## Implementation Requirements (For Restoration)
*   Update `src/forensic_utils.py` and the database schema to isolate core data from live delta data.
*   Modify `src/retriever.py` to prioritize `live_deltas` results over core results in the final FTS5/Vector ranking algorithm when the DataJack modules are eventually ported.