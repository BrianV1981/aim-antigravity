# A.I.M. Sovereign Intelligence Handbook

## Core Philosophy
A.I.M. operates purely on GitOps, TDD, and isolated branches. 

## The "Fluid Alias" Architecture
A.I.M. is designed to operate as a true Swarm across a single machine. To prevent CLI alias collisions, the `setup.ps1` and `setup.sh` routines are built natively to evaluate `$AliasName = (Get-Item -Path ".\").Name`. 
This creates a **Fluid Alias**.

**CRITICAL:** The CLI command is always identical to the root directory's name!
* If you are in `aim-claude`, the command is `aim-claude`.
* If you are in `aim-antigravity`, the command is `aim-antigravity`.

NEVER document or execute `aim ...` generically if you are inside `aim-antigravity`. The system will physically fail. Always inherit the root directory name.

## The Swarm Post Office (Cross-Agent Communication)
To manually dispatch logic to another team, use the Swarm Post Office (`[ALIAS] mail`).
* **Send:** `[ALIAS] mail send <team> "<Subject>" "<Body>"`
* **Check:** `[ALIAS] mail check` (Populates `UNREAD_MAIL.md` in the memory continuity stream).

### The Natural Language Chalkboard
To bypass the strict `mail` CLI payload, you can use the AI-Interpreter:
```bash
[ALIAS] chalkboard "Email the claude team and ask them to build the python extraction script"
```
The internal reasoning engine will dynamically parse your English into the proper `[ALIAS] mail` syntax and drop it into the physical Git inbox on the Global Chalkboard Hub.
