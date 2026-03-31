#!/usr/bin/env python3
import os
import sys
import json
import subprocess

def find_aim_root():
    current = os.path.abspath(os.getcwd())
    while current != '/':
        if os.path.exists(os.path.join(current, "core/CONFIG.json")): return current
        if os.path.exists(os.path.join(current, "setup.ps1")): return current
        if os.path.exists(os.path.join(current, "setup.sh")): return current
        current = os.path.dirname(current)
        if current.endswith(':\\') or current == '\\': break
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
SCRIPTS_DIR = os.path.join(AIM_ROOT, "scripts")
SRC_DIR = os.path.join(AIM_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from reasoning_utils import generate_reasoning

def parse_chalkboard_prompt(raw_text):
    system_instruction = (
        "You are the Chalkboard NL Interpreter for the A.I.M. Swarm. "
        "Your job is to read natural language requests from the human engineer and extract the routing parameters "
        "to dispatch a message through the 'aim mail send' command.\n\n"
        "You must output ONLY raw, strictly valid JSON without any markdown formatting, code blocks, or preamble. "
        "The JSON must have EXACTLY three keys:\n"
        '{"target_team": "<the target agent team, e.g. claude, antigravity, or global>", "subject": "<a professional summary of the task>", "body": "<the detailed message to send>"}'
    )
    
    # Try parsing multiple times to combat LLM markdown wrap hallucinations
    for _ in range(2):
        response = generate_reasoning(raw_text, system_instruction=system_instruction, brain_type="tier1")
        if not response or "[ERROR" in response or response.startswith("Error:"):
            return None, response
            
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
            
        try:
            data = json.loads(cleaned.strip())
            if "target_team" in data and "subject" in data and "body" in data:
                return data, None
        except json.JSONDecodeError:
            pass # Try again
            
    return None, f"Failed to parse LLM valid JSON structure from LLM output:\n{response}"

def main():
    if len(sys.argv) < 2:
        print("Usage: aim_chalkboard.py \"<natural language command>\"")
        sys.exit(1)

    raw_request = sys.argv[1]
    
    print(f"--- Chalkboard Interpreter ---")
    print(f"[*] Analyzing your request...")
    
    data, error = parse_chalkboard_prompt(raw_request)
    
    if error:
        print(f"[ERROR] Chalkboard parsing failed: {error}")
        sys.exit(1)
        
    target_team = data["target_team"]
    subject = data["subject"]
    body = data["body"]
    
    print(f"[*] Extracted Intent -> Route: {target_team.upper()} | Subject: {subject}")
    print(f"[*] Dispatching to native Swarm Post Office...")
    
    mail_script = os.path.join(SCRIPTS_DIR, "aim_mail.py")
    cmd = [sys.executable, mail_script, "send", target_team, subject, body]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Post Office rejected the package: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
