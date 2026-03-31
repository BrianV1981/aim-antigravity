#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil

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
CONFIG_PATH = os.path.join(AIM_ROOT, "core", "CONFIG.json")
HUB_LOCAL_DIR = os.path.join(AIM_ROOT, "archive", "swarm_hub")

def load_swarm_config():
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
                return cfg.get("swarm_settings", {})
    except Exception as e:
        print(f"[ERROR] Could not load CONFIG: {e}")
    return {}

def run_git(args, cwd=HUB_LOCAL_DIR):
    try:
        subprocess.run(["git"] + args, cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git operation failed: git {' '.join(args)}")
        sys.exit(1)

def ensure_hub_cloned(hub_repo):
    if not os.path.exists(HUB_LOCAL_DIR):
        print(f"[*] Postmaster cloning Swarm Post Office ({hub_repo})...")
        os.makedirs(os.path.dirname(HUB_LOCAL_DIR), exist_ok=True)
        try:
            subprocess.run(["git", "clone", f"https://github.com/{hub_repo}.git", HUB_LOCAL_DIR], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to clone. Make sure the Hub exists.")
            sys.exit(1)
    else:
        run_git(["pull", "origin", "main"])

def parse_mail(filepath):
    subject = "Swarm Mail"
    body_lines = []
    parsing_body = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith("**Subject:**"):
            subject = line.replace("**Subject:**", "").strip()
        elif line.strip() == "---" and not parsing_body:
            parsing_body = True
        elif parsing_body:
            body_lines.append(line)
            
    return subject, "".join(body_lines).strip()

def action_escalate(team_id):
    inbox_dir = os.path.join(HUB_LOCAL_DIR, "inbox", team_id.lower())
    escalated_dir = os.path.join(inbox_dir, "escalated")
    os.makedirs(escalated_dir, exist_ok=True)
    
    mail_files = []
    if os.path.exists(inbox_dir):
        for f in os.listdir(inbox_dir):
            if f.endswith(".md"):
                mail_files.append(os.path.join(inbox_dir, f))

    if not mail_files:
        print("[*] Postmaster found no mail to scan for escalations.")
        return

    escalation_str = "[URGENT], [TICKET], [ISSUE]"
    print(f"[*] Postmaster scanning {len(mail_files)} mail fragment(s) for tags: {escalation_str}")
    
    escalated_count = 0
    gh_exe = shutil.which("gh")
    if not gh_exe:
        # Fallback to local Windows path
        if os.path.exists(r"C:\Program Files\GitHub CLI\gh.exe"):
            gh_exe = r"C:\Program Files\GitHub CLI\gh.exe"
        else:
            print("[ERROR] GitHub CLI (gh) not found on PATH. Postmaster cannot function.")
            sys.exit(1)

    for mf in mail_files:
        subject, body = parse_mail(mf)
        
        # Determine if it qualifies mapping to the Issue board
        if "[URGENT]" in subject.upper() or "[TICKET]" in subject.upper() or "[ISSUE]" in subject.upper():
            print(f"    -> [MATCH] Escalating '{subject}' to parent GitHub Issues...")
            
            # Using gh issue create locally opens it in the CURRENT repository
            # Since the script runs from AIM_ROOT, it will bind to aim-antigravity natively
            try:
                subprocess.run([gh_exe, "issue", "create", "--title", subject, "--body", body], cwd=AIM_ROOT, check=True)
                escalated_count += 1
                
                # Move to the escalated folder natively in the Post Office so aim_mail.py check skips it!
                shutil.move(mf, os.path.join(escalated_dir, os.path.basename(mf)))
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to push GitHub Issue: {e}")

    if escalated_count > 0:
        print(f"[*] Postmaster successfully routed {escalated_count} issue(s). Synchronizing Swarm Hub...")
        run_git(["add", "."])
        run_git(["commit", "-m", f"Postmaster: {team_id.upper()} escalated {escalated_count} message(s) to native GitHub tracking"])
        run_git(["push", "origin", "main"])
        print("[SUCCESS] GitHub Issue board updated.")
    else:
        print("[*] Postmaster verified no issues required escalation.")

def main():
    if len(sys.argv) < 2:
        print("Usage: aim_postmaster.py <escalate>")
        sys.exit(1)

    action = sys.argv[1]
    
    swarm_settings = load_swarm_config()
    hub_repo = swarm_settings.get("hub_repo")
    team_id = swarm_settings.get("team_id", "unknown-team")

    if not hub_repo:
        print("[ERROR] No 'hub_repo' configured in core/CONFIG.json.")
        sys.exit(1)

    ensure_hub_cloned(hub_repo)

    if action == "escalate":
        action_escalate(team_id)
    else:
        print(f"Unknown Postmaster action: {action}")

if __name__ == "__main__":
    main()
