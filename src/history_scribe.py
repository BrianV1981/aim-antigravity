#!/usr/bin/env python3
import sys
import json
import os
import glob
import sqlite3
from datetime import datetime

# --- DYNAMIC ROOT DISCOVERY ---
def find_aim_root():
    """Dynamically discovers the A.I.M. root directory."""
    current = os.path.abspath(os.getcwd())
    while current != '/':
        if os.path.exists(os.path.join(current, "core", "CONFIG.json")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AIM_ROOT = find_aim_root()
sys.path.append(os.path.join(AIM_ROOT, "src"))
sys.path.append(os.path.join(AIM_ROOT, "scripts"))

try:
    from extract_signal import extract_signal, skeleton_to_markdown
except ImportError:
    extract_signal = None
    skeleton_to_markdown = None

HISTORY_DB = os.path.join(AIM_ROOT, "archive/history.db")
HISTORY_DIR = os.path.join(AIM_ROOT, "archive/history")
RAW_DIR = os.path.join(AIM_ROOT, "archive/raw")

class HistoryDB:
    def __init__(self):
        os.makedirs(os.path.dirname(HISTORY_DB), exist_ok=True)
        self.conn = sqlite3.connect(HISTORY_DB)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                session_id TEXT PRIMARY KEY,
                timestamp TEXT,
                content TEXT
            )
        """)
        # FTS5 for session search
        self.cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS history_fts USING fts5(session_id UNINDEXED, timestamp UNINDEXED, content)")
        self.conn.commit()

    def add_session(self, session_id, timestamp, content):
        self.cursor.execute("INSERT OR REPLACE INTO history (session_id, timestamp, content) VALUES (?, ?, ?)", 
                           (session_id, timestamp, content))
        self.cursor.execute("INSERT OR REPLACE INTO history_fts (session_id, timestamp, content) VALUES (?, ?, ?)",
                           (session_id, timestamp, content))
        self.conn.commit()

def save_split_markdown(session_id, md_content, base_path, line_limit=2000):
    """Splits a large markdown file into 2000-line chunks."""
    lines = md_content.splitlines()
    if len(lines) <= line_limit:
        with open(base_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return [base_path]

    chunks = []
    for i in range(0, len(lines), line_limit):
        part_num = (i // line_limit) + 1
        chunk_content = "\n".join(lines[i:i + line_limit])
        chunk_path = base_path.replace(".md", f"_part{part_num}.md")
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk_content)
        chunks.append(chunk_path)
    return chunks

def scribe_all_sessions():
    db = HistoryDB()
    os.makedirs(HISTORY_DIR, exist_ok=True)
    
    # 1. Antigravity IDE native text transcripts
    ide_logs = glob.glob(os.path.expanduser("~/.gemini/antigravity/brain/*/.system_generated/logs/overview.txt"))
    # 2. Legacy terminal JSON logs (if ported via Datajack)
    legacy_logs = glob.glob(os.path.join(RAW_DIR, "*.json"))

    print(f"--- History Scribe: Processing {len(ide_logs)} Antigravity sessions & {len(legacy_logs)} Legacy JSONs ---")
    
    processed_count = 0
    # Process Antigravity native overview texts directly
    for txt_path in ide_logs:
        try:
            # Extract session UUID from path: ~/.gemini/antigravity/brain/<id>/.system_generated/logs/overview.txt
            session_id = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(txt_path))))
            md_base_path = os.path.join(HISTORY_DIR, f"{session_id}.md")
            
            if os.path.exists(md_base_path) or os.path.exists(md_base_path.replace(".md", "_part1.md")):
                continue

            with open(txt_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            save_split_markdown(session_id, md_content, md_base_path)
            
            # Index timestamp using file modified time
            mtime = os.path.getmtime(txt_path)
            ts = datetime.fromtimestamp(mtime).isoformat()
            db.add_session(session_id, ts, md_content)
            processed_count += 1
        except Exception as e:
            print(f"Error parsing Antigravity log {txt_path}: {e}")

    # Process Legacy JSONs via extract_signal if available
    for t_path in legacy_logs:
        try:
            with open(t_path, 'r') as f: data = json.load(f)
            session_id = data.get('sessionId') or data.get('session_id')
            if not session_id: continue
            md_base_path = os.path.join(HISTORY_DIR, f"{session_id}.md")
            if os.path.exists(md_base_path) or os.path.exists(md_base_path.replace(".md", "_part1.md")):
                continue
            if extract_signal and skeleton_to_markdown:
                skeleton = extract_signal(t_path)
                if not skeleton: continue
                md_content = skeleton_to_markdown(skeleton, session_id)
                save_split_markdown(session_id, md_content, md_base_path)
                ts = data.get('startTime') or datetime.now().isoformat()
                db.add_session(session_id, ts, md_content)
                processed_count += 1
        except Exception:
            pass
            
    print(f"[SUCCESS] Scribed {processed_count} historical sessions (Split into 2000-line chunks).")

if __name__ == "__main__":
    scribe_all_sessions()
