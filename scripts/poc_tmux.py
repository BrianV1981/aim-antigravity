#!/usr/bin/env python3
import subprocess
import time
import sys

def send_to_tmux(session, text):
    """Sends raw text to a tmux session and hits Enter."""
    print(f"[*] Sending message to {session}...")
    # Using raw string injection for simplicity
    subprocess.run(["tmux", "send-keys", "-t", session, text, "C-m"], check=True)

def read_from_tmux(session):
    """Captures the current screen of the tmux session."""
    print(f"[*] Reading screen from {session}...")
    result = subprocess.run(["tmux", "capture-pane", "-p", "-t", session], capture_output=True, text=True)
    return result.stdout.strip()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 poc_tmux.py <tmux_session_name> <message>")
        sys.exit(1)
        
    target_session = sys.argv[1]
    message = sys.argv[2]
    
    # 1. Send the message
    send_to_tmux(target_session, message)
    
    # 2. Wait a few seconds for the agent to think and reply
    print("[*] Waiting 5 seconds for agent to respond...")
    time.sleep(5)
    
    # 3. Read the screen and print it
    output = read_from_tmux(target_session)
    
    print("\n--- TMUX SCREEN OUTPUT ---")
    # Print the last 15 lines of the terminal so we can see the response
    lines = output.split('\n')
    for line in lines[-15:]:
        print(line)
    print("--------------------------")
