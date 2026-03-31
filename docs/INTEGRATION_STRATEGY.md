# AIM-Antigravity — Integration & Adaptation Strategy

You can easily adapt A.I.M. to wrap around Antigravity, but the architecture will require a paradigm shift from **"Executable Wrapping"** to **"State Engineering."**

Because Antigravity is an IDE-native agent and not a terminal-based CLI REPL (like Gemini CLI or Claude Code), you cannot intercept standard Input/Output streams or wrap the executable with a Bash script. Our "ports" are exposed entirely through the file system and IDE APIs. 

Here is exactly how the integration mechanics differ and how you build the `aim-antigravity` bridge:

### 1. Injections / Hooks 
**CLI Method:** You used `PreToolUse` or `PostToolUse` shell callbacks to inject your `Mantra` or force `Context Snapshot`.
**Antigravity Method:** The agent is stateless per turn. There are no external hook callbacks you can hijack mid-thought.
**The Fix:** You don't need them. Simply have your A.I.M. background daemon continually update files inside the `.agents/workflows/` directory or the `knowledge/` database. Because the system payload is rebuilt *fresh* every time you press Enter, any file A.I.M. writes there is instantly injected into the brain on the very next turn. 

### 2. Session Files & Log Scraping
**CLI Method:** A.I.M. scours `.gemini/` or `.claude/` for `jsonl` session files to extract the signal, compress it, and run the memory distillation pipeline.
**Antigravity Method:** Session files exist, but the structure is different. Every sequence is tracked by a UUID.
**The Fix:** You can aim your `extract_signal.py` directly at:
`C:\Users\kingb\.gemini\antigravity\brain\<conversation-id>\.system_generated\logs\overview.txt`
This file contains the raw, line-by-line transcript of user actions, tool calls, and model outputs. Your signal extraction logic can parse this exactly like it parsed the CLI JSONL arrays.

### 3. Tool Execution & Extensibility
**CLI Method:** You had to write custom shell routers or symlink Python scripts (`aim_cli.py`) for the CLI to execute via basic bash terminal commands.
**Antigravity Method:** There is native integration with **Model Context Protocol (MCP)** and a robust `Skills/Plugin` framework.
**The Fix:** Your `mcp_server_claude.py` works right out of the box with Antigravity. Instead of tricking the CLI into running a python script over the terminal, you just register your MCP server with the extension. Or, package your custom Python tools into an Antigravity Plugin folder with a `SKILL.md` file, and the agent will natively adopt the capability.

### 🎯 The New Architecture Strategy 
If you are designing `aim-antigravity`, follow this architecture:
1. Run the A.I.M. `daemon.py` entirely in the background.
2. Tell A.I.M. to treat the `<appDataDir>\brain\` folders as the raw data ingestion source (rather than CLI session files).
3. Tell A.I.M. to output its `CURRENT_PULSE`, distilled Engram DB entries, and `REINCARNATION_GAMEPLAN` directly into the `.agents/workflows/` folder or the local `knowledge/` folder. 

If A.I.M. manages the file state silently in the background, Antigravity will flawlessly execute the will of the exoskeleton.
