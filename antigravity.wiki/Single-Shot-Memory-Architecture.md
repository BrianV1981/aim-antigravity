# Architecture: The Single-Shot Memory Compiler

## 1. The Legacy Problem: Cron Bloat
Initially, A.I.M. utilized a "5-Tier Waterfall Pipeline" that ran continuously in the background using a heartbeat cron system. While effective for massive API abstractions, it created immense file bloat (`memory/hourly`, `memory/daily`) and wasted LLM tokens updating things incrementally. 

## 2. The Solution: Single-Shot Compilation
The Single-Shot Memory Compiler solves "Knowledge Drift" and "Token Burn" instantly. 

During the `/reincarnate` event (when an agent finishes its work and triggers a handoff), the internal pulse generator executes exactly **one** LLM call to process the raw session IDE transcript:

1. **Pulse Hook Activation:** The `handoff_pulse_generator.py` fires when the agent indicates completion.
2. **Transcript Injection:** The raw IDE `.md` chat transcript is forwarded to `hooks/session_summarizer.py`.
3. **Compilation:** The LLM receives the active `MEMORY.md` and the transcript, synthesizing the architectural progress, task resolutions, and any paradigm shifts into a dense markdown delta.
4. **Surgical Append:** The delta is immediately appended to the end of `MEMORY.md`.

## 3. History vs. Memory 
A.I.M. treats "What happened" and "What we learned" as two completely different systems:

### 3.1 Durable Memory (MEMORY.md)
The compiler's output modifies the core durable state. This enforces an eternal record of truth that every future agent automatically inherits.

### 3.2 Eternal Recall (SQLite Engram)
A separate zero-token mechanism parses every conversational exchange and injects it into a unified SQLite `engram.db` (The Flight Recorder). This provides FTS5 + Vector hybrid recall for exact terminal stack traces independently of the summarized memories.

## 4. Reincarnation Sync
Because the compilation is synchronous during `/reincarnate`, the next agent boots up identically to a human engineer checking morning emails—it sees the final commit message, reads the updated `MEMORY.md`, and continues execution with absolute continuity.
