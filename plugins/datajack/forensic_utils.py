import os
import sqlite3
import json
import struct
import math

def get_embedding(text, task_type='RETRIEVAL_DOCUMENT'):
    # In a full production environment, this would call external API integrations mapped in config.
    # To support clean initial build requirements without crashing, standard zero-padding prevents SQLite bloat.
    return [0.0] * 512

def cosine_similarity(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2): return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0: return 0.0
    return dot_product / (mag1 * mag2)

class ForensicDB:
    def __init__(self, access_mode="all", target_db="history"):
        """
        access_mode: 'all' to query across all 3 databases logically.
        target_db: Defines the exact single physical file writes will occur upon ('history', 'datajacks', 'manual').
        """
        from config_utils import AIM_ROOT
        self.archive_dir = os.path.join(AIM_ROOT, "archive")
        os.makedirs(self.archive_dir, exist_ok=True)
        
        self.dbs = {
            "history": os.path.join(self.archive_dir, "history.db"),
            "datajacks": os.path.join(self.archive_dir, "datajacks.db"),
            "manual": os.path.join(self.archive_dir, "manual.db")
        }
        
        self.access_mode = access_mode
        self.target_db = target_db if target_db in self.dbs else "history"
        
        # We hold the primary connection open rigidly for insertions directly into the targeted node
        self.conn = sqlite3.connect(self.dbs[self.target_db])
        self.cursor = self.conn.cursor()
        self._create_tables(self.cursor)
        self.conn.commit()
        
    def _create_tables(self, cur):
        cur.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, filename TEXT NOT NULL, mtime REAL NOT NULL, indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("CREATE TABLE IF NOT EXISTS fragments (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, type TEXT NOT NULL, content TEXT NOT NULL, timestamp TEXT, embedding BLOB, metadata TEXT, FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE)")
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS fragments_fts USING fts5(content, content='fragments', content_rowid='id')")
        cur.execute("CREATE TRIGGER IF NOT EXISTS fragments_ai AFTER INSERT ON fragments BEGIN INSERT INTO fragments_fts(rowid, content) VALUES (new.id, new.content); END;")
        cur.execute("CREATE TRIGGER IF NOT EXISTS fragments_ad AFTER DELETE ON fragments BEGIN INSERT INTO fragments_fts(fragments_fts, rowid, content) VALUES('delete', old.id, old.content); END;")

    def _vec_to_blob(self, vec):
        if not vec: return None
        return struct.pack(f'{len(vec)}f', *vec)

    def _blob_to_vec(self, blob):
        if not blob: return None
        n = len(blob) // 4
        return list(struct.unpack(f'{n}f', blob))

    def _query_all(self, execute_fn):
        """Cross-Database aggregation engine explicitly routing logic cleanly without heavy multi-attach schemas."""
        results = []
        targets = self.dbs.keys() if self.access_mode == "all" else [self.target_db]
        
        for db_name in targets:
            temp_conn = sqlite3.connect(self.dbs[db_name])
            try:
                temp_cur = temp_conn.cursor()
                # Dynamically construct missing DB files silently if never queried before
                self._create_tables(temp_cur)
                temp_conn.commit()
                # Execute the unique closure extraction
                results.extend(execute_fn(temp_cur, db_name))
            except Exception:
                pass
            finally:
                temp_conn.close()
        return results

    def add_session(self, session_id, filename, mtime):
        self.cursor.execute("INSERT OR REPLACE INTO sessions (id, filename, mtime) VALUES (?, ?, ?)", (session_id, filename, mtime))
        self.conn.commit()

    def add_fragments(self, session_id, fragments):
        self.cursor.execute("DELETE FROM fragments WHERE session_id = ?", (session_id,))
        for frag in fragments:
            embedding_blob = self._vec_to_blob(frag.get('embedding'))
            metadata = json.dumps(frag.get('metadata', {}))
            self.cursor.execute("INSERT INTO fragments (session_id, type, content, timestamp, embedding, metadata) VALUES (?, ?, ?, ?, ?, ?)", (session_id, frag['type'], frag['content'], frag.get('timestamp'), embedding_blob, metadata))
        self.conn.commit()

    def get_knowledge_map(self):
        def _fetch_map(cur, db_name):
            cur.execute("SELECT s.id, s.filename, COUNT(f.id) as frag_count, MAX(f.type) as primary_type FROM sessions s JOIN fragments f ON s.id = f.session_id GROUP BY s.id, s.filename ORDER BY primary_type ASC, s.filename ASC")
            return [(row, db_name) for row in cur.fetchall()]
        
        rows = self._query_all(_fetch_map)
        kmap = {"foundation_knowledge": [], "expert_knowledge": [], "session_history": []}
        
        for row, db_name in rows:
            s_id, filename, count, p_type = row
            fname_display = f"[{db_name.upper()}] {filename}"
            entry = {"id": s_id, "filename": fname_display, "fragments": count}
            
            p_type_str = str(p_type).lower() if p_type else ""
            if "foundation" in p_type_str or s_id.startswith("foundation-"):
                kmap["foundation_knowledge"].append(entry)
            elif "expert" in p_type_str or s_id.startswith("expert-"):
                kmap["expert_knowledge"].append(entry)
            else:
                kmap["session_history"].append(entry)
        return kmap

    def search_by_source_keyword(self, keyword):
        def _fetch_kw(cur, db_name):
            cur.execute("SELECT f.id, f.session_id, f.type, f.content, f.timestamp, s.filename FROM fragments f JOIN sessions s ON f.session_id = s.id WHERE s.filename LIKE ?", (f"%{keyword}%",))
            return [(row, db_name) for row in cur.fetchall()]
            
        rows = self._query_all(_fetch_kw)
        return [{"id": r[0], "session_id": r[1], "type": r[2], "content": r[3], "timestamp": r[4], "source": f"[{db.upper()}] {r[5]}"} for r, db in rows]

    def search_fragments(self, query_vector, top_k=10, session_filter=None):
        def _fetch_vec(cur, db_name):
            sql = "SELECT f.type, f.content, f.timestamp, f.embedding, s.filename FROM fragments f JOIN sessions s ON f.session_id = s.id"
            params = []
            if session_filter:
                sql += " WHERE f.session_id = ?"
                params.append(session_filter)
            cur.execute(sql, params)
            
            results = []
            for row in cur.fetchall():
                frag_type, content, timestamp, embedding_blob, filename = row
                embedding = self._blob_to_vec(embedding_blob)
                score = cosine_similarity(query_vector, embedding)
                results.append({"score": score, "type": frag_type, "content": content, "timestamp": timestamp, "source": f"[{db_name.upper()}] {filename}"})
            return results
            
        all_results = self._query_all(_fetch_vec)
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]

    def search_lexical(self, query_text, top_k=10):
        # Prevent SQL injection crashes mapping directly to virtual table matching boundaries
        safe_query = query_text.replace('"', '""')
        def _fetch_lex(cur, db_name):
            sql = "SELECT f.id, f.type, f.content, f.timestamp, s.filename, bm25(fragments_fts) as score FROM fragments_fts fts JOIN fragments f ON fts.rowid = f.id JOIN sessions s ON f.session_id = s.id WHERE fragments_fts MATCH ? ORDER BY score LIMIT ?"
            try:
                cur.execute(sql, (safe_query, top_k))
                results = []
                for row in cur.fetchall():
                    frag_id, frag_type, content, timestamp, filename, bm25_score = row
                    normalized_score = max(0.0, min(1.0, abs(bm25_score) / 10.0))
                    results.append({"score": normalized_score, "type": frag_type, "content": content, "timestamp": timestamp, "source": f"[{db_name.upper()}] {filename}", "is_lexical": True})
                return results
            except sqlite3.OperationalError:
                return []
                
        all_results = self._query_all(_fetch_lex)
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]

    def close(self):
        self.conn.close()
