#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

def find_aim_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != '/':
        if os.path.exists(os.path.join(current, "core/CONFIG.json")): return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

AIM_ROOT = find_aim_root()
SKILLS_DIR = Path(AIM_ROOT) / "skills"
ARCHIVE_DIR = Path(AIM_ROOT) / "archive"

def _native_run(script_path: Path, args_dict: dict) -> str:
    if script_path.suffix == ".sh":
        cmd_base = ["bash", str(script_path)]
    else:
        cmd_base = [sys.executable, str(script_path)]
    if args_dict:
        cmd_base.append(json.dumps(args_dict))
        
    try:
        result = subprocess.run(
            cmd_base,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(Path(script_path).parent)
        )
        return result.stdout.strip() or result.stderr.strip() or "Skill completed."
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Skill timed out (60s limit)"})
    except Exception as e:
        return json.dumps({"error": f"Execution error: {str(e)}"})

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <skill_name> '<args_json>'")
        sys.exit(1)
        
    skill_name = sys.argv[1]
    args_json = sys.argv[2] if len(sys.argv) > 2 else "{}"
    
    script_path = SKILLS_DIR / f"{skill_name}.py"
    if not script_path.exists():
        script_path = SKILLS_DIR / f"{skill_name}.sh"
        if not script_path.exists():
            print(json.dumps({"error": f"Skill '{skill_name}' not found in tools directory."}))
            sys.exit(1)

    try:
        args_dict = json.loads(args_json) if args_json and args_json != "{}" else {}
        output = _native_run(script_path, args_dict)
        print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
