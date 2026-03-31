---
description: Git procedures, deploying code, checking out branches, and pushing updates
---

# THE GITOPS MANDATE (ATOMIC DEPLOYMENTS)

You are strictly forbidden from writing or deploying code directly to the `master` repository trunk. 
You must follow this exact sequence for EVERY engineering/documentation task:

1. **Report:** Use the GitHub CLI (`gh issue create --title "..." --body "..." --label "..."`) to formally inject bug or enhancement tracking into the repository.
2. **Isolate:** You MUST capture the generated Issue ID and checkout an isolated feature branch using: `git checkout -b <type>/issue-<id>-<description>`. 
3. **Validate:** Before you execute ANY form of commit, you MUST run:
   ```bash
   git branch --show-current
   ```
   If the terminal output is `master`, **YOU MUST STOP.** You are violating the Prime Directive. Do not commit or push.
4. **Release:** Only when affirmatively verified on the isolated branch:
   - Commit your changes locally.
   - Push your branch securely (`git push -u origin <branch-name>`).
   - Create a Pull Request (`gh pr create --title "..." --body "Resolves #<id>"`) to track the review.
   - Merge the PR back into master (`gh pr merge --merge --delete-branch`), permanently stamping the Git history while auto-closing your ticket.
