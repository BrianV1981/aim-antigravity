import sys
import os

class NullKnowledgeProvider:
    """A fallback provider that fails gracefully if the actual Engram DB is broken."""
    def __init__(self, error_msg="DataJack plugin is offline."):
        self.error_msg = error_msg
        
    def get_knowledge_map(self):
        return {"error": self.error_msg}
        
    def semantic_search(self, query, top_k=5):
        return [{"content": f"[SYSTEM OFFLINE] {self.error_msg}", "score": 0.0, "type": "error"}]
        
    def lexical_search(self, query, top_k=5):
        return []
        
    def close(self):
        pass

def load_knowledge_provider():
    """The SafeLoad Factory. Attempts to load the heavy SQLite/Embedding DB.
    Returns a NullProvider if dependencies (like keyring or sqlite-vec) are missing."""
    try:
        from plugins.datajack.forensic_utils import ForensicDB
        return ForensicDB()
    except Exception as e:
        sys.stderr.write(f"\n[A.I.M. SAFE-LOAD] DataJack Engram system offline: {e}\n")
        return NullKnowledgeProvider(str(e))
