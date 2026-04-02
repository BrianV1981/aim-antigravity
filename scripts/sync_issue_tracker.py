#!/usr/bin/env python3
"""
A.I.M. Issue Synchronizer — Dynamic Multi-Repo Edition

Pulls open issues from the CURRENT repository (auto-detected via git remote)
and optionally merges issues from the cross-swarm hub_repo if configured in
core/CONFIG.json. Each A.I.M. deployment gets its own issues automatically.
"""
import os
import sys
import json
import subprocess
import re
from datetime import datetime

def find_aim_root():
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "core/CONFIG.json")): return current
        if os.path.exists(os.path.join(current, "setup.sh")): return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
CONTINUITY_DIR = os.path.join(AIM_ROOT, "continuity")
TRACKER_PATH = os.path.join(CONTINUITY_DIR, "ISSUE_TRACKER.md")
CONFIG_PATH = os.path.join(AIM_ROOT, "core", "CONFIG.json")

def detect_current_repo():
    """Auto-detect the current repo from git remote origin."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True, cwd=AIM_ROOT
        )
        url = result.stdout.strip()
        # Handle HTTPS: https://github.com/Owner/Repo.git
        match = re.search(r'github\.com[:/](.+?)(?:\.git)?$', url)
        if match:
            return match.group(1)
    except subprocess.CalledProcessError:
        pass
    
    # Fallback: try gh CLI
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True, text=True, check=True, cwd=AIM_ROOT
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        pass
    
    return None

def get_hub_repo():
    """Read the optional cross-swarm hub_repo from CONFIG.json."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
                return cfg.get("swarm_settings", {}).get("hub_repo")
    except:
        pass
    return None

def fetch_issues(repo=None, state="open", limit=100):
    """Fetch issues from a specific repo or the current repo."""
    cmd = ["gh", "issue", "list", "--state", state, "--limit", str(limit),
           "--json", "number,title,labels,createdAt"]
    if repo:
        cmd.extend(["--repo", repo])
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, cwd=AIM_ROOT
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to fetch {state} issues from {repo or 'current repo'}: {e.stderr}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to parse GitHub CLI output.")
        return []

def format_issues(issues):
    """Format a list of issues into markdown bullet points."""
    if not issues:
        return "*No open issues found.*\n\n"
    lines = ""
    for issue in issues:
        labels = ", ".join([label['name'] for label in issue.get('labels', [])])
        label_str = f" [{labels}]" if labels else ""
        date_str = issue.get('createdAt', '')[:10]
        lines += f"* **#{issue['number']}** - {issue['title']}{label_str} *(Created: {date_str})*\n"
    return lines

def generate_markdown(current_repo, current_issues, hub_repo=None, hub_issues=None):
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    
    md = f"# A.I.M. Issue Ledger\n\n"
    md += f"*Last Synchronized: {now}*\n"
    md += f"*This file serves as the local, zero-latency index of all active project tasks.*\n\n"
    
    # Section 1: Current repo issues (always present)
    md += f"## 🟢 OPEN ISSUES — `{current_repo or 'Local Repo'}`\n\n"
    md += format_issues(current_issues)
    md += "\n"
    
    # Section 2: Hub repo issues (only if configured and different from current)
    if hub_repo and hub_issues is not None:
        md += f"## 🌐 CROSS-SWARM ISSUES — `{hub_repo}`\n\n"
        md += format_issues(hub_issues)
        md += "\n"
    
    return md

def main():
    print("--- A.I.M. ISSUE SYNCHRONIZER (Dynamic) ---")
    os.makedirs(CONTINUITY_DIR, exist_ok=True)
    
    # 1. Auto-detect current repo
    current_repo = detect_current_repo()
    if current_repo:
        print(f"[1/3] Detected repo: {current_repo}")
    else:
        print("[1/3] WARNING: Could not detect current repo. Falling back to local `gh issue list`.")
    
    # 2. Fetch current repo issues
    print(f"[2/3] Fetching OPEN issues from {current_repo or 'current repo'}...")
    current_issues = fetch_issues(repo=current_repo)
    print(f"      Found {len(current_issues)} open issues.")
    
    # 3. Optionally fetch hub repo issues (if configured and different)
    hub_repo = get_hub_repo()
    hub_issues = None
    if hub_repo and hub_repo != current_repo:
        print(f"[3/3] Fetching OPEN issues from cross-swarm hub: {hub_repo}...")
        hub_issues = fetch_issues(repo=hub_repo)
        print(f"      Found {len(hub_issues)} hub issues.")
    else:
        print("[3/3] No separate hub repo configured (or same as current). Skipping cross-swarm sync.")
    
    # 4. Write the tracker
    markdown_content = generate_markdown(current_repo, current_issues, hub_repo if hub_issues else None, hub_issues)
    
    with open(TRACKER_PATH, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"\n[SUCCESS] Local Issue Ledger written to: {TRACKER_PATH}")
    print(f"          {len(current_issues)} local issues" + (f" + {len(hub_issues)} hub issues" if hub_issues else ""))

if __name__ == "__main__":
    main()