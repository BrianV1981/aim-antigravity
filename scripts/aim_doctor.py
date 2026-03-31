#!/usr/bin/env python3
import sys
import os
import subprocess
import sqlite3

def check_command(cmd, name):
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"[OK] {name} is installed and available.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"[FAIL] {name} is missing or broken.")
        return False

def check_python_version():
    if sys.version_info >= (3, 10):
        print(f"[OK] Python version {sys.version_info.major}.{sys.version_info.minor} is supported.")
        return True
    else:
        print(f"[FAIL] Python version must be >= 3.10. Current: {sys.version_info.major}.{sys.version_info.minor}")
        return False

def check_sqlite():
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        conn.close()
        print(f"[OK] SQLite3 {version} is functional.")
        return True
    except Exception as e:
        print(f"[FAIL] SQLite3 is broken: {e}")
        return False

def check_keyring_deps():
    if sys.platform.startswith('linux'):
        print("[INFO] Linux detected. Checking for dbus-x11 and libdbus-1-dev...")
        try:
            import dbus
            print("[OK] dbus Python bindings found.")
        except ImportError:
            print("[WARNING] Python 'dbus' module missing. Keyring might fail on headless Linux.")
    else:
        print(f"[OK] OS Keyring dependencies natively supported on {sys.platform}.")
    return True

def main():
    print("--- A.I.M. SYSTEM DOCTOR ---\n")
    checks = [
        check_python_version(),
        check_command(["git", "--version"], "Git"),
        check_sqlite(),
        check_keyring_deps()
    ]
    
    print("\n--- DIAGNOSTIC COMPLETE ---")
    if all(checks):
        print("[SUCCESS] All core environment dependencies are healthy.")
    else:
        print("[ERROR] One or more system dependencies failed. A.I.M. may not function correctly.")

if __name__ == "__main__":
    main()