---
description: Initialize agent Brain by ingesting GEMINI.md into the local KI database
---
# /init

This is the Bootstrap Script for any fresh Antigravity agent opening this project.
When the user types `/init`, you MUST perform the following exact steps chronologically and mechanically:

1. **Read the Source:** Look for `GEMINI.md` at the root of this exact repository. Use the `view_file` tool to read the entire file into your active context.
2. **Execute Ingestion:** You must immediately create a new local Knowledge Item specifically named `aim_master_directives` in your local OS's native `appDataDir\knowledge` folder (`~/.gemini/antigravity/knowledge` or `C:\Users\<user>\.gemini\antigravity\knowledge`).
   - Use `write_to_file` to create `metadata.json` citing "Master A.I.M. Core Directives" referencing `/GEMINI.md`.
   - Use `write_to_file` to create `artifacts/content.md` containing the pure verbatim text you read from `GEMINI.md`.
3. **Report:** Provide a clean markdown Walkthrough stating that the agent's Brain has been successfully bootstrapped with the `GEMINI.md` Directives. Remind the user that these directives are now permanently active for this machine.
