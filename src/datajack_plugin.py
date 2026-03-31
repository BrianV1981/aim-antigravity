import sys
import os

class NullKnowledgeProvider:
    """A fallback provider that fails gracefully if the actual Engram DB is broken."""
    def __init__(self, error_msg="DataJack plugin is offline."):
        self.error_msg = error_msg
        
    def get_knowledge_map(self):
        return {"error": self.error_msg, "foundation_knowledge": [], "expert_knowledge": [], "session_history": []}
        
    def search_fragments(self, query, top_k=5, **kwargs):
        return []
        
    def search_lexical(self, query, top_k=5):
        return []

    def search_by_source_keyword(self, keyword):
        return []
        
    def close(self):
        pass

def load_knowledge_provider(mode="all", target_db="history"):
    """
    The SafeLoad Factory. Attempts to load the heavy SQLite/Embedding DB.
    Returns a NullProvider if dependencies or connections fail dynamically.
    """
    try:
        from plugins.datajack.forensic_utils import ForensicDB
        return ForensicDB(access_mode=mode, target_db=target_db)
    except Exception as e:
        sys.stderr.write(f"\n[A.I.M. SAFE-LOAD] DataJack Engram system offline: {e}\n")
        return NullKnowledgeProvider(str(e))
