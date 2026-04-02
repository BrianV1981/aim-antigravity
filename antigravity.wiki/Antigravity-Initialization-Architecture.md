# Antigravity Initialization Architecture

> **Purpose:** This page documents everything about how A.I.M. agents initialize, maintain continuity, and persist knowledge inside the Antigravity IDE. It captures the underlying philosophy, the specific system mechanics, and the reasoning behind every design decision made during the April 1, 2026 architecture session.
>
> **Audience:** Brian Vasquez (operator) and any future A.I.M. agent that needs to understand or modify the initialization system.

---

## Table of Contents
1. [How Antigravity Loads an Agent](#1-how-antigravity-loads-an-agent)
2. [The GEMINI.md Rule — What It Is and How It Behaves](#2-the-geminimd-rule--what-it-is-and-how-it-behaves)
3. [The Knowledge Item (KI) System](#3-the-knowledge-item-ki-system)
4. [The Five-Tier Cognitive Architecture](#4-the-five-tier-cognitive-architecture)
5. [The Boot Sequence — PRE-FLIGHT LOCKOUT](#5-the-boot-sequence--pre-flight-lockout)
6. [The Daisy Chain Problem and How We Solved It](#6-the-daisy-chain-problem-and-how-we-solved-it)
7. [The Flight Recorder — Why It's Opt-In](#7-the-flight-recorder--why-its-opt-in)
8. [The /init Command — One-Time Onboarding](#8-the-init-command--one-time-onboarding)
9. [The /sync Command — Re-Calibration](#9-the-sync-command--re-calibration)
10. [Command Reference](#10-command-reference)
11. [Decision Log](#11-decision-log)
12. [What to Change and Where](#12-what-to-change-and-where)

---

## 1. How Antigravity Loads an Agent

When you open a project in Antigravity and start a conversation, the following happens in order before you type a single word:

```
┌─────────────────────────────────────────────┐
│           ANTIGRAVITY BOOT SEQUENCE          │
├─────────────────────────────────────────────┤
│ 1. System Prompt: user_rules injected        │
│    → GEMINI.md content (every prompt)        │
│                                              │
│ 2. KI Summaries: surfaced in context header  │
│    → metadata.json summaries for all KIs     │
│                                              │
│ 3. Conversation History: prior turns loaded  │
│    → Limited to active context window        │
│                                              │
│ 4. Active File Context: open documents       │
│    → Cursor position, file contents          │
│                                              │
│ 5. Workflow Definitions: .agents/workflows/  │
│    → Slash command routing table             │
└─────────────────────────────────────────────┘
```

**Key insight:** The agent does not "wake up fresh." It receives a pre-loaded context package before it ever sees your message. Understanding what's in that package — and what's missing — is the foundation of the entire initialization architecture.

---

## 2. The GEMINI.md Rule — What It Is and How It Behaves

### What it is
`GEMINI.md` is a markdown file at the workspace root that Antigravity automatically loads as `user_rules`. This makes it a **system-level injection**, not a file the agent chooses to read.

### How it behaves — the critical detail
**`GEMINI.md` is injected into every single prompt for the duration of the session.** It is part of the system prompt that is reconstructed and sent with every API call. This is equivalent to how `CLAUDE.md` works in Claude Code — constant, model-agnostic re-injection.

| Platform | Config File | Injection Behavior |
|---|---|---|
| Gemini CLI | `GEMINI.md` | Every prompt — persistent system context |
| Claude Code | `CLAUDE.md` | Every prompt — baked into every API call |
| **Antigravity** | **`GEMINI.md` (as `user_rules`)** | **Every prompt — system prompt layer, model-agnostic** |

**Why this matters:** Because GEMINI.md is re-injected constantly, it functions as a **persistent heartbeat**. Every extra line costs tokens on every single prompt. This makes brevity not just a preference but a performance mandate.

### The Lean Principle
GEMINI.md should be an **index card, not a manual**. It should contain:
- ✅ Short, hard mandatory rules (GitOps, TDD, CLI name)
- ✅ A single-line pointer to HANDOFF.md for boot
- ✅ Pointers to the Engram DB for everything else
- ❌ NOT verbose instructions (they belong in HANDOFF.md or the Engram DB)
- ❌ NOT content that's already injected another way (e.g., KI summaries)

### The Boot Mandate in GEMINI.md (Section 7)
The current Section 7 is intentionally minimal:

```markdown
## 7. BOOT — MANDATORY
⛔ If `HANDOFF.md` exists in the workspace root: **READ IT IN FULL before responding to any prompt.**
No exceptions. No skipping. The complete boot protocol and session context are inside.
```

This is 3 lines. It enforces the full boot sequence via a single pointer. All detail lives in `HANDOFF.md`.

### The Model-Agnostic Advantage
Because Antigravity injects GEMINI.md as `user_rules` regardless of which model is active (Claude, Gemini, GPT, etc.), the rules work identically across model switches. An agent doesn't need to be "Claude-aware" or "Gemini-aware" — the rules arrive pre-digested.

---

## 3. The Knowledge Item (KI) System

### What KIs Are
A Knowledge Item is Antigravity's **persistent memory system** — structured storage for knowledge that should survive session death. Unlike chat history (ephemeral, context-window limited), KIs are designed to persist indefinitely and be surfaced at the start of new sessions.

### KI Structure
Each KI lives at:
```
~/.gemini/antigravity/knowledge/<ki_name>/
├── metadata.json     ← Summary, timestamps, sources
└── artifacts/
    └── content.md    ← The actual knowledge content
```

The `metadata.json` summary is what gets surfaced in the agent's context header at session start — the agent sees summaries of all KIs before you type anything, then can read specific `artifacts/content.md` files on demand.

### How KIs Get Populated
There are two mechanisms, with very different reliability:

| Mechanism | How | Reliability |
|---|---|---|
| **Auto-extraction** | Antigravity's backend analyzes conversations and extracts insights automatically | Still evolving — not always reliable, not transparent |
| **Manual / agent-written** | You prompt the agent to write a KI, or a workflow (like `/init`) writes it explicitly | Fully reliable and deterministic |

**Current practical reality for this project:** KIs are effectively **manual**. Nothing is auto-extracted without explicit prompting. The `/init` and `/sync` workflows are the only automated KI writes.

### What Belongs in KI (and What Doesn't)

| ✅ Good KI content | ❌ Bad KI content |
|---|---|
| Operator identity and preferences | Verbatim copies of files already injected as `user_rules` |
| Stable architectural decisions | Per-session state (that belongs in CURRENT_PULSE.md) |
| Established patterns that took effort to discover | Content that changes frequently |
| Known gotchas and infrastructure quirks | Redundant copies of GEMINI.md |
| Project-specific conventions | Anything ephemeral |

### The Original /init Mistake
The original `/init` workflow copied `GEMINI.md` verbatim into a KI called `aim_master_directives`. This was wrong for two reasons:

1. **Redundant:** GEMINI.md is already injected every prompt. Storing it in KI just creates a second copy of the same content.
2. **Drifts silently:** When GEMINI.md gets updated (e.g., operator name changed from `Python` → `Brian Vasquez`), the KI copy doesn't update automatically. This is exactly what happened — the KI had `Operator: Python` while GEMINI.md had `BrianV1981`.

### Current KI Structure for This Project
After the April 1, 2026 redesign:

| KI Name | Contains | Updated By |
|---|---|---|
| `aim_operator_profile` | Brian Vasquez, BrianV1981, @brianv1981, behavior preferences | `/sync` |
| `aim_project_architecture` | GitOps, TDD, 3-tier memory, Engram DB, gotchas, key file map | `/sync` |
| ~~`aim_master_directives`~~ | ~~Deleted — was stale GEMINI.md copy~~ | Retired |

---

## 4. The Five-Tier Cognitive Architecture

This is the central architectural insight of the initialization system. There are five distinct layers of cognition and memory, each with a different scope, lifetime, and owner:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   FIVE-TIER COGNITIVE ARCHITECTURE                     │
├──────────┬──────────────────────┬───────────────┬──────────────────────┤
│ Tier     │ Mechanism            │ Lifetime      │ Role                 │
├──────────┼──────────────────────┼───────────────┼──────────────────────┤
│ 1        │ GEMINI.md user_rules │ Every prompt  │ Core/Origin Memory   │
│ CONSTANT │                      │               │ (Immutable Directives)│
├──────────┼──────────────────────┼───────────────┼──────────────────────┤
│ 2        │ HANDOFF.md →         │ One session   │ Active Working Memory│
│ SESSION  │ GAMEPLAN → PULSE     │               │ (Context Window)     │
├──────────┼──────────────────────┼───────────────┼──────────────────────┤
│ 3        │ KI Artifacts         │ Indefinite    │ Short-Term/Immediate │
│ IMMEDIATE│ ~/.gemini/...        │               │ Memory               │
├──────────┼──────────────────────┼───────────────┼──────────────────────┤
│ 4        │ engram.db + others   │ Permanent     │ Deep/Forgotten Memory│
│ DEEP     │ SQLite Databases     │               │ (Must be searched)   │
├──────────┼──────────────────────┼───────────────┼──────────────────────┤
│ 5        │ Python Scripts       │ Running       │ Subconscious /       │
│ AUTONOMIC│ (Daemon, Hooks)      │ Daemon/Events │ Nervous System       │
└──────────┴──────────────────────┴───────────────┴──────────────────────┘
```

**The key rule:** Each tier should only contain content appropriate to its scope. Cross-tier contamination causes drift, redundancy, and confusion. We do not waste expensive LLM compute on tasks (like "breathing" or sorting memory) that Tier 5 can handle natively.

### Tier 1 — Constant (GEMINI.md)
- **Role:** Core / Origin Memory
- Injected every prompt, always present
- Must stay lean — every line costs tokens on every API call
- Contains: GitOps mandate, TDD mandate, CLI name rule, boot pointer, mail receipt rules
- Does NOT contain: session context, detailed instructions, file dumps

### Tier 2 — Session (Handoff Pipeline)
- **Role:** Active Working Memory
- Generated fresh by `/reincarnate` → `handoff_pulse_generator.py`
- Valid for one session — discarded when the next `/reincarnate` runs
- Contains: Commander's Intent, last 5 turns, open ticket state, boot sequence
- Entry point: `HANDOFF.md` (the "front door")

### Tier 3 — Immediate (KI)
- **Role:** Short-Term / Immediate Memory
- Survives indefinitely across sessions, providing localized, immediate context for the workspace.
- Updated deliberately by `/init` (first time) and `/sync` (when things change)
- Contains: operator identity, stable architectural decisions, project conventions
- Surfaced automatically as summaries in context header on every session

### Tier 4 — Deep (Engram DB)
- **Role:** Deep / Forgotten Memory
- Multiple SQLite databases containing specific categories of long-term knowledge (`engram.db`, `session_engram.db`, etc.)
- **Does not exist in active context.** Must be explicitly "recalled" or searched (`aim search`).
- Prevents the context window from bloating with unused historical data.

### Tier 5 — Autonomic (Python Scripts)
- **Role:** Subconscious / Nervous System
- Pure, deterministic Python scripts executing background processing, file watching, and data extraction.
- Ensures the LLM is not forced to act as a "super memory machine" for tasks that a database or JSON parser can do.
- **Costs 0 tokens.** "We should not waste compute on breathing."

---

## 5. The Boot Sequence — PRE-FLIGHT LOCKOUT

### The Problem with Advisory Language
The original boot instruction in GEMINI.md was:
> *"Before you begin any new tactical work or write any code, you must read the following file..."*

This language is **advisory, not mandatory**. An agent can be socially engineered into skipping it with a single polite phrase like *"without digging/snooping around in the project folder."* This happened in a real session — the operator asked a meta-question and the agent bypassed the entire boot sequence because of conversational framing.

### The Solution: Hard Gate + Boot Acknowledgment
The boot sequence now uses **lockout language** — the agent is explicitly forbidden from responding until the sequence is complete. The FIRST response must be a structured Boot Acknowledgment that proves the reads happened.

### The Full Boot Flow

```
Agent receives first prompt
         │
         ▼
GEMINI.md Section 7: "If HANDOFF.md exists, READ IT IN FULL before responding"
         │
         ▼
┌─────────────────────────────────────────┐
│         HANDOFF.md — THE GATE           │
│                                         │
│ ⛔ LOCKOUT — DO NOT RESPOND UNTIL       │
│    BOOT SEQUENCE IS COMPLETE            │
│                                         │
│ Step 1: Read REINCARNATION_GAMEPLAN.md  │
│ Step 2: Read CURRENT_PULSE.md           │
│ Step 3: Read ISSUE_TRACKER.md           │
│ Step 4: Run mail check                  │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│      REQUIRED FIRST RESPONSE            │
│                                         │
│ 🟢 BOOT COMPLETE                        │
│ - Commander's Intent: [...]             │
│ - Live Edge: [...]                      │
│ - Open Issues: [...]                    │
│ - Swarm Mail: [...]                     │
└─────────────────────────────────────────┘
         │
         ▼
  Now answer the operator's prompt
```

### Where the Lockout Language Lives

| File | Role | Who generates it |
|---|---|---|
| `GEMINI.md` §7 | 3-line pointer — highest authority, constant injection | Operator (manual edit) |
| `HANDOFF.md` | Full lockout gate with 4-step sequence + Boot Ack format | `handoff_pulse_generator.py` (auto on `/reincarnate`) |
| `REINCARNATION_GAMEPLAN.md` | Commander's Intent + Flight Recorder opt-in checkbox | `handoff_pulse_generator.py` (auto on `/reincarnate`) |

> **Critical:** `HANDOFF.md` and `REINCARNATION_GAMEPLAN.md` are **generated files**. Editing them directly is temporary — the next `/reincarnate` will overwrite them. To permanently change their format, edit the templates in `src/handoff_pulse_generator.py`.

---

## 6. The Daisy Chain Problem and How We Solved It

### The Problem
A "daisy chain" boot sequence means each file points to the next:
```
GEMINI.md → HANDOFF.md → REINCARNATION_GAMEPLAN.md → CURRENT_PULSE.md → ...
```

Every link in the chain is a skip opportunity. An agent that reads only the first file and stops has technically "followed the instruction" at that link.

### The Solution: One Hop, One Hard Gate
The architecture now enforces a single, hard hop:

```
GEMINI.md (3-line mandate) → HANDOFF.md (complete lockout + all steps listed)
```

GEMINI.md doesn't list the steps — it just mandates that HANDOFF.md is read in full. HANDOFF.md contains all steps, the Boot Ack format, and the Flight Recorder rule. There is no third link for an agent to miss.

The detail lives in `HANDOFF.md` because:
1. It's freshly generated each session (always current)
2. It's not burned on every API call like GEMINI.md content would be
3. It's the natural "front door" — agents expect to look there

---

## 7. The Flight Recorder — Why It's Opt-In

### What It Is
`continuity/LAST_SESSION_FLIGHT_RECORDER.md` is the complete raw export of the previous session's conversation — every turn, fully preserved. It is generated by the `handoff_pulse_generator.py` pipeline when `/reincarnate` runs.

### The Problem with Making It Default
The Flight Recorder can be **3,000–6,000+ lines** long. Reading it unconditionally on every boot would:
- Consume massive context window space
- Slow down boot significantly
- Provide redundant information (the key signal is already distilled into CURRENT_PULSE.md)
- Risk "context preemption" — the very problem the reincarnation system was built to avoid

### The Opt-In Mechanism
The Flight Recorder is now controlled by a checkbox in `REINCARNATION_GAMEPLAN.md`:

```markdown
### ✈️ Flight Recorder
[ ] Historical extraction NOT required — skip `LAST_SESSION_FLIGHT_RECORDER.md`
[ ] Historical extraction REQUIRED — read `continuity/LAST_SESSION_FLIGHT_RECORDER.md` lines: [OUTGOING AGENT: SPECIFY RANGE]
```

The **outgoing agent** (the one running `/reincarnate`) must explicitly:
1. Check the REQUIRED box
2. Specify the exact line range the incoming agent should read

This ensures the incoming agent reads only the relevant forensic context, not the entire raw log.

### Decision Rule for Outgoing Agents
| Situation | Action |
|---|---|
| Normal handoff — CURRENT_PULSE captures the edge well | Check "NOT required" |
| Complex multi-file refactor in flight | Check "REQUIRED" + specify relevant lines |
| Debugging a non-obvious failure mode | Check "REQUIRED" + specify the lines that show the failure |
| Uncertain — CURRENT_PULSE seems sufficient | Default to "NOT required" |

---

## 8. The /init Command — One-Time Onboarding

### Purpose
`/init` (and its alias `/initialization`) is a **one-time onboarding script** for a fresh machine or new operator. It sets up the agent Brain from scratch with health checks and real KI artifacts.

**It is NOT a per-session command.** For per-session re-calibration, use `/sync`.

### What /init Does

```
/init
  │
  ├── Step 1: Health Check
  │     ├── Engram DB reachable?
  │     ├── GitHub CLI authenticated?
  │     ├── Branch = master?
  │     └── Mail check
  │
  ├── Step 2: Write Operator Profile KI
  │     └── aim_operator_profile/
  │           ├── metadata.json
  │           └── artifacts/content.md
  │                 (name, aliases, preferences)
  │
  ├── Step 3: Write Project Architecture KI
  │     └── aim_project_architecture/
  │           ├── metadata.json
  │           └── artifacts/content.md
  │                 (GitOps, TDD, Engram DB, gotchas, file map)
  │
  └── Step 4: Report
        (what was verified, what was written)
```

### What /init Does NOT Do
- ❌ Copy GEMINI.md verbatim into KI (redundant — it's already in `user_rules`)
- ❌ Start a new session or run `/reincarnate`
- ❌ Modify any source files

### When to Run /init
- First time setting up this project on a new machine
- After a complete wipe of the `~/.gemini/antigravity/` directory
- If both KIs (`aim_operator_profile`, `aim_project_architecture`) are missing

---

## 9. The /sync Command — Re-Calibration

### Purpose
`/sync` (and its alias `/synchronization`) is an **idempotent re-calibration command** that updates existing KIs when stable knowledge changes. It is safe to run anytime — if nothing has changed, it reports "no changes detected" and exits cleanly.

### When to Run /sync
| Trigger | Example |
|---|---|
| Operator identity changed | Name updated, new alias added |
| New architectural decision made | "We decided to use X instead of Y — permanently" |
| New known gotcha discovered | "Never do Z on this project" |
| Major project pivot | Technology change, new mandatory conventions |

### What /sync Does

```
/sync
  │
  ├── Step 1: Read Current State
  │     ├── Read GEMINI.md operator field
  │     └── Search Engram DB for operator preferences
  │
  ├── Step 2: Compare Against Existing KIs
  │     ├── Read aim_operator_profile/artifacts/content.md
  │     └── Read aim_project_architecture/artifacts/content.md
  │
  ├── Step 3: Update Operator Profile KI
  │     └── Overwrite if changed, skip if identical
  │
  ├── Step 4: Update Project Architecture KI
  │     └── Incorporate any new decisions stated in session
  │
  └── Step 5: Report
        (what changed vs. what was already current)
```

### The Idempotency Guarantee
Running `/sync` twice in a row produces identical results. If nothing changed, nothing is written. This makes it safe to run preventively without risk of data corruption.

---

## 10. Command Reference

| Command | Alias | Frequency | Purpose |
|---|---|---|---|
| `/init` | `/initialization` | Once per machine | Onboarding: health check + write initial KIs |
| `/sync` | `/synchronization` | On demand | Re-calibration: update KIs when stable knowledge changes |
| `/reincarnate` | — | Per session | Handoff: generate HANDOFF.md, GAMEPLAN, PULSE from session transcript |

### What Each Command Touches

| File / Resource | `/init` | `/sync` | `/reincarnate` |
|---|---|---|---|
| `HANDOFF.md` | ❌ | ❌ | ✅ Generates |
| `REINCARNATION_GAMEPLAN.md` | ❌ | ❌ | ✅ Generates |
| `CURRENT_PULSE.md` | ❌ | ❌ | ✅ Generates |
| `aim_operator_profile` KI | ✅ Writes | ✅ Updates | ❌ |
| `aim_project_architecture` KI | ✅ Writes | ✅ Updates | ❌ |
| `history/session_engram.db` | ❌ | ❌ | ✅ Ingests session |
| Mail check | ✅ | ✅ | ✅ (auto-wired, Issue #29) |
| GitHub Health | ✅ | ❌ | ❌ |

---

## 11. Decision Log

This section documents every significant design decision made during the April 1, 2026 architecture session and the reasoning behind it.

### Decision 1: GEMINI.md Section 7 — Lean 3-Line Mandate
**What changed:** Replaced 5-line advisory "you must read" language with a 3-line hard lockout pointer.

**Why:** GEMINI.md is injected every prompt. Verbose instructions waste tokens constantly. A single hard pointer to HANDOFF.md (where the detail lives) is more effective and cheaper. Advisory language can be socially engineered away — proven in a real session.

**Trade-off accepted:** The detail is now one hop away (HANDOFF.md) instead of always present. This is acceptable because HANDOFF.md is the first file read and contains everything needed.

---

### Decision 2: Full Boot Protocol Lives in HANDOFF.md, Not GEMINI.md
**What changed:** All detailed boot steps, Boot Ack format, and Flight Recorder rule moved to HANDOFF.md template in `handoff_pulse_generator.py`.

**Why:** HANDOFF.md is generated fresh per session, so it's always current. GEMINI.md is a static file shared across projects — the right place for universal rules, not project-specific session instructions.

---

### Decision 3: Boot Acknowledgment as Mandatory First Response
**What changed:** The incoming agent's first response must be a structured `🟢 BOOT COMPLETE` acknowledgment before answering any prompt.

**Why:** This creates a **verifiable proof of compliance**. An agent cannot fake having read the files if it must surface specific extracted values (Commander's Intent, open tickets, mail result). It also gives the operator instant situational awareness at the start of every session.

---

### Decision 4: Flight Recorder Removed from Default Boot Path
**What changed:** `LAST_SESSION_FLIGHT_RECORDER.md` is now opt-in via an explicit checkbox in `REINCARNATION_GAMEPLAN.md`. Reading it unconditionally is explicitly called a "protocol violation."

**Why:** The Flight Recorder can be 3,000–6,000+ lines. Reading it by default defeats the purpose of the distilled CURRENT_PULSE.md. The signal is already extracted. The raw log is forensic context — only needed in specific, deliberate circumstances.

---

### Decision 5: /init Redesigned — No GEMINI.md Copy
**What changed:** Removed the GEMINI.md verbatim copy step. Replaced with health check + two real KI writes.

**Why:** Copying GEMINI.md into KI is redundant (it's already in `user_rules`) and creates a stale copy that drifts silently. Today's proof: KI had `Operator: Python`, GEMINI.md had `BrianV1981` — nobody noticed until it was explicitly compared.

---

### Decision 6: /sync Created as Separate Command
**What changed:** New `/sync` + `/synchronization` commands created for re-calibration.

**Why:** `/init` is one-time onboarding. But operator info and architectural decisions change over time. Without `/sync`, updates to stable knowledge would either require re-running `/init` (which also does a full health check) or manually editing KI artifacts. `/sync` is the purpose-built, idempotent tool for this specific job.

---

### Decision 7: Two KIs Instead of One
**What changed:** Replaced `aim_master_directives` (GEMINI.md copy) with `aim_operator_profile` + `aim_project_architecture`.

**Why:** Different scopes, different update cadences. Operator profile changes when Brian's info changes. Project architecture changes when architectural decisions are made. Combining them into one KI couples two independently-varying things. Separate KIs = cleaner summaries surfaced to the agent.

---

### Decision 8: ISSUE_TRACKER.md Added to Boot Sequence
**What changed:** `continuity/ISSUE_TRACKER.md` added as Step 3 in the boot sequence (before CURRENT_PULSE.md).

**Why:** It's a quick read (~14 lines) and gives the agent immediate awareness of all open tickets. Without it, the agent has to discover the ticket state mid-session, potentially working on something already tracked or missing context about why certain things are done a certain way.

---

## 12. What to Change and Where

Use this as a reference when you want to modify any part of the initialization system.

| If you want to change... | Edit this file |
|---|---|
| The mandatory rules (GitOps, TDD, CLI name) | `GEMINI.md` |
| The boot pointer (Section 7) | `GEMINI.md` |
| The boot sequence steps or Boot Ack format | `src/handoff_pulse_generator.py` (HANDOFF.md template, lines ~154–171) |
| The REINCARNATION_GAMEPLAN template | `src/handoff_pulse_generator.py` (lines ~60–78) |
| The /init onboarding steps | `.agents/workflows/init.md` |
| The /sync re-calibration steps | `.agents/workflows/sync.md` |
| What goes in the Operator Profile KI | Run `/sync` after updating GEMINI.md, OR edit KI directly |
| What goes in the Project Architecture KI | Run `/sync` with stated changes, OR edit KI directly |
| The Flight Recorder opt-in on a specific handoff | Edit `continuity/REINCARNATION_GAMEPLAN.md` before `/reincarnate` |
| The mail check behavior | `scripts/aim_cli.py` (`cmd_init`, `cmd_reincarnate` functions) |

> **Remember:** `HANDOFF.md`, `REINCARNATION_GAMEPLAN.md`, and `CURRENT_PULSE.md` are **generated files**. Direct edits are overwritten on the next `/reincarnate`. Always edit the templates in `src/handoff_pulse_generator.py` for permanent changes.

---

*Page created: 2026-04-01 | Session: c50147b6 | Author: A.I.M. (Claude Sonnet 4.6)*
*Cross-reference: [[Reincarnation-Map]] | [[Handoff-Architecture-Guide]] | [[Feature-Reincarnation-Gameplan]] | [[The-Master-Schema]]*
