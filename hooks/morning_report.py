#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

AIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTINUITY_DIR = os.path.join(AIM_ROOT, "continuity")
REPORT_PATH = os.path.join(CONTINUITY_DIR, "MORNING_REPORT.md")

def get_git_state():
    try:
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=AIM_ROOT).stdout.strip()
        status = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, cwd=AIM_ROOT).stdout.strip()
        recent_log = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True, cwd=AIM_ROOT).stdout.strip()
        
        state = f"**Active Branch:** `{branch}`\n"
        state += f"**Latest Commit:** `{recent_log}`\n"
        if status:
            state += f"**Pending Changes (git status):**\n```\n{status}\n```\n"
        else:
            state += "**Working Tree:** Clean\n"
        return state
    except Exception as e:
        return f"*Git state unavailable: {e}*\n"

def get_latest_memory():
    memory_path = os.path.join(AIM_ROOT, "MEMORY.md")
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Grab the last 1500 chars (usually the most recent single-shot delta)
            return content[-1500:] 
    return "*No memory axioms exist yet.*\n"

def get_issue_tracker():
    tracker_path = os.path.join(CONTINUITY_DIR, "ISSUE_TRACKER.md")
    if os.path.exists(tracker_path):
        with open(tracker_path, "r", encoding="utf-8") as f:
            return f.read()
    return "*Issue Tracker empty. Run sync_issue_tracker.py*\n"

def generate_morning_report():
    os.makedirs(CONTINUITY_DIR, exist_ok=True)
    
    report = f"# A.I.M. Executive Morning Briefing\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += "## 1. Local Repository State (GitOps)\n"
    report += get_git_state() + "\n\n"
    
    report += "## 2. Active Radar (Issue Tracker)\n"
    report += get_issue_tracker() + "\n\n"
    
    report += "## 3. Deep Memory Context (Recent Architectural Deltas)\n"
    report += "```md\n...[TRUNCATED HISTORY]...\n"
    report += get_latest_memory() + "\n```\n\n"
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"      [A.I.M] Executive Morning Briefing written to {os.path.basename(REPORT_PATH)}.")

if __name__ == "__main__":
    generate_morning_report()
