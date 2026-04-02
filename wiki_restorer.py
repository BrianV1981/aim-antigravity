import os
import shutil

TARGET_WIKI = r"c:\Users\kingb\aim-antigravity\antigravity.wiki"
SOURCE_WIKI = r"\\wsl.localhost\Ubuntu\home\kingb\aim\aim.wiki"

PROTECTED_FILES = {
    'Antigravity-Initialization-Architecture.md',
    'Testing-and-TDD-Architecture.md',
    'The-Swarm-Post-Office.md',
    'Handoff-Architecture-Guide.md',
    '_Sidebar.md'
}

def sanitize_filename(filename):
    # WSL maps invalid windows characters like colon (:) to a special unicode char \uf03a
    # We will just replace it with a dash to be safe on Windows.
    return filename.replace(chr(0xf03a), '-')

# Phase 1: The Purge
for filename in os.listdir(TARGET_WIKI):
    if filename == '.git' or filename in PROTECTED_FILES:
        continue
    filepath = os.path.join(TARGET_WIKI, filename)
    if os.path.isfile(filepath):
        print(f"[PURGE] Deleting: {filename}")
        os.remove(filepath)

# Phase 2: The Import
for filename in os.listdir(SOURCE_WIKI):
    if filename == '.git':
        continue
        
    sanitized_name = sanitize_filename(filename)
    
    # Don't overwrite the newly authored files with old ones from aim.wiki
    if sanitized_name in PROTECTED_FILES:
        print(f"[SKIP] Keeping local protected file: {sanitized_name}")
        continue
        
    source_path = os.path.join(SOURCE_WIKI, filename)
    target_path = os.path.join(TARGET_WIKI, sanitized_name)
    
    if os.path.isfile(source_path):
        print(f"[IMPORT] Copying {sanitized_name}...")
        shutil.copy2(source_path, target_path)

print("[SUCCESS] Wiki Purge and Import Complete!")
