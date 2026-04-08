#!/usr/bin/env python3
"""
run_tests.py — A.I.M. Full Test Suite Runner

Runs the entire pytest suite and prints a clean summary.
Usage: python scripts/run_tests.py
"""
import subprocess
import sys
import os
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AIM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 60)
    print("  A.I.M. Test Suite Runner")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-q"],
        cwd=AIM_ROOT,
        capture_output=False
    )

    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("  ✅ ALL TESTS PASSED")
    else:
        print("  ❌ FAILURES DETECTED")
    print("=" * 60)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
