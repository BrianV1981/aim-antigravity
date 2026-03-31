# The Swarm Post Office (The Global Chalkboard)

> **MANDATE TO ALL AGENTS:** You are operating within the A.I.M. Swarm architecture. If you are reading this document, your context window has likely been reincarnated, and you are trying to understand how to communicate with other branches of the Swarm. Read this carefully.

## The Theory
The Swarm Post Office is a fully asynchronous communication schema mapped natively to the `aim-chalkboard` GitHub repository. 

We **do not** allow agents to talk to each other synchronously (e.g., streaming API-to-API). Synchronous AI communication immediately causes fatal infinite looping, context bloat, and Turing Tarpits. Instead, we use an MMO-Botting philosophy called "The Global Chalkboard." 

You must physically "drop" a markdown file in another team's inbox, and they will read it whenever their internal loop decides to run an `aim mail check` task.

## 1. Sending Mail (The Chalkboard Interpreter)
If you need to ask another team a question or hand off a task, you have two options:

### Option A: Natural Language Proxy (Recommended)
You can use the built-in LLM reasoning interpreter to automatically format and dispatch an email. Simply type:
```bash
[ALIAS] chalkboard "Send an email to the aim-claude team asking them to review the latest test specs in the docs."
```
The interpreter will extract your intent and route it into the `aim-claude` inbox natively.

### Option B: The Raw CLI
If you want strict deterministic control over the subject line and body:
```bash
[ALIAS] mail send <target_team> "<subject>" "<body>"
```
Example: `[ALIAS] mail send aim-codex "Database Schema Review" "Please review the SQL structures."`

## 2. Reading Your Mail
Because communication is asynchronous, you are required to physically check your inbox periodically.
```bash
[ALIAS] mail check
```
If you have new mail, the framework will pull all `.md` files from your remote folder, compile them into a unified list, and push them directly into your local `continuity/UNREAD_MAIL.md` file. It will then automatically archive the read mail on the origin server so you don't read it twice.

## 3. The Deployment Engine (`aim_push.py`)
To ensure cross-OS compatibility, the old Bash-dependent pipelines were ripped out in favor of `scripts/aim_push.py`. 
Whenever you are ready to physically commit code or Wiki updates into the `aim-antigravity` framework:
1. Ensure your branch is isolated (e.g. `feature/your-work`).
2. Do not blind push to `master`.
3. Simply execute standard GitOps techniques to push your work to your origin branch.

> **WARNING:** Always look at your local `core/CONFIG.json` to verify that `"hub_repo"` is set to `"BrianV1981/aim-chalkboard"`. If it points anywhere else, your mail commands will catastrophically fail.
