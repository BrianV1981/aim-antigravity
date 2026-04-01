#!/usr/bin/env python3
import json
import sys
import os

def extract_signal(json_path):
    """
    Surgically extracts the architectural signal from a session JSON.
    Removes raw tool outputs while keeping Intent, Thoughts, and Actions.
    Also extracts token counts and tool execution metrics for the Eureka Protocol.
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        messages = data.get('messages') or data.get('session_history')
        if messages is None:
            return []
            
        signal = []
        
        for msg in messages:
            if not isinstance(msg, dict):
                continue
                
            m_role = msg.get('role') or msg.get('type')
            ts = msg.get('timestamp', 'Unknown')
            
            # --- SIGNAL EXTRACTION ---
            fragment = { "role": m_role, "timestamp": ts }
            
            content = msg.get('content')
            tokens = msg.get('tokens', {})
            if tokens:
                fragment['tokens'] = tokens
            
            def process_content(c):
                if isinstance(c, list):
                    return " ".join([str(item.get('text', '')) for item in c if isinstance(item, dict) and 'text' in item])
                return str(c) if c is not None else ""

            if m_role == 'user' or m_role == 'system':
                fragment['text'] = process_content(content)
            
            elif m_role in ['gemini', 'model']:
                fragment['text'] = process_content(content)
                fragment['thoughts'] = msg.get('thoughts', [])
                
                # Capture the INTENT of the actions, not the raw output
                tool_calls = msg.get('toolCalls', []) or msg.get('tool_calls', [])
                fragment['actions'] = []
                for call in tool_calls:
                    if not isinstance(call, dict):
                        continue
                    name = call.get('name') or call.get('function', {}).get('name')
                    args = call.get('args') or call.get('function', {}).get('arguments')
                    fragment['actions'].append({ "tool": name, "intent": str(args)[:200] })
            else:
                # Skip tool results and other roles to maximize reduction
                continue
            
            signal.append(fragment)
            
        return signal
    except Exception as e:
        return f"Extraction Error: {e}"

def extract_signal_from_txt(txt_path):
    """
    Surgically extracts the architectural signal from an Antigravity overview.txt transcript.
    Acts as a proxy for the legacy JSON-based extract_signal, maintaining logic structure.
    """
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        signal = []
        in_noise_block = False
        
        for line in lines:
            if "call:default_api:" in line or "response:default_api:" in line:
                signal.append({"role": "system", "timestamp": "Unknown", "text": f"> **[SYSTEM TOOL CALL]** `{line.strip()}`"})
                continue
                
            strip_line = line.strip()
            if strip_line == '{' or (strip_line.startswith('{') and len(strip_line) < 50):
                in_noise_block = True
                continue
            if in_noise_block and (strip_line == '}' or strip_line.startswith('}')):
                in_noise_block = False
                continue
                
            if not in_noise_block and strip_line:
                signal.append({"role": "model", "timestamp": "Unknown", "text": strip_line})
                
        return signal
    except Exception as e:
        return f"Extraction Error: {e}"

def extract_signal_from_antigravity_steps(brain_dir):
    """
    Crawls the dynamic mid-session `.system_generated/steps` folders to extract
    the active tool trajectory when `overview.txt` has not yet been flushed.
    """
    import glob
    
    signal = []
    try:
        steps_path = os.path.join(brain_dir, ".system_generated", "steps", "*", "content.md")
        step_files = glob.glob(steps_path)
        
        # Sort files by their parent directory's numeric or chronological ordering
        step_files.sort(key=os.path.getmtime)
        
        for sf in step_files:
            try:
                with open(sf, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        # Extract the high-level intent, truncate the noise
                        truncated = content[:300] + "..." if len(content) > 300 else content
                        signal.append({"role": "model", "timestamp": "Unknown", "text": f"> **[SYSTEM STEP]**\n{truncated}"})
            except Exception:
                continue
                
        return signal
    except Exception as e:
        return f"Extraction Error: {e}"

def extract_latest_markdown_export():
    """
    Crawls the Windows Downloads folder for the most recent Antigravity `.md` export,
    strips the UI disclaimer framing, and returns the raw transcript string.
    """
    import glob
    try:
        downloads_path = os.path.expanduser(r"~\Downloads\*.md")
        md_files = glob.glob(downloads_path)
        if not md_files:
            return "[A.I.M] No native markdown export found in Downloads."
            
        latest_file = max(md_files, key=os.path.getmtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Strip the standard Antigravity "purely the output" disclaimer
        clean_lines = []
        skip = False
        for line in lines:
            if "Note: _This is purely the output" in line:
                skip = True
            elif skip and line.strip() == "":
                skip = False
            elif not skip:
                clean_lines.append(line)
                
        return "".join(clean_lines).strip()
    except Exception as e:
        return f"[A.I.M] Markdown Extraction Error: {e}"

def skeleton_to_markdown(skeleton, session_id):
    """
    Converts a JSON signal skeleton into a beautifully formatted Obsidian-native Markdown string.
    Zero API cost.
    """
    md = f"---\nSession: {session_id}\nType: Raw Backup\n---\n\n# A.I.M. Signal Skeleton\n\n"
    for turn in skeleton:
        role = turn.get('role', 'unknown').upper()
        text = turn.get('text', '').strip()
        ts = turn.get('timestamp', '')
        
        if role == 'USER':
            md += f"## 👤 USER ({ts})\n"
            if text:
                md += f"{text}\n\n"
        elif role == 'GEMINI' or role == 'MODEL':
            md += f"## 🤖 A.I.M. ({ts})\n"
            thoughts = turn.get('thoughts', [])
            if thoughts:
                md += "> **Internal Monologue:**\n"
                for thought in thoughts:
                    # Some thoughts are just strings, others are dicts
                    if isinstance(thought, dict):
                        desc = thought.get('description', '') or thought.get('text', '')
                        md += f"> * {desc}\n"
                    else:
                        md += f"> * {thought}\n"
                md += "\n"
            
            if text:
                md += f"{text}\n\n"
            
            actions = turn.get('actions', [])
            if actions:
                md += "**Tools Executed:**\n"
                for action in actions:
                    tool = action.get('tool', 'unknown')
                    intent = action.get('intent', '')
                    md += f"- `{tool}`: {intent}\n"
                md += "\n"
                
        md += "---\n\n"
    return md

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_signal.py <path_to_json>")
        sys.exit(1)
    
    result = extract_signal(sys.argv[1])
    print(json.dumps(result, indent=2))
