import json
import os
from datetime import datetime

def parse_iso(ts):
    if not ts: return None
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except:
        return None

def analyze_file(file_path):
    print(f"\n--- Analyzing {os.path.basename(file_path)} ---")
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    messages = data.get('messages', [])
    last_user_ts = None
    turn_count = 0
    
    for i, msg in enumerate(messages):
        msg_type = msg.get('type')
        ts = parse_iso(msg.get('timestamp'))
        
        if msg_type == 'user':
            last_user_ts = ts
            turn_count += 1
        elif msg_type == 'gemini' and last_user_ts:
            latency = (ts - last_user_ts).total_seconds()
            tokens = msg.get('tokens', {}).get('total', 0)
            
            if latency > 60:
                print(f"Turn {turn_count}: LATENCY SPIKE! Latency: {latency:.2f}s, Tokens: {tokens}")
            
            # Basic Fade Check: Look for common violations
            tool_calls = msg.get('toolCalls', [])
            for tc in tool_calls:
                name = tc.get('name')
                if name == 'run_shell_command':
                    cmd = tc.get('args', {}).get('command', '')
                    if 'git commit' in cmd or 'git add' in cmd:
                        # Check if user asked for it in the previous message
                        prev_user_content = ""
                        for j in range(i-1, -1, -1):
                            if messages[j].get('type') == 'user':
                                for part in messages[j].get('content', []):
                                    if 'text' in part:
                                        prev_user_content += part['text']
                                break
                        if 'commit' not in prev_user_content.lower() and 'add' not in prev_user_content.lower():
                             print(f"Turn {turn_count}: POTENTIAL FADE! Unrequested Git action: {cmd}")

            # Reset last_user_ts after a gemini response to measure from the NEXT user message
            # Or should we measure consecutive gemini responses in a multi-step turn?
            # In this structure, gemini messages often follow tool results.
            # Let's see if 'tool' messages exist.
            last_user_ts = None

files = [
    '/home/kingb/aim/archive/raw/session-2026-03-28T22-45-a03174d1.json',
    '/home/kingb/aim/archive/raw/session-2026-03-28T06-41-6e8b78d8.json',
    '/home/kingb/aim/archive/raw/session-2026-03-28T18-13-ff8aece5.json'
]

for f in files:
    if os.path.exists(f):
        analyze_file(f)
