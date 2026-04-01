import re
import os

pb_path = r'C:\Users\kingb\.gemini\antigravity\conversations\45ccd4d9-07a4-4ca8-a328-d34d320cb414.pb'
try:
    with open(pb_path, 'rb') as f:
        data = f.read().decode('utf-8', 'ignore')
        
    # Rip continuous text blocks that are 50 characters or longer
    # Focusing on dialogue, punctuation, and markdown syntax
    matches = re.findall(r'[A-Za-z0-9 \-_.,?!\"\'\*#:\(\)>{}\[\]\n\r\/|`\\]{30,}', data)
    
    clean_blocks = []
    for m in matches:
        if len(m.strip()) > 30 and not "CORTEX_STEP_TYPE" in m:
            clean_blocks.append(m.strip())
            
    print("\n\n=== RIP SUCCESS ===\n\n".join(clean_blocks[-10:]))
except Exception as e:
    print(f"Failed to RIP: {e}")
