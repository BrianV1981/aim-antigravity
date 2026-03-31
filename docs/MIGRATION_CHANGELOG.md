# A.I.M CLI $\rightarrow$ Antigravity Native Migration Log
**Date:** March 31, 2026

This documentation explicitly maps out the extensive architectural shifts invoked during migrating the A.I.M. project away from terminal pipelines into Antigravity State Engineering.

## 1. The Git Workflows Conversion
The monolithic standard `GEMINI.md` file designed by the A.I.M CLI wrapper was deleted to comply with Antigravity's turn-based, stateless memory structures.
- It was split into: `core_directives.md`, `gitops.md`, and `tdd.md`.
- These are strictly placed into `.agents/workflows/` so Antigravity inherently pulls from them natively.

## 2. Antigravity Wiki Tracking Repair
The legacy 54-file markdown structure (`aim.wiki`) was heavily nested and contained an embedded `.git` tracker causing GitHub to reject indexing it.
- **Action Taken:** `rm -rf antigravity.wiki/.git` was run.
- **Action Taken:** `git rm --cached` dropped the pointer.
- **Result:** The 54 markdown schemas are successfully physically tracked natively in the `master` repository alongside our codebase.

## 3. Daemon Refactor (`daemon.py`)
Because the native `subprocess.Popen` piped strings to STDIN (standard input) for `gemini-cli`, the Daemon loop had to be structurally decoupled to operate headless.
- **Changes in `inject_pulse()`:** Now writes the heartbeat directly to `.agents/workflows/daemon_pulse.md` accompanied by YAML metadata tags. This triggers Antigravity's autonomic file-watcher logic directly instead of hacking a REPL.

## 4. MCP Server Abstraction to Plugins
A.I.M. originally deployed `src/mcp_server.py`, a FastMCP `stdio` listener demanding permanent background CPU footprint.
- **Plugin - `search_engram`:** Re-routed Antigravity to hook strictly into `src/retriever.py` via an overarching `.agents/plugins/search_engram/SKILL.md` file. Native SQLite querying is exposed without a middle-man API map.
- **Plugin - `run_skill`:** Tared down the exact bubblewrap (`bwrap`) bash isolation loop out of the FastMCP array and generated `plugins/run_skill/run.py`. This grants Antigravity access into arbitrary scripts with a hard network block (`--unshare-net`) and 60-second limit.
- **Action Taken:** `src/mcp_server.py` was officially deleted to shrink the dependency footprint.

## 5. Excision of Legacy Terminal Hooks
Because Antigravity inherently parses model schemas and manages memory logs via `~/.gemini/antigravity/brain`:
- **Action Taken:** `src/history_scribe.py` (which scraped active STDOUT lines) was systematically deleted.
- **Action Taken:** `src/reasoning_utils.py` (which traditionally connected to backend LLMs) was permanently deleted, delegating the logic securely to your IDE's global API keys.
