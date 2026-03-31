import os
import re

WIKI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "antigravity.wiki")

def fix_wiki():
    if not os.path.exists(WIKI_DIR):
        print(f"[ERROR] Could not locate wiki at {WIKI_DIR}")
        return

    # Dynamically find the files since Windows/WSL might have mapped the colon to an obscure Unicode char
    files = os.listdir(WIKI_DIR)
    
    file_mapping = {}
    
    for f in files:
        if "Actual-Intelligent-Memory" in f and "Grok" in f:
            new_name = "A.I.M.-Actual-Intelligent-Memory-Review-(Grok-Conversation,-March-25,-2026).md"
            if f != new_name:
                file_mapping[f] = new_name
            
        if "MMO-Botter" in f and "Curse-of-Knowledge" in f:
            new_name = "The-MMO-Botters-Advantage-A-Case-Study-in-the-Curse-of-Knowledge.md"
            if f != new_name:
                file_mapping[f] = new_name

    for old_file, new_file in file_mapping.items():
        old_path = os.path.join(WIKI_DIR, old_file)
        new_path = os.path.join(WIKI_DIR, new_file)
        safe_old = old_file.encode('ascii', 'replace').decode('ascii')
        print(f"[*] Renaming physical file:\n    Old: {safe_old}\n    New: {new_file}")
        
        # Git doesn't like moving files if its index is corrupted due to the WSL mapping
        # So we literally rename the file in the physical OS, and we will just let git track the deletion/creation
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"[ERROR] Could not rename {old_file} -> {new_file}: {e}")

    # Now we need to update all 54 Markdown files replacing internal linking strings
    # We must replace both the exact Unicode mapping (if it was copied directly) 
    # and the original `:` character used by the Linux agents.
    
    replacements = [
        # Search targets for A.I.M. Grok Review
        ("A.I.M.:-Actual-Intelligent-Memory-Review-(Grok-Conversation,-March-25,-2026)", "A.I.M.-Actual-Intelligent-Memory-Review-(Grok-Conversation,-March-25,-2026)"),
        ("A.I.M.-Actual-Intelligent-Memory-Review-(Grok-Conversation,-March-25,-2026)", "A.I.M.-Actual-Intelligent-Memory-Review-(Grok-Conversation,-March-25,-2026)"),
        
        # Search targets for MMO Botters Advantage
        ("The-MMO-Botter's-Advantage:-A-Case-Study-in-the-Curse-of-Knowledge", "The-MMO-Botters-Advantage-A-Case-Study-in-the-Curse-of-Knowledge"),
        ("The-MMO-Botter's-Advantage-A-Case-Study-in-the-Curse-of-Knowledge", "The-MMO-Botters-Advantage-A-Case-Study-in-the-Curse-of-Knowledge")
    ]
    
    md_files = [f for f in os.listdir(WIKI_DIR) if f.endswith('.md')]
    mod_count = 0
    
    for md_file in md_files:
        path = os.path.join(WIKI_DIR, md_file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            original_content = content
            for old_str, new_str in replacements:
                content = content.replace(old_str, new_str)
                
            if content != original_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                mod_count += 1
                print(f"[+] Rebuilt internal links inside: {md_file}")
                
        except Exception as e:
            print(f"[WARNING] Skipping link parsing in {md_file}: {e}")

    print(f"\n[*] Total files structurally repaired: {mod_count}")

if __name__ == "__main__":
    fix_wiki()
