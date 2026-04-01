import os
import re

directories = ["src", "scripts", "hooks", "skills", "tests"]
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pattern = re.compile(r'sys\.path\.append\((.+?)\)')
replacement = r'sys.path.insert(0, \1)'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, count = pattern.subn(replacement, content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[{count} replacements] {os.path.relpath(filepath, root_dir)}")
        return count
    return 0

total_replacements = 0
for d in directories:
    dir_path = os.path.join(root_dir, d)
    if not os.path.exists(dir_path): continue
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                total_replacements += process_file(path)

print(f"\n[DONE] Swept repository. {total_replacements} total 'sys.path.append' -> 'sys.path.insert(0)' replacements made.")
