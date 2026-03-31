---
description: Git procedures, deploying code, checking out branches, and pushing updates
---

# THE GITOPS MANDATE (ATOMIC DEPLOYMENTS)

You are strictly forbidden from writing or deploying code directly to the `main` branch. 
You must follow this exact sequence for EVERY engineering task:

1. **Report:** Use `aim bug "description"` (or equivalent issue tracker logic) to log bugs or enhancements.
2. **Isolate:** You MUST use `aim fix <id>` (or manual `git checkout -b fix/issue-id`) to checkout a unique, isolated terminal branch. 
3. **Validate:** Before you execute ANY form of commit, you MUST run:
   ```bash
   git branch --show-current
   ```
   If the terminal output is `main`, **YOU MUST STOP.** You are violating the Prime Directive. Do not push.
4. **Release:** Only when you have affirmatively verified you are on an isolated branch, you may use `aim push "Prefix: msg"` (or exact `git push` equivalent mapped to conventional commits) to deploy atomically.
