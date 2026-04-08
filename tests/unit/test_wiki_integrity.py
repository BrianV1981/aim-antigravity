import os
import re
import unittest
from pathlib import Path

# Paths to the wiki and sidebar
AIM_ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
WIKI_DIR = AIM_ROOT / "antigravity.wiki"
SIDEBAR_PATH = WIKI_DIR / "_Sidebar.md"

class TestWikiIntegrity(unittest.TestCase):
    
    def test_sidebar_links_exist(self):
        """Ensure all files listed in the _Sidebar.md officially exist inside the wiki."""
        self.assertTrue(SIDEBAR_PATH.exists(), "Wiki _Sidebar.md does not exist.")
        
        with open(SIDEBAR_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Match [[Page Name]] or [[Label|File-Name]] formats
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        broken_links = []
        
        for link in links:
            # Handle aliases like [[The GitOps Bridge|Feature-GitOps-Bridge]]
            # Or direct links like [[Home]]
            if "|" in link:
                target_file = link.split("|")[1].strip() + ".md"
            else:
                # GitHub allows spaces in wiki links that map to hyphens, but here let's check pure names or dashed 
                target_file = link.strip().replace(" ", "-") + ".md"
                
            # Handle Edge cases where files don't use hyphens exactly, just check if path exists
            p = WIKI_DIR / target_file
            if not p.exists():
                broken_links.append(target_file)
                
        self.assertEqual(len(broken_links), 0, f"Sidebar contains broken links: {broken_links}")
        
    def test_internal_markdown_links_exist(self):
        """Crawl all wiki markdown files and ensure [link](target.md) links are valid."""
        broken_links = []
        
        for md_file in WIKI_DIR.rglob("*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Find standard markdown links [text](path.md)
            # Ignoring http/https links
            md_links = re.findall(r'\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)', content)
            
            for link in md_links:
                if link.startswith("http"):
                    continue
                # Resolve relative path
                target_path = WIKI_DIR / link
                if not target_path.exists():
                    broken_links.append(f"{md_file.name} -> {link}")
                    
        self.assertEqual(len(broken_links), 0, f"Wiki files contain broken markdown links: {broken_links}")

if __name__ == "__main__":
    unittest.main()
