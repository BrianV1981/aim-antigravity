# A.I.M. (Actual Intelligent Memory)

**"Treat your AI like a bot, not an oracle. Built by a gamer, for the trenches."**

☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)](https://github.com/BrianV1981/aim-antigravity/blob/main)
[![Platform](https://img.shields.io/badge/Platform-Google%20Antigravity%20IDE-0088cc.svg)](https://github.com/BrianV1981/aim-antigravity/blob/main)

**A.I.M.** is an open-source engineering ecosystem designed to cure the "Amnesia Problem" of autonomous AI agents by acting as a strict operating system and exoskeleton.

---

> ⚠️ **THE VIBE CODING ORIGIN & ANTIGRAVITY EVOLUTION**
>
> A.I.M. wasn't built by a machine learning researcher in Silicon Valley. It was built by a gamer who spent years writing macros and automation bots for MMOs. When you automate a bot, you learn quickly that you can't rely on "magic." You need rigid state machines, clearly defined scopes, and watchdog timers to reset the bot when it wanders off path.
> 
> A.I.M. applies this exact philosophy to LLMs. Instead of trying to build a smarter brain, A.I.M. provides the leash. 
>
> Originally built as a raw terminal wrapper for the Gemini CLI, **A.I.M. has officially migrated to Google Antigravity.** The IDE's file-based State Engineering and native Knowledge Items (KIs) perfectly absorb our strict, MMO-style routing protocols without requiring fragile Bash scripts. 

📖 **Full Documentation:** [Read the Official GitHub Wiki](https://github.com/BrianV1981/aim/wiki)
🛠️ **Engineers:** Hate biological metaphors? [Read the metaphor-free Technical Spec here](https://github.com/BrianV1981/aim/wiki/Technical-Specification).
🧪 **Architecture Shifts:** Understand the shift to native Windows execution via the [Testing & TDD Architecture Guide](Testing-and-TDD-Architecture.md).
🎛️ **The Cockpit:** Review the 14 interactive setup menus inside the [TUI Map](TUI-Map.md).

---

## 🛑 The Problem: The 50-Turn Spaghetti Code

If you let an AI agent code autonomously, it is brilliant for the first 10 turns. By turn 50, its context window is overflowing, it forgets your architectural rules, it hallucinates file paths, and your repository degrades into unmaintainable spaghetti code.

The industry's answer is to build a bigger context window. That's giving a distractible worker a bigger desk.

A.I.M.'s answer is a strict Standard Operating Procedure natively enforced through Antigravity KIs.

---

## 🚀 The Solution: A Sovereign Exoskeleton

A.I.M. transforms your Antigravity agent into a disciplined Principal Engineer. It externalizes the agent's memory into structured markdown files, automates its Git lifecycle via strict Issue-Driven Development (IDD), and provides an indestructible context shield.

---

## 🧠 The Architecture (v2.0)

A.I.M. does not use a massive, unconstrained context window. Its core insight is separating **what requires an LLM** from **what is better handled by deterministic state machines**.

### 1. The Knowledge Item (KI) Sieve
The AI industry assumes memory management requires an LLM to blindly read every file. A.I.M. doesn't. We use Antigravity's **Knowledge Items** (`aim_master_directives`) to inject highly targeted, zero-noise rules directly into the agent's boot sequence. The agent doesn't think about these rules; they are baked into its autonomic nervous system.

### 2. The [Cascading Memory](Feature-Cascading-Memory.md) Engine (The Background Brain)
While the frontline Antigravity agent works in the IDE, optional background Python daemons (The Harvester, The Distiller) can silently compress raw logs into permanent, distilled architectural rules without polluting the active context window. 

### 3. The Engram DB (The Subconscious)
The permanent memory lives in `.engram` cartridges. You can load 10,000 pages of specific documentation (e.g., `django_master.engram`) into a decentralized SQLite database, completely bypassing the need for massive cloud vector stores. 

---

## 🔥 Killer Features

### 🎯 The Matrix Agent (Plug-and-Play Specialists)
Combine a specific knowledge cartridge with a surgically constrained `GEMINI.md` mandate. You don't rely on the LLM's pre-trained weights to guess the answer. You inject the exact documentation and force the agent to loop until the terminal output is green.

### 🔌 The [DataJack](The-DataJack-Protocol.md) Protocol
Package thousands of pages of verified solutions into a single `.engram` cartridge. When you load it into the background DB, your agent wakes up with pre-calculated semantic recall of the entire library. Zero embedding costs. One person pays the compute tax once — the community inherits it.

### 🐙 The [GitOps Bridge](Feature-GitOps-Bridge.md)
A.I.M. forces atomic, traceable deployments:
- Write an issue.
- Spin up an Antigravity agent.
- Fix the bug on an isolated branch.
Every change is tied to an issue. Every regression is instantly revertible.

### 🛑 Predictable Restraint
A massive danger with modern LLMs is "auto-execution." A.I.M.'s rigid GitOps and behavioral hierarchy physically suppresses this instinct. The agent treats the operator as the explicit trigger, ensuring it never touches your codebase until you give the exact execution order. 

---

## 🏗️ Getting Started (Any OS)

Because A.I.M. is now natively powered by the Antigravity IDE, **Linux, WSL, macOS, and Windows 11 are all fully supported out of the box.** 

### 1. Installation
1. Clone this repository to your local machine:
   `git clone https://github.com/BrianV1981/aim-antigravity.git`
2. Open the directory in **Google Antigravity**.

### 2. The Bootstrap Sequence
In the Antigravity agent chat, simply type:
```
/init
```
This single workflow slash-command will:
- Ingest the `GEMINI.md` master schema.
- Create your `aim_master_directives` Knowledge Item (KI).
- Bootstrap your local environment.

You are now ready to begin atomic execution.

---

> *"Alcmaeon of Croton, Praxagoras of Kos, and Herophilus of Chalcedon were three Ancient Greek philosophers interested in the relation between the head and the body. Alcmaeon argued that the brain is the seat of intelligence, connected to the extremities of the body by poroi. Praxagoras suggested that the brain controls movement in the body, and posed the existence of neurons responsible for sending brain signals through the body..."*