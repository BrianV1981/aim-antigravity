---
name: search_engram
description: Search the A.I.M. Engram DB for historical technical knowledge, architectural decisions, and project mandates.
---

# search_engram

This plugin allows you (Antigravity) to query the local Hybrid RAG SQLite database natively.

### Execution
To use this skill, use your `run_command` tool to execute the native retriever script:

```bash
python3 src/retriever.py "<your query>" --full
```

**(Note: Do NOT try to read the SQLite database natively using SQL commands. Always use this retrieval script to automatically benefit from the semantic vectorization and lexical dual-search algorithms).**
