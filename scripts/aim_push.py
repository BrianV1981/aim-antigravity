#!/usr/bin/env python3
import os
import sys
import subprocess

def find_aim_root():
    current = os.path.abspath(os.getcwd())
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, "core/CONFIG.json")): return current
        if os.path.exists(os.path.join(current, "setup.ps1")): return current
        if os.path.exists(os.path.join(current, "setup.sh")): return current
        current = os.path.dirname(current)
        if current.endswith(':\\') or current == '\\': break
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()

def get_current_branch():
    try:
        res = subprocess.run(["git", "branch", "--show-current"], cwd=AIM_ROOT, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return "main"

def add_tracked_files():
    try:
        # Instead of `git add .`, we only stage semantic files manually then `git add -u` (tracked files only)
        # This prevents the Swarm logic from accidentally sweeping massive data-lake files.
        subprocess.run(["git", "add", "VERSION", "CHANGELOG.md"], cwd=AIM_ROOT, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "add", "-u"], cwd=AIM_ROOT, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to stage files: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python aim_push.py '<msg>'")
        sys.exit(1)

    commit_msg = sys.argv[1].strip()
    
    version = "v1.0.0"
    version_file = os.path.join(AIM_ROOT, "VERSION")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            version = f.read().strip()

    print("[*] Staging tracked modifications...")
    add_tracked_files()
    
    # We allow the commit to fail gracefully if there is nothing to commit
    print(f"[*] Committing: {commit_msg}")
    subprocess.run([
        "git", "commit", 
        "-m", commit_msg, 
        "-m", f"Version: {version}"
    ], cwd=AIM_ROOT)

    branch = get_current_branch()
    print(f"[*] Pushing local branch '{branch}' to origin...")
    try:
        subprocess.run(["git", "push", "-u", "origin", branch], cwd=AIM_ROOT, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Native Branch Push failed. Did GitHub block it? {e}")
        sys.exit(1)
        
    print(f"\n[SUCCESS] Successfully deployed alias architecture. Version: {version}")

if __name__ == "__main__":
    main()
