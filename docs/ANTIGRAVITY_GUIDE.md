# Antigravity — Architecture & Customization Guide

This document outlines how Antigravity (your AI agent) builds its context and how you can mold it to fit your workflow.

## 1. Loadup Sequence

Antigravity is completely stateless between individual turns. Every time a prompt is submitted, an orchestration engine builds a contextual payload and injects it into the system prompt.

At the start of **every single request**, Antigravity is injected with:
- **Base Directives:** Core identity, operating behavior, formatting rules, and tool capabilities.
- **Operator Context:** OS information (`Windows`), workspace roots, app directory (`C:\Users\kingb\.gemini\antigravity`), active files in the editor, and cursor position.
- **Knowledge Base (KIs):** Summaries of past learned patterns from the local Knowledge database.
- **Custom Rules & Workflows:** Explicit global configuration rules and repo-level workflow procedures.

## 2. Where is the `GEMINI.md`?

**Antigravity does not use a hardcoded equivalent to `CLAUDE.md`.**

It does not automatically scan the root of your repo for a `gemini.md` or `antigravity.md` on startup. Instead, instructions are pulled from a structured hierarchy of customizable layers.

## 3. How to Customize Antigravity

To enforce rules, teach frameworks, or guide behavior, use these three mechanisms in order of precedence:

### A. Global Custom Rules (The Baseline)
You can define Custom Rules directly in your IDE/Extension settings. These rules are injected into the core system prompt on *every request* across *every project*.
> [!TIP]
> **Use for:** Broad operating directives (e.g., "Always use TDD", "Never use Tailwind", "Speak bluntly and use no jargon").

### B. Workflows (Repository-Level Guidelines)
To provide repo-specific Standard Operating Procedures (like "how to manage migrations", "release processes", or "architectural boundaries"), use the **Workflows** system.

**Implementation:**
Create a folder in your workspace root named `.agents/workflows/` (or `.agent/workflows/`). Inside, place individual `.md` files for distinct tasks:

```yaml
---
description: How to push code and release in this repo
---

1. Never commit to main.
2. Use the `aim-claude bug -> fix -> push` flow.
```

Antigravity automatically loads these files when executing instructions that conceptually match the `description` header.

### C. The Knowledge System (KIs/Memory)
When completing complex tasks or establishing architectural patterns, that information is distilled into a Knowledge Item (KI) stored persistently at `C:\Users\kingb\.gemini\antigravity\knowledge`.

Antigravity is mandated to review these KIs natively *before* writing code, acting as local memory to prevent repeating the same mistakes across different sessions.

## 4. Cross-Platform Consistency (Windows vs Linux)

Antigravity’s core architecture and customization mechanisms are OS-agnostic because they are powered by the same underlying engine and IDE interface. If you move your workflow from Windows to a native Linux or macOS environment, the customization behavior is identical.

### 🟢 What is Exactly the Same
1. **The Interface:** You manage Global Custom Rules through the exact same IDE settings menus.
2. **Workflows:** The repository-level rules work identically. The `.agents/workflows/` folder travels with your repo, and Antigravity will read it automatically regardless of the OS.
3. **The Logic:** The orchestration engine processes your context the exact same way.

### 🟡 The ONLY Difference: The File Path
The single difference between Windows and Linux is where the system stores its persistent, localized brain (KIs, memory, logs):
- **Windows:** `C:\Users\<user>\.gemini\antigravity\`
- **Linux / macOS:** `~/.gemini/antigravity/` (e.g., `/home/<user>/.gemini/antigravity/`)

---

## Summary: A.I.M. Optimization
If you want Antigravity to perfectly mirror the baseline set by `CLAUDE.md` and `REINCARNATION_GAMEPLAN.md`:
1. Put broad communication and testing mandates into global **Custom Rules**.
2. Put the GitOps flow and `aim-claude` CLI commands into `.agents/workflows/gitops.md`.
