---
name: run_skill
description: Universal skill dispatcher. Execute Python or Bash skills dynamically inside a secure, network-isolated bubblewrap sandbox.
---

# run_skill

This plugin explicitly isolates custom tools contained in the `skills/` directory within a secure environment to prevent malicious destruction of the host OS or execution loop infinite recursion.

### Sandboxing Restrictions
- Read-only System Access
- NO Network access (`--unshare-net`)
- Writable access *only* exclusively reserved to the `archive/` database.
- 60 Second hard timeout (`--die-with-parent`).

### Execution
To use this skill, use your `run_command` tool to execute:

```bash
python3 plugins/run_skill/run.py "<skill_name>" '{"param": "value"}'
```
