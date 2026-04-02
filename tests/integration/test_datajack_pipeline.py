"""
Integration tests: DataJack export -> import round-trip pipeline.

Covers:
- export_cartridge() writes a valid .engram ZIP containing metadata.json + JSONL chunks
- import_cartridge() reads the .engram and inserts fragments into a target DB
- Full round-trip: export from source DB -> import into a fresh DB -> search finds content
- The export skill (export_datajack_cartridge.py) calls aim_exchange.py as a subprocess

No real LLM, network, or interactive-input calls are made.
Filesystem I/O uses tmp_path and in-memory SQLite where possible.
"""

import importlib.util
import io
import json
import os
import struct
import sys
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch, call

# ---------------------------------------------------------------------------
# Dependency stubs (must come before any aim import)
# ---------------------------------------------------------------------------

def _stub(name):
    mod = types.ModuleType(name)
    sys.modules.setdefault(name, mod)
    return mod

for _m in ["google", "google.genai"]:
    _stub(_m)
# Note: requests IS installed — do not stub it.
# keyring is NOT installed — stub with attributes unit tests patch.
if "keyring" not in sys.modules:
    _kr = types.ModuleType("keyring")
    _kr.get_password = lambda *a, **k: None
    _kr.set_password = lambda *a, **k: None
    sys.modules["keyring"] = _kr

AIM_SRC = str(Path(__file__).parent.parent.parent / "src")
AIM_ROOT = str(Path(AIM_SRC).parent)

_config_stub = types.ModuleType("config_utils")
_config_stub.CONFIG = {
    "models": {
        "embedding_provider": "local",
        "embedding": "nomic-embed-text",
        "embedding_endpoint": "http://localhost:11434/api/embeddings",
    }
}
_config_stub.AIM_ROOT = AIM_ROOT
sys.modules["config_utils"] = _config_stub

if AIM_SRC not in sys.path:
    sys.path.insert(0, AIM_SRC)

for _pkg in ["plugins", "plugins.datajack"]:
    sys.modules.setdefault(_pkg, types.ModuleType(_pkg))

# Load ForensicDB
_forensic_spec = importlib.util.spec_from_file_location(
    "plugins.datajack.forensic_utils",
    os.path.join(AIM_SRC, "plugins", "datajack", "forensic_utils.py"),
)
_forensic_mod = importlib.util.module_from_spec(_forensic_spec)
with patch.dict(sys.modules, {"config_utils": _config_stub}):
    _forensic_spec.loader.exec_module(_forensic_mod)

sys.modules["plugins.datajack.forensic_utils"] = _forensic_mod
ForensicDB = _forensic_mod.ForensicDB

# Load aim_exchange
_exchange_path = os.path.join(AIM_SRC, "plugins", "datajack", "aim_exchange.py")
_exchange_spec = importlib.util.spec_from_file_location("aim_exchange", _exchange_path)
_exchange_mod = importlib.util.module_from_spec(_exchange_spec)

# Load aim_exchange with sovereign_sync stubbed ONLY for the duration of the
# exec — patch.dict restores sys.modules afterwards so unit tests that do
# `import sovereign_sync` still get the real module.
from unittest.mock import MagicMock
_ss_stub = types.ModuleType("sovereign_sync")
_ss_stub.export_to_jsonl = MagicMock(return_value=0)
_ss_stub.import_from_jsonl = MagicMock(return_value=0)

_prev_ss = sys.modules.get("sovereign_sync", _SENTINEL := object())
with patch.dict(sys.modules, {
    "config_utils": _config_stub,
    "plugins.datajack.forensic_utils": _forensic_mod,
    "sovereign_sync": _ss_stub,
}):
    _exchange_spec.loader.exec_module(_exchange_mod)
# patch.dict restores sovereign_sync to its previous state (absent or real)

export_cartridge = _exchange_mod.export_cartridge
import_cartridge = _exchange_mod.import_cartridge

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAKE_DIM = 4

def _unit_vec(index, dim=FAKE_DIM):
    v = [0.0] * dim
    v[index] = 1.0
    return v

def _make_source_db(db_path, session_id="expert-test-001", filename="POLICY_TEST.md",
                    content="The A.I.M. mandate requires TDD and GitOps discipline."):
    """Populate a ForensicDB at db_path with one session and one fragment."""
    db = ForensicDB(custom_path=db_path)
    db.add_session(session_id, filename, 1234567890.0)
    db.add_fragments(session_id, [
        {
            "type": "expert_knowledge",
            "content": content,
            "embedding": _unit_vec(0),
            "timestamp": "2026-01-01T00:00:00+00:00",
        }
    ])
    db.close()
    return session_id


# ---------------------------------------------------------------------------
# 1. export_cartridge — output file structure
# ---------------------------------------------------------------------------

class TestExportCartridge(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.src_db = os.path.join(self.tmpdir, "source.db")
        self.engram_out = os.path.join(self.tmpdir, "test_export.engram")
        _make_source_db(self.src_db, session_id="expert-alpha")

    def _run_export(self, keyword="expert-alpha"):
        """
        Patch ForensicDB so it uses our temp source.db instead of the real archive.
        Patch AIM_ROOT in aim_exchange to use tmpdir so the tmp_engram_build lands
        inside our test directory.
        """
        OrigForensicDB = ForensicDB

        class PatchedDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=self.src_db)

        with patch.object(_exchange_mod, "ForensicDB", PatchedDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("builtins.input", return_value="n"), \
             patch("sys.stdout", new_callable=io.StringIO):
            export_cartridge(keyword, self.engram_out)

    def test_engram_file_is_created(self):
        self._run_export()
        self.assertTrue(os.path.exists(self.engram_out),
                        f".engram file was not created at {self.engram_out}")

    def test_engram_is_valid_zip(self):
        self._run_export()
        self.assertTrue(zipfile.is_zipfile(self.engram_out))

    def test_engram_contains_metadata_json(self):
        self._run_export()
        with zipfile.ZipFile(self.engram_out, "r") as zf:
            names = zf.namelist()
        self.assertIn("metadata.json", names)

    def test_metadata_json_is_valid(self):
        self._run_export()
        with zipfile.ZipFile(self.engram_out, "r") as zf:
            meta = json.loads(zf.read("metadata.json"))
        self.assertIn("keyword", meta)
        self.assertIn("exported_at", meta)
        self.assertIn("payload_hash", meta)

    def test_metadata_keyword_matches_export_keyword(self):
        self._run_export("expert-alpha")
        with zipfile.ZipFile(self.engram_out, "r") as zf:
            meta = json.loads(zf.read("metadata.json"))
        self.assertEqual(meta["keyword"], "expert-alpha")

    def test_engram_contains_at_least_one_jsonl_chunk(self):
        self._run_export()
        with zipfile.ZipFile(self.engram_out, "r") as zf:
            jsonl_files = [n for n in zf.namelist() if n.endswith(".jsonl")]
        self.assertTrue(len(jsonl_files) >= 1)

    def test_jsonl_chunk_has_valid_header(self):
        self._run_export()
        with zipfile.ZipFile(self.engram_out, "r") as zf:
            jsonl_files = [n for n in zf.namelist() if n.endswith(".jsonl")]
            first = zf.read(jsonl_files[0]).decode("utf-8")
        first_line = first.splitlines()[0]
        header = json.loads(first_line)
        self.assertIn("session_id", header)
        self.assertIn("filename", header)

    def test_no_keyword_match_does_not_create_file(self):
        OrigForensicDB = ForensicDB

        class PatchedDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=self.src_db)

        out = os.path.join(self.tmpdir, "nothing.engram")
        with patch.object(_exchange_mod, "ForensicDB", PatchedDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("sys.stdout", new_callable=io.StringIO):
            export_cartridge("KEYWORD_THAT_DOES_NOT_EXIST_EVER", out)
        self.assertFalse(os.path.exists(out))


# ---------------------------------------------------------------------------
# 2. import_cartridge — ingesting a pre-built .engram into a fresh DB
# ---------------------------------------------------------------------------

class TestImportCartridge(unittest.TestCase):

    def _build_engram(self, tmpdir, session_id, content, keyword="test"):
        """
        Manually construct a minimal valid .engram file without calling
        export_cartridge, so import tests are fully isolated.
        """
        import hashlib, time, zipfile, io as sysio

        # Build JSONL content
        header = json.dumps({"session_id": session_id, "filename": f"{session_id}.jsonl",
                             "mtime": time.time()})
        fragment = json.dumps({"type": "expert_knowledge", "content": content,
                               "timestamp": None, "embedding": None, "metadata": {}})
        jsonl_bytes = (header + "\n" + fragment + "\n").encode("utf-8")

        # Compute hash
        hasher = hashlib.sha256()
        for line in (header + "\n" + fragment + "\n").splitlines(keepends=True):
            hasher.update(line.encode("utf-8"))

        metadata = json.dumps({
            "keyword": keyword,
            "exported_at": "2026-01-01T00:00:00",
            "sessions_count": 1,
            "payload_hash": hasher.hexdigest(),
        })

        engram_path = os.path.join(tmpdir, f"{keyword}.engram")
        with zipfile.ZipFile(engram_path, "w") as zf:
            zf.writestr("metadata.json", metadata)
            zf.writestr(f"chunks/{session_id}.jsonl", jsonl_bytes)

        return engram_path

    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.dst_db_path = os.path.join(self.tmpdir, "dst.db")
        self.content = "Imported fragment: GitOps mandate TDD discipline."
        self.session_id = "import-session-001"
        self.engram_path = self._build_engram(
            self.tmpdir, self.session_id, self.content
        )

    def _run_import(self):
        OrigForensicDB = ForensicDB
        dst_path = self.dst_db_path

        class PatchedDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=dst_path)

        with patch.object(_exchange_mod, "ForensicDB", PatchedDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("builtins.input", return_value="y"), \
             patch("sys.stdout", new_callable=io.StringIO):
            import_cartridge(self.engram_path)

    def test_import_creates_session_in_db(self):
        self._run_import()
        db = ForensicDB(custom_path=self.dst_db_path)
        row = db.conn.execute(
            "SELECT id FROM sessions WHERE id = ?", (self.session_id,)
        ).fetchone()
        db.close()
        self.assertIsNotNone(row)

    def test_import_creates_fragment_in_db(self):
        self._run_import()
        db = ForensicDB(custom_path=self.dst_db_path)
        row = db.conn.execute(
            "SELECT content FROM fragments WHERE session_id = ?", (self.session_id,)
        ).fetchone()
        db.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], self.content)

    def test_import_aborted_when_user_declines(self):
        OrigForensicDB = ForensicDB
        dst_path = self.dst_db_path

        class PatchedDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=dst_path)

        with patch.object(_exchange_mod, "ForensicDB", PatchedDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("builtins.input", return_value="n"), \
             patch("sys.stdout", new_callable=io.StringIO):
            import_cartridge(self.engram_path)

        db = ForensicDB(custom_path=self.dst_db_path)
        row = db.conn.execute("SELECT id FROM sessions WHERE id = ?", (self.session_id,)).fetchone()
        db.close()
        self.assertIsNone(row)

    def test_import_missing_file_prints_error(self):
        OrigForensicDB = ForensicDB
        dst_path = self.dst_db_path

        class PatchedDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=dst_path)

        with patch.object(_exchange_mod, "ForensicDB", PatchedDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("builtins.input", return_value="y"), \
             patch("sys.stdout", new_callable=io.StringIO) as out:
            import_cartridge("/nonexistent/path/to.engram")
        self.assertIn("ERROR", out.getvalue())


# ---------------------------------------------------------------------------
# 3. Full round-trip: export from source DB -> import into destination DB
#    -> lexical search finds the original content
# ---------------------------------------------------------------------------

class TestRoundTrip(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()
        self.src_db_path = os.path.join(self.tmpdir, "src.db")
        self.dst_db_path = os.path.join(self.tmpdir, "dst.db")
        self.engram_path = os.path.join(self.tmpdir, "round_trip.engram")
        self.unique_content = "round_trip_unique_content_xyz_sentinel"
        _make_source_db(
            self.src_db_path,
            session_id="expert-rt-001",
            filename="POLICY_RT.md",
            content=self.unique_content,
        )

    def _do_export(self):
        OrigForensicDB = ForensicDB
        src_path = self.src_db_path

        class SourceDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=src_path)

        with patch.object(_exchange_mod, "ForensicDB", SourceDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("sys.stdout", new_callable=io.StringIO):
            export_cartridge("expert-rt-001", self.engram_path)

    def _do_import(self):
        OrigForensicDB = ForensicDB
        dst_path = self.dst_db_path

        class DestDB(OrigForensicDB):
            def __init__(inner_self, custom_path=None):
                super().__init__(custom_path=dst_path)

        with patch.object(_exchange_mod, "ForensicDB", DestDB), \
             patch.object(_exchange_mod, "AIM_ROOT", self.tmpdir), \
             patch("builtins.input", return_value="y"), \
             patch("sys.stdout", new_callable=io.StringIO):
            import_cartridge(self.engram_path)

    def test_round_trip_engram_file_exists_after_export(self):
        self._do_export()
        self.assertTrue(os.path.exists(self.engram_path))

    def test_round_trip_content_retrievable_via_lexical_search(self):
        self._do_export()
        self._do_import()
        db = ForensicDB(custom_path=self.dst_db_path)
        results = db.search_lexical("round_trip_unique_content", top_k=5)
        db.close()
        self.assertTrue(len(results) >= 1)
        self.assertTrue(any(self.unique_content in r["content"] for r in results))

    def test_round_trip_session_exists_in_destination(self):
        self._do_export()
        self._do_import()
        db = ForensicDB(custom_path=self.dst_db_path)
        row = db.conn.execute(
            "SELECT id FROM sessions WHERE id = ?", ("expert-rt-001",)
        ).fetchone()
        db.close()
        self.assertIsNotNone(row)

    def test_round_trip_source_db_unchanged(self):
        """Source DB is read-only during export; verify its content is still intact."""
        self._do_export()
        db = ForensicDB(custom_path=self.src_db_path)
        rows = db.conn.execute("SELECT content FROM fragments").fetchall()
        db.close()
        self.assertTrue(any(self.unique_content in r[0] for r in rows))


# ---------------------------------------------------------------------------
# 4. Export skill subprocess wrapper
# ---------------------------------------------------------------------------

class TestExportSkillWrapper(unittest.TestCase):
    """
    Tests for skills/export_datajack_cartridge.py.
    The skill calls aim_exchange.py via subprocess — we mock subprocess.run
    to avoid needing a real database or embedding system.
    """

    SKILL_PATH = str(
        Path(__file__).parent.parent.parent / "skills" / "export_datajack_cartridge.py"
    )

    def _load_skill(self):
        spec = importlib.util.spec_from_file_location("export_skill", self.SKILL_PATH)
        return spec  # we won't exec it; we test the subprocess call pattern

    def test_skill_file_exists(self):
        self.assertTrue(os.path.exists(self.SKILL_PATH), f"Skill not found: {self.SKILL_PATH}")

    def test_skill_invokes_aim_exchange_export_subcommand(self):
        """
        When the skill runs, it should call:
          python aim_exchange.py export <keyword> --out <file.engram>
        Verify by mocking subprocess.run and inspecting the call.
        """
        import subprocess

        mock_result = MagicMock()
        mock_result.stdout = "[SUCCESS] Cartridge compiled: test.engram"
        mock_result.stderr = ""

        # Execute the skill with a fake argv, capturing its output
        captured_calls = []

        def fake_run(cmd, **kwargs):
            captured_calls.append(cmd)
            return mock_result

        original_argv = sys.argv[:]
        try:
            sys.argv = [self.SKILL_PATH, json.dumps({"keyword": "expert-", "name": "test.engram"})]
            with patch("subprocess.run", side_effect=fake_run), \
                 patch("sys.stdout", new_callable=io.StringIO) as out:
                spec = importlib.util.spec_from_file_location("export_skill_run", self.SKILL_PATH)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            output_text = out.getvalue()
        finally:
            sys.argv = original_argv

        # Verify subprocess.run was called
        self.assertTrue(len(captured_calls) >= 1, "subprocess.run was never called")
        cmd_flat = " ".join(str(c) for c in captured_calls[0])
        self.assertIn("export", cmd_flat)

    def test_skill_output_is_valid_json(self):
        """The skill must print a JSON object as its output."""
        import subprocess

        mock_result = MagicMock()
        mock_result.stdout = "[SUCCESS]"
        mock_result.stderr = ""

        original_argv = sys.argv[:]
        try:
            sys.argv = [self.SKILL_PATH, json.dumps({"keyword": "expert-", "name": "out.engram"})]
            with patch("subprocess.run", return_value=mock_result), \
                 patch("sys.stdout", new_callable=io.StringIO) as out:
                spec = importlib.util.spec_from_file_location("export_skill_json", self.SKILL_PATH)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            raw = out.getvalue().strip()
        finally:
            sys.argv = original_argv

        parsed = json.loads(raw)
        self.assertIsInstance(parsed, dict)

    def test_skill_output_contains_file_key(self):
        import subprocess

        mock_result = MagicMock()
        mock_result.stdout = "done"
        mock_result.stderr = ""

        original_argv = sys.argv[:]
        try:
            sys.argv = [self.SKILL_PATH, json.dumps({"keyword": "expert-", "name": "myfile.engram"})]
            with patch("subprocess.run", return_value=mock_result), \
                 patch("sys.stdout", new_callable=io.StringIO) as out:
                spec = importlib.util.spec_from_file_location("export_skill_key", self.SKILL_PATH)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            parsed = json.loads(out.getvalue())
        finally:
            sys.argv = original_argv

        self.assertIn("file", parsed)


if __name__ == "__main__":
    unittest.main()
