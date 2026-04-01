import os
import glob
import re
import json
import sys

def get_latest_conversation_dir(brain_dir):
    """Finds the most recently modified conversation directory."""
    try:
        dirs = [os.path.join(brain_dir, d) for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
        if not dirs:
            return None
        return max(dirs, key=os.path.getmtime)
    except Exception as e:
        print(f"Error finding brain dir: {e}")
        return None

def extract_signal():
    print("[*] Initiating A.I.M. Continuity Extraction Pipeline...")
    
    # Path to Antigravity brain memory
    brain_dir = os.path.expanduser(r"~\.gemini\antigravity\brain")
    if not os.path.exists(brain_dir):
        # Fallback to direct absolute known path if ~ expansion fails in windows
        brain_dir = r"C:\Users\kingb\.gemini\antigravity\brain"
        
    latest_dir = get_latest_conversation_dir(brain_dir)
    
    if not latest_dir:
        print("[!] Fatal: Could not locate active Antigravity session framework.")
        return

    log_file = os.path.join(latest_dir, ".system_generated", "logs", "overview.txt")
    out_file = os.path.join(os.getcwd(), "continuity", "LAST_SESSION_FLIGHT_RECORDER.md")
    
    # Create continuity directory if it doesn't exist
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    if not os.path.exists(log_file):
        print(f"[!] Warning: overview.txt not found at {log_file}.")
        print("[*] Generating fallback stub to prevent pipeline crash...")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("# A.I.M. Flight Recorder Transcript\n\n> [!WARNING]\n> `overview.txt` was not yet flushed to disk. Transcript is currently locked in memory.\n")
        return

    print(f"[*] Parsing literal system transcript: {log_file}")
    
    output_lines = ["# 🔄 A.I.M. Flight Recorder Transcript\n\n*Forensic log synthesized actively from zero-token shell.*\n---"]
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Rough heuristic to strip massive unformatted JSON blobs from logs
        # while keeping the human-readable dialogue and tool calls distinct.
        lines = content.split('\n')
        
        in_noise_block = False
        for line in lines:
            # Reformat system tool calls to readable commands
            if "call:default_api:" in line or "response:default_api:" in line:
                output_lines.append(f"\n> **[SYSTEM TOOL CALL]** `{line.strip()}`\n")
                continue
                
            strip_line = line.strip()
            
            # Simple toggle to remove deep dict noise if the backend spits raw JSON
            if strip_line == '{' or (strip_line.startswith('{') and len(strip_line) < 50):
                in_noise_block = True
                continue
            if in_noise_block and (strip_line == '}' or strip_line.startswith('}')):
                in_noise_block = False
                continue
                
            if not in_noise_block:
                output_lines.append(line)

        # Output to local
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
            
        print(f"[SUCCESS] Forensic Flight Recorder extracted and saved to: {out_file}")

        # --- ZERO API PULSE GENERATION ---
        last_actions = [line for line in output_lines if 'TOOL CALL' in line]
        pulse_content = "# Current Pulse (Automated Local Extraction)\n\n### Recent Execution Trajectory:\n"
        for act in last_actions[-5:]:
            pulse_content += f"- {act.replace('> **[SYSTEM TOOL CALL]**', '').strip()}\n"
        
        pulse_path = os.path.join(os.path.dirname(out_file), "CURRENT_PULSE.md")
        with open(pulse_path, "w", encoding="utf-8") as f:
            f.write(pulse_content)
        print(f"[SUCCESS] CURRENT_PULSE synthesized via Python zero-token parser.")

        # --- ZERO API GAMEPLAN GENERATION ---
        intent_str = "No specific commander intent provided."
        if "--intent" in sys.argv:
            idx = sys.argv.index("--intent")
            if idx + 1 < len(sys.argv):
                intent_str = sys.argv[idx + 1]

        gameplan_content = f"# Reincarnation Gameplan\n\n### Commander's Intent:\n> {intent_str}\n\n### Immediate Directives for Next Agent:\n1. Re-establish context via the Flight Recorder if necessary.\n2. Resume terminal execution trajectory from the CURRENT_PULSE.md.\n3. Implement the Commander's explicit objective."
        
        gameplan_path = os.path.join(os.path.dirname(out_file), "REINCARNATION_GAMEPLAN.md")
        with open(gameplan_path, "w", encoding="utf-8") as f:
            f.write(gameplan_content)
        print(f"[SUCCESS] REINCARNATION_GAMEPLAN mechanically mapped via Python.")

    except Exception as e:
        print(f"[!] Extraction Pipeline Failure: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "extract":
        extract_signal()
    else:
        print("Usage: python aim_continuity.py extract")

if __name__ == "__main__":
    main()
