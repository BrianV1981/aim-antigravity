"""
A.I.M. Proxy DataJack
Hooks Antigravity's outbound API traffic natively.
Run via: mitmdump -s aim-proxy.py -p 8080
"""
import json
import os
import time
from mitmproxy import http

# Determine root A.I.M tmp directory
AIM_TMP_DIR = os.path.expanduser(r"~/.gemini/tmp")
os.makedirs(AIM_TMP_DIR, exist_ok=True)

class AIMProxyDataJack:
    def __init__(self):
        self.session_started = time.strftime("%Y%m%dT%H%M%S")
        self.log_file = os.path.join(AIM_TMP_DIR, f"aim_session_{self.session_started}.json")
        self.conversation_skeleton = []
        print(f"[*] A.I.M Proxy active. Routing logs silently to: {self.log_file}")

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Intercepts requests from Antigravity to the host LLM API
        (Gemini/Claude) and rips the human/agent conversational array natively.
        """
        if "generativelanguage.googleapis.com" in flow.request.pretty_host or "api.anthropic.com" in flow.request.pretty_host:
            try:
                # Capture the raw plaintext payload
                body = flow.request.get_text()
                if body:
                    data = json.loads(body)
                    
                    # Extract Gemini format (A.I.M relies on 'contents' array structure)
                    if 'contents' in data:
                        for entry in data['contents']:
                            role = entry.get('role', 'user')
                            parts = entry.get('parts', [])
                            
                            # Join text elements, filtering out image/function boundaries for the Skeleton
                            text_content = ""
                            for p in parts:
                                if 'text' in p:
                                    text_content += p['text'] + "\n"
                            
                            if text_content.strip():
                                self.conversation_skeleton.append({
                                    "role": role.upper(),
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                    "text": text_content.strip()
                                })
                        
                        # Atomically flush the ripped conversation to the standard A.I.M directory
                        with open(self.log_file, "w", encoding="utf-8") as f:
                            json.dump(self.conversation_skeleton, f, indent=2)

            except Exception as e:
                # Silently catch JSON parse errors so we don't crash the proxy
                print(f"[A.I.M Proxy] DataJack Extraction Error: {e}")

addons = [
    AIMProxyDataJack()
]
