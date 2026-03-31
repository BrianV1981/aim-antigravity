#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import glob
import shutil
from datetime import datetime

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
UNREAD_PATH = os.path.join(AIM_ROOT, "continuity", "UNREAD_MAIL.md")

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
        print(f"[*] Cloning Swarm Post Office ({hub_repo})...")
        os.makedirs(os.path.dirname(HUB_LOCAL_DIR), exist_ok=True)
        try:
            subprocess.run(["gh", "repo", "clone", hub_repo, HUB_LOCAL_DIR], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to clone. Make sure `gh` CLI is authenticated and repo exists.")
            sys.exit(1)
    else:
        # Pull latest
        run_git(["pull", "origin", "main"])

def action_send(team_id, target_team, subject, body):
    target_dir = os.path.join(HUB_LOCAL_DIR, "inbox", target_team.lower())
    os.makedirs(target_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_subject = "".join(c if c.isalnum() else "_" for c in subject)[:30]
    filename = f"{timestamp}_{safe_subject}.md"
    filepath = os.path.join(target_dir, filename)

    content = f"**From:** {team_id.upper()}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**Subject:** {subject}\n\n---\n\n{body}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[*] Depositing mail to: /inbox/{target_team.lower()}/")
    run_git(["add", "."])
    run_git(["commit", "-m", f"Mail: {team_id.upper()} -> {target_team.upper()}"])
    run_git(["push", "origin", "main"])
    print("[SUCCESS] Mail successfully dispatched to the Swarm Post Office.")

def action_check(team_id):
    inbox_dir = os.path.join(HUB_LOCAL_DIR, "inbox", team_id.lower())
    archive_dir = os.path.join(inbox_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    mail_files = []
    if os.path.exists(inbox_dir):
        for f in os.listdir(inbox_dir):
            if f.endswith(".md"):
                mail_files.append(os.path.join(inbox_dir, f))

    if not mail_files:
        print("[SUCCESS] Inbox is empty. Nothing new to read.")
        return

    print(f"[*] Found {len(mail_files)} new piece(s) of mail.")
    
    compiled_mail = f"\n\n## 📨 NEW MAIL FETCHED: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    for mf in mail_files:
        with open(mf, 'r', encoding='utf-8') as f:
            compiled_mail += f"{f.read()}\n\n---\n"
        # Move to archive securely
        shutil.move(mf, os.path.join(archive_dir, os.path.basename(mf)))

    # Append to local UNREAD_MAIL.md
    with open(UNREAD_PATH, "a", encoding="utf-8") as f:
        f.write(compiled_mail)

    print("[*] Archiving fetched mail on remote...")
    run_git(["add", "."])
    run_git(["commit", "-m", f"Mail: {team_id.upper()} fetched {len(mail_files)} message(s)"])
    run_git(["push", "origin", "main"])
    
    print(f"[SUCCESS] Mail imported to continuity/UNREAD_MAIL.md!")

def main():
    if len(sys.argv) < 2:
        print("Usage: aim_mail.py <send|check> [args]")
        sys.exit(1)

    action = sys.argv[1]
    
    swarm_settings = load_swarm_config()
    hub_repo = swarm_settings.get("hub_repo")
    team_id = swarm_settings.get("team_id", "unknown-team")

    if not hub_repo:
        print("[ERROR] No 'hub_repo' configured in core/CONFIG.json.")
        sys.exit(1)

    print("--- A.I.M. Swarm Post Office ---")
    ensure_hub_cloned(hub_repo)

    if action == "send":
        if len(sys.argv) < 5:
            print("Usage: aim_mail.py send <target_team> <subject> <body>")
            sys.exit(1)
        target = sys.argv[2]
        subj = sys.argv[3]
        body = sys.argv[4]
        action_send(team_id, target, subj, body)
    elif action == "check":
        action_check(team_id)
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
