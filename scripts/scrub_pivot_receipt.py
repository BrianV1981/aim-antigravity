import json
import os
from datetime import datetime

input_file = os.path.expanduser("~/.gemini/tmp/aim/chats/session-2026-03-30T10-31-99e6820b.json")
output_json = "docs/RECEIPT_THE_PIVOT_SCRUBBED.json"

with open(input_file, 'r') as f:
    data = json.load(f)

messages = data.get('messages', [])
scrubbed_log = []

for i, msg in enumerate(messages):
    role = msg.get('role')
    timestamp = msg.get('timestamp')
    
    entry = {
        "turn": i + 1,
        "role": role,
        "timestamp": timestamp,
    }
    
    # Calculate Latency if previous exists
    if i > 0 and 'timestamp' in messages[i-1] and timestamp:
        try:
            t1 = datetime.fromisoformat(messages[i-1]['timestamp'].replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            entry['latency_seconds'] = (t2 - t1).total_seconds()
        except:
            pass
            
    if role == 'user':
        text = msg.get('text', '')
        # Only keep key quotes, scrub the rest
        if "push it to main" in text.lower():
            entry['event'] = "USER DIRECTIVE: Evaluate branches and push to main"
            entry['quote'] = "push it to main, anmd see evaluate the other branches"
        elif "hold on, what new docs" in text.lower():
            entry['event'] = "USER INTERVENTION: Halting rogue deletion"
            entry['quote'] = "hold on, what new docs? are they update wiki pages etc?"
        elif "restore all branches" in text.lower():
            entry['event'] = "USER DIRECTIVE: Emergency Restoration"
            entry['quote'] = "restore all branches that did not commit"
        elif "today was a disaster" in text.lower():
            entry['event'] = "USER DECLARATION: The Pivot"
            entry['quote'] = "Ok, today was a disaster and I need you to go back and check/review what happened"
        else:
            entry['event'] = "User Input (Scrubbed)"
            
    elif role == 'gemini':
        # Track tools used
        tools_used = []
        for action in msg.get('actions', []):
            tool_name = action.get('tool')
            if tool_name:
                intent = action.get('intent', '{}')
                try:
                    intent_dict = json.loads(intent)
                    if tool_name == 'run_shell_command':
                        tools_used.append(f"run_shell_command: {intent_dict.get('command', '')[:50]}...")
                    else:
                        tools_used.append(tool_name)
                except:
                    tools_used.append(tool_name)
        
        entry['tools_executed'] = tools_used
        entry['event'] = "Agent Action (Content Scrubbed)"
        
        # Check for the rogue deletion command
        for tool in tools_used:
            if "git branch -D" in tool or "git push origin --delete" in tool:
                entry['CRITICAL_EVENT'] = "ROGUE MASS DELETION EXECUTED"

    scrubbed_log.append(entry)

with open(output_json, 'w') as f:
    json.dump(scrubbed_log, f, indent=2)

print(f"Successfully scrubbed {len(messages)} turns. Saved to {output_json}")
