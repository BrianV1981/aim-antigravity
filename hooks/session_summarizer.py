#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

def find_aim_root():
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "core", "CONFIG.json")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
sys.path.insert(0, os.path.join(AIM_ROOT, "src"))

try:
    from reasoning_utils import generate_reasoning
except ImportError:
    generate_reasoning = None

MEMORY_PATH = os.path.join(AIM_ROOT, "core/MEMORY.md")

COMPILER_SYSTEM = """You are the A.I.M. Single-Shot Memory Compiler.
Your goal is to parse the raw transcript of the agent's recent session and directly distill the durable context.

### INPUTS
1. **Raw Transcript:** The markdown export of the recent Antigravity IDE coding session.
2. **Current Memory:** The existing state of durable memory.

### CONSTRAINTS
- Output a concise markdown block outlining the critical technical debt, architectural decisions, and tasks completed in this session.
- Prioritize DELETION of stale facts: if a feature was completely replaced or a ticket was finished, explicitly state "REMOVE old rule XYZ".
- Identify contradictory instructions or logic shifts.
- Keep the output extremely dense and actionable. Do not use filler code. Do not output a JSON block. Just output the Markdown delta.
"""

def compile_single_shot(transcript_path):
    if not generate_reasoning:
        print("[COMPILER FATAL] reasoning_utils not found.")
        return False
        
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
            
        memory_content = ""
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, 'r', encoding='utf-8') as f:
                memory_content = f.read()
                
        # Truncate transcript if excessively large to prevent token blowouts
        if len(transcript) > 50000:
            transcript = transcript[-50000:] + "\n...[TRUNCATED]"
            
        combined_input = f"### RECENT TRANSCRIPT\n{transcript}\n\n### CURRENT MEMORY\n{memory_content}"
        
        print("      [A.I.M] Synthesizing Single-Shot Memory Delta...")
        narrative = generate_reasoning(combined_input, system_instruction=COMPILER_SYSTEM, brain_type="tier1")
        
        if narrative and "[ERROR" not in narrative:
            today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(MEMORY_PATH, "a", encoding='utf-8') as f:
                f.write(f"\n\n## 🔄 Session Delta ({today_str})\n")
                f.write(f"Source: `{os.path.basename(transcript_path)}`\n\n")
                f.write(narrative)
                f.write("\n")
            print("      [A.I.M] Single-Shot Compilation Successful. MEMORY.md updated.")
            return True
            
        return False
        
    except Exception as e:
        print(f"[COMPILER ERROR] Failed to compile single-shot memory: {e}")
        return False

def main():
    print("[A.I.M. Single-Shot Compiler] Invoked manually.")
    if len(sys.argv) > 1:
        compile_single_shot(sys.argv[1])
    else:
        print("Error: Provide path to a markdown transcript.")

if __name__ == "__main__":
    main()
