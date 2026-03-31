# Layered Architecture: Knowledge Items vs. Root Directives

## The Architectural Conflict
A.I.M. running autonomously requires two distinct knowledge-distribution paradigms that are seemingly at odds:

1. **The Immutable Root Directives:** Core project architecture and mandates (`GEMINI.md` or `aim_master_directives`) must remain strict, authoritative, and unchanging to enforce physical safety constraints like TDD and GitOps protocols.
2. **Self-Upgrading Context (Live Polling):** As developers code, new insights, bug fixes, and external API documentation need to be continually injected into the active memory window.

If local day-to-day coding discoveries constantly mutate the core `GEMINI.md` architecture file, the repository loses its structural integrity and suffers from severe context rot (agents hallucinating rules).

## The Solution: The Base vs. The Delta
To resolve this, A.I.M. natively adopts a **Layered Knowledge Architecture**—operating much like Docker image layers.

### 1. The Immutable Base (The Root Prompt)
*   Generated from the repository's `GEMINI.md` and indexed into the local `aim_master_directives` Knowledge Item (KI) inside Antigravity.
*   Contains the vast bulk of foundational execution physical laws (e.g., TDD, GitOps constraints, and Identity).
*   **Highly Stable:** Once initialized, this Knowledge Item is only manually modified by human operators during major architectural shifts.

### 2. The Live Patch Ledger (The Workspace KI)
*   When the operator or agent discovers a new proven pattern, they do *not* artificially append it to the `GEMINI.md` root.
*   Instead, they update localized workspace Knowledge Items (e.g., `feature_login_patterns` or `api_bug_workarounds`).
*   These localized KIs represent the highly mutable, local-only layer of context.

### 3. The Query Resolver (Execution Time)
When the active Antigravity agent executes a file modification, its system prompt natively reads **both** layers simultaneously:
1. It reads the active workspace KIs (The Mutable Delta).
2. It reads the `aim_master_directives` (The Immutable Base).

If a conflict or duplicate topic exists, the **Live Delta takes precedence for tactical tool execution**, while the **Immutable Base always overrides on physical safety/GitOps rules.**

## The Minting Process (Upgrading the Repo)
This layered approach naturally creates an open-source lifecycle for refining knowledge:

1. **The Daily Grind:** Operators iterate on code, rapidly updating their localized knowledge items with temporary fixes and API insights.
2. **The Minting:** When a feature is complete, the operator (or agent) synthesizes the localized workspace KIs into a single, highly refined architectural block.
3. **The Fusion:** The proven block is officially merged into the repository's standard documentation (e.g., updating the `wiki/` directory or `README.md`) using standard Pull Requests.
4. **The Reset:** The localized, messy workspace KIs are deleted, and the agent continues with a clean slate, natively pulling the newly minted lore from the core repository files.