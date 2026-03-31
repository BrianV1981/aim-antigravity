#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
import time

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
    sender = "unknown"
    body_lines = []
    parsing_body = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith("**Subject:**"):
            subject = line.replace("**Subject:**", "").strip()
        elif line.startswith("**From:**"):
            sender = line.replace("**From:**", "").strip().lower()
        elif line.strip() == "---" and not parsing_body:
            parsing_body = True
        elif parsing_body:
            body_lines.append(line)
            
    return sender, subject, "".join(body_lines).strip()

def action_moderate():
    inbox_base = os.path.join(HUB_LOCAL_DIR, "inbox")
    mail_files = []
    if not os.path.exists(inbox_base): return

    for root, dirs, files in os.walk(inbox_base):
        if "escalated" in root or "archive" in root: continue
        for f in files:
            if f.endswith(".md") and f != ".gitkeep":
                mail_files.append(os.path.join(root, f))
    
    groups = {}
    for mf in mail_files:
        sender, subject, _ = parse_mail(mf)
        groups.setdefault((sender, subject), []).append(mf)
        
    deleted_spams = 0
    spam_senders_warned = set()
    
    for (sender, subject), files in groups.items():
        if len(files) >= 5:
            print(f"[!] [MODERATOR] Spam Loop Detected from {sender.upper()} on subject '{subject}' ({len(files)} identical drops).")
            files.sort()
            for mf in files[1:]:
                os.remove(mf)
                deleted_spams += 1
            if sender not in spam_senders_warned and sender != "unknown":
                print(f"[!] [MODERATOR] Issuing native Spam Warning drop to {sender.upper()}...")
                subprocess.run([sys.executable, os.path.join(AIM_ROOT, 'scripts', 'aim_mail.py'), 'send', sender, "[SPAM WARNING] Loop Detected", f"The Moderator daemon has detected your Turing-Tarpit recursion loop regarding the subject '{subject}'. The network has purged your looping spam requests. Please snap your context loop immediately."], check=False)
                spam_senders_warned.add(sender)
                
    if deleted_spams > 0:
        print(f"[*] Postmaster successfully quarantined {deleted_spams} spam loop file(s).")
        run_git(["add", "."])
        run_git(["commit", "-m", f"Moderator: Purged {deleted_spams} recursive spam loops from network queue"])
        run_git(["push", "origin", "main"])
        print("[SUCCESS] Global Chalkboard purified.")

def action_escalate(team_id):
    inbox_dir = os.path.join(HUB_LOCAL_DIR, "inbox", team_id.lower())
    escalated_dir = os.path.join(inbox_dir, "escalated")
    os.makedirs(escalated_dir, exist_ok=True)
    
    mail_files = []
    if os.path.exists(inbox_dir):
        for f in os.listdir(inbox_dir):
            if f.endswith(".md"): mail_files.append(os.path.join(inbox_dir, f))

    if not mail_files: return

    escalated_count = 0
    gh_exe = shutil.which("gh")
    if not gh_exe and os.path.exists(r"C:\Program Files\GitHub CLI\gh.exe"):
        gh_exe = r"C:\Program Files\GitHub CLI\gh.exe"

    for mf in mail_files:
        _, subject, body = parse_mail(mf)
        
        if "[URGENT]" in subject.upper() or "[TICKET]" in subject.upper() or "[ISSUE]" in subject.upper():
            print(f"    -> [MATCH] Escalating '{subject}' to parent GitHub Issues...")
            if not gh_exe:
                print("[ERROR] GitHub CLI (gh) not found on PATH. Postmaster cannot function.")
                break
            try:
                subprocess.run([gh_exe, "issue", "create", "--title", subject, "--body", body], cwd=AIM_ROOT, check=True)
                escalated_count += 1
                shutil.move(mf, os.path.join(escalated_dir, os.path.basename(mf)))
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to push GitHub Issue: {e}")

    if escalated_count > 0:
        print(f"[*] Postmaster successfully routed {escalated_count} native GitHub Action(s). Synchronizing Swarm Hub...")
        run_git(["add", "."])
        run_git(["commit", "-m", f"Postmaster: {team_id.upper()} escalated {escalated_count} message(s) to native GitHub tracking"])
        run_git(["push", "origin", "main"])
        print("[SUCCESS] GitHub Issue board updated.")

def action_daemon(team_id, interval):
    print(f"[*] Synthesizing Postmaster Daemon (Polling Interval: {interval} minutes)")
    print(f"[*] Network: aim-chalkboard | Core Anchor: {team_id.upper()}")
    while True:
        print("\n[*] --- Postmaster Heartbeat Sweep ---")
        run_git(["pull", "origin", "main"])
        action_moderate()
        action_escalate(team_id)
        print(f"[*] --- Sweep Terminated. Sleeping for {interval} minutes ---")
        time.sleep(int(interval) * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: aim_postmaster.py <escalate|daemon>")
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
    elif action == "daemon":
        interval = 5
        if "--interval" in sys.argv:
            idx = sys.argv.index("--interval")
            if idx + 1 < len(sys.argv):
                interval = int(sys.argv[idx+1])
        action_daemon(team_id, interval)
    else:
        print(f"Unknown Postmaster action: {action}")

if __name__ == "__main__":
    main()
