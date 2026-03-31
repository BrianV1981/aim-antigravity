# 🛑 Operator's Guide: The 30% Rule & Context Collapse

**Original Post Date:** March 26, 2026
*Author: Brian Vasquez, Creator of A.I.M.*

This document outlines the operational reality of running long-horizon LLM agents. What you are about to read is not theoretical or strictly scientific empirical data. It is highly anecdotal—the result of hundreds of hours of personal experience and "vibe testing" within the Gemini CLI. 

If you want an autonomous agent that operates at a Senior/Principal engineer level, you must understand how context windows actually behave in production.

---

## 1. The Myth of the 2-Million Token Window
"Context is King." We have all heard it. But a 2-million token context window is **complete garbage** if the LLM cannot weigh the immediate, tactical reality of the current conversation.

If you force an agent to carry 1.5 million tokens of historical thrashing, debugging, and conversational noise, its "attention weights" become hopelessly diluted. It cannot properly prioritize the command you just gave it because it is drowning in the noise of its past failures.

## 2. The Economics of Context Thrashing
Token consumption is not linear; it is cumulative. Every turn you take, the entire history of the session is re-sent to the model.

*   At 20% context capacity, a single click/turn can eat over 200,000 tokens.
*   **Five turns later, you have burned over 1,000,000 tokens.**
*   Let a session drift to 50% capacity, and you are bleeding tokens like a severed artery.

This is not just an economic problem; it is a cognitive problem.

## 3. The "Compression" Trap (Do Not Do This)
Many users hit 50% capacity (1,000,000+ tokens) and rely on the AI to "compress" or "summarize" the session down to 10-15% capacity so they can keep working in the same terminal.

**This is a hard, catastrophic NO.**

When you allow an agent to hit 50% capacity and then command it to compress its own sprawling, noisy context down to 10%, you are destroying its tactical cognition. It will hallucinate. It will forget exact variable names. It will lose the thread of the architecture.

> *An agent operating under 30% capacity with a clean context injection is a genius. That exact same agent, after hitting 50% and compressing down to 15%, is completely lobotomized. I mean that.*

## 4. The Operator's Strategy: The 30% Exit Plan

You must operate A.I.M. in defined, tactical bursts. Do not try to build an entire application in a single terminal session.

### The Sweet Spot (10% -> 25%)
This is the golden zone. During this window, the agent has enough context to understand the architecture, but is still "light" enough to strictly obey its initial directives, follow GitOps, and write proper TDD. It is hyper-productive.

### Phase A: The Preparation Agent (0% -> 20%)
1. Spin up your first A.I.M. session.
2. Use this agent strictly for **scoping and scaffolding**.
3. Have it map the codebase, define the architecture, and write hyper-explicit GitHub Issues / Bug Reports for the upcoming tasks.
4. Have it write the `ROADMAP.md` or Execution Guide.
5. **The Warning:** Once the context hits 20%, you need to start wrapping things up.
6. **The Exit:** By the time you hit 30%, *start panicking*. You must formulate an exit plan immediately. If you push into the 30s, you might finish a task, but you run a high risk of the agent suffering from "System Prompt Fade" and failing to write a solid handoff. (While you technically *can* run to 40%, 30% is the safe, disciplined cutoff).
7. Run `aim reincarnate` to distill the state into a Gameplan and exit the session.

### Phase B: The Execution Agent (The Fresh Mind)
1. The Reincarnation protocol spins up a brand new A.I.M. agent in a fresh terminal.
2. Because of the continuity pipeline, this new agent will wake up and instantly read the `REINCARNATION_GAMEPLAN.md`.
3. **The Advantage:** If you handed off at 30% capacity, the dying agent's Gameplan is tight, logical, and highly prescriptive. The new agent ingests it perfectly, weighs the tactical instructions flawlessly, and executes the code with Senior-level precision.
4. If you had waited until 1,000,000 tokens to handoff, the continuity documents would be massive, rambling, and impossible for the new agent to parse methodically.

### The Golden Rule
**Always spin up a new agent BEFORE compression is necessary.**

Treat your terminal sessions like sprint cycles, not marathons. Use `aim reincarnate`, kill the bloated process, and let a fresh agent carry the baton. This is the only way to maintain epistemic certainty and prevent hallucinations.