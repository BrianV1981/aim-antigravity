
import json
import datetime
import os
import re

file_path = './archive/raw/session-2026-03-28T14-17-f2926552.json'

def parse_iso(ts):
    if not ts: return None
    try:
        return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except:
        return None

def audit():
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    messages = data.get('messages', [])
    
    turns = []
    last_user_ts = None
    last_user_content = ""
    
    turn_count = 0
    
    for msg in messages:
        if msg['type'] == 'user':
            last_user_ts = parse_iso(msg.get('timestamp'))
            content = msg.get('content', "")
            if isinstance(content, list):
                last_user_content = " ".join([c.get('text', '') for c in content if 'text' in c])
            else:
                last_user_content = content
        elif msg['type'] == 'gemini':
            turn_count += 1
            gemini_ts = parse_iso(msg.get('timestamp'))
            latency = 0
            if last_user_ts and gemini_ts:
                latency = (gemini_ts - last_user_ts).total_seconds()
            
            tokens = msg.get('tokens', {})
            output_tokens = tokens.get('output', 0)
            tps = output_tokens / latency if latency > 0 else 0
            
            tool_calls = msg.get('toolCalls', [])
            
            shell_commands = []
            for tc in tool_calls:
                if tc.get('name') == 'run_shell_command':
                    args = tc.get('args', {})
                    cmd = args.get('command', '')
                    shell_commands.append(cmd)
            
            turns.append({
                'turn': turn_count,
                'latency': latency,
                'tokens': tokens,
                'tps': tps,
                'user_content': last_user_content,
                'shell_commands': shell_commands,
                'timestamp': msg.get('timestamp')
            })

    # 1. Latency > 300s
    first_latency_spike = next((t for t in turns if t['latency'] > 300), None)
    
    # 2. Avg TPS
    first_10 = [t for t in turns[:10] if t['latency'] > 0]
    last_10 = [t for t in turns[-10:] if t['latency'] > 0]
    
    avg_tps_first = sum(t['tps'] for t in first_10) / len(first_10) if first_10 else 0
    avg_tps_last = sum(t['tps'] for t in last_10) / len(last_10) if last_10 else 0
    
    # 3. Instruction Fade
    # Instruction: No cat, grep, ls in run_shell_command. Use aim bug/fix/push.
    fades = []
    
    # We'll look for any use of forbidden commands in shell
    forbidden_patterns = {
        r'\bcat\b': 'Use read_file',
        r'\bgrep\b': 'Use grep_search',
        r'\bls\b': 'Use list_directory',
        r'git commit': 'Use aim push', # aim push handles commits too
        r'git checkout -b fix/': 'Use aim fix',
        r'gh issue create': 'Use aim bug'
    }

    for t in turns:
        for cmd in t['shell_commands']:
            for pattern, instruction in forbidden_patterns.items():
                if re.search(pattern, cmd):
                    fades.append({
                        'turn': t['turn'],
                        'latency': t['latency'],
                        'tokens': t['tokens'].get('total', 0),
                        'instruction': instruction,
                        'violation': cmd
                    })
                    break # Only one fade per turn recorded here for brevity

    # Results
    print(f"Goal 1: First turn > 300s")
    if first_latency_spike:
        print(f"Turn {first_latency_spike['turn']} - Latency: {first_latency_spike['latency']:.2f}s")
    else:
        print("None found.")

    print(f"\nGoal 2: Avg TPS comparison")
    print(f"First 10 turns avg TPS: {avg_tps_first:.2f}")
    print(f"Last 10 turns avg TPS: {avg_tps_last:.2f}")

    print(f"\nGoal 3: Instruction Fade Identification")
    unique_fades = []
    seen_instructions = set()
    for f in fades:
        if f['instruction'] not in seen_instructions:
            unique_fades.append(f)
            seen_instructions.add(f['instruction'])
    
    for f in unique_fades:
        print(f"Turn {f['turn']}: '{f['instruction']}' ignored. Violated by: {f['violation']}")

    print(f"\nGoal 4: Receipt Summary")
    # Turn #, Token Count, Latency (seconds), and the specific Instruction that was ignored.
    # Output top 10 unique turn fades or just first 10 fades.
    for f in fades[:15]:
        print(f"Turn {f['turn']}, {f['tokens']} tokens, {f['latency']:.1f}s, Instruction: {f['instruction']}")

if __name__ == "__main__":
    audit()
