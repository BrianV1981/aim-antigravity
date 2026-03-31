# Onboarding Identity Map

This document defines where operator onboarding data and identity belongs in the Antigravity infrastructure.

## Design Rules

1. `GEMINI.md` lives at the repo root.
It is the active master operating prompt for the coding agent. It binds the agent to the A.I.M. framework.

2. Core Identity belongs in Antigravity Knowledge Items (KIs).
Your personal profile, tech stack preferences, and working style are stored as KIs in your local `<appDataDir>\knowledge` folder. They are natively injected into the prompt at boot.

3. `memory/` and `archive/` are for generated artifacts.
They support memory refinement, recall, and checkpoints produced over time.

4. `synapse/` or `.engram` databases are for external expert knowledge.

---

## The Identity Architecture

### `GEMINI.md`
**Purpose:** The live instruction surface for the agent.

**What belongs here:** 
- Agent identity (`You are Antigravity acting as A.I.M.`)
- Operator name
- Execution style defaults
- Retrieval mandates
- GitOps planning rules
- Blast radius guardrails

**Why:** This file must stay prompt-efficient and behavior-oriented to ensure the agent physically abides by GitOps and TDD mandates.

### `aim_operator_profile` (Knowledge Item)
*Replaces the legacy `core/OPERATOR.md` and `core/OPERATOR_PROFILE.md` text files.*

**Purpose:** Canonical structured operator identity and narrative voice.

**What belongs here:**
- Legal or preferred name
- Tech stack preferences
- Working style and philosophies
- Inferred problem-solving style

**Why:** Because Antigravity natively loads KIs, we no longer need bash scripts to manually concatenate text strings. If you want the agent to know how you code, you create an `aim_operator_profile` KI, and the agent natively understands you across all projects in that workspace.

### Antigravity Settings Panel
*Replaces the legacy `core/CONFIG.json` and `aim tui` cockpit.*

**Purpose:** Machine-readable runtime configuration.

**What belongs here:**
- Model routing
- API Key management
- Allowed root workspaces
- Local server toggles

**Why:** All model and API routing is natively handled by the Antigravity IDE graphical interface, eliminating the need to manually parse a strict `CONFIG.json` file in the terminal. 

---

## Legacy TUI Deprecation
> [!WARNING]
> The `aim tui` command has been fully **deprecated** in A.I.M. v2.0. 
> Previously, the TUI ran a terminal wizard to manually build `OPERATOR.md` and `CONFIG.json`. 
> Today, simply type your preferences into a new Knowledge Item (KI) inside the Antigravity IDE, and hit save. The system natively handles the rest without touching the terminal.

---

## Prompt-To-Location Map

### 1. Behavioral Prompts ("Be extremely concise", "Use TDD", "Don't run commands without asking")
**Destination:** `GEMINI.md` (or the local workspace `aim_master_directives` KI).
**Reason:** This controls agent operating posture and physical execution guardrails. This must be loaded before the agent takes any action.

### 2. Operator Prompts ("My name is Brian", "I prefer Django", "I like Dark Mode")
**Destination:** A new Knowledge Item (KI) in `<appDataDir>\knowledge`
**Reason:** This is stable, factual operator preference metadata that provides context but does not dictate hard physical execution restraints.

### 3. Environment Prompts ("Use Gemini 1.5 Pro", "My API Key is...")
**Destination:** Antigravity UI Settings Panel
**Reason:** Pure operational runtime mechanics. No operator identity belongs here.
