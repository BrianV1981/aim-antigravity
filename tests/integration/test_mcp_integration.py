"""
Integration tests: MCP server tool registration and dispatch.

Covers:
- mcp_server.py can be imported as a module (FastMCP stubbed)
- search_engram and run_skill tools are defined on the loaded module
- search_engram() returns formatted results when perform_search is mocked
- run_skill() with a non-existent skill returns proper error JSON
- run_skill() with a real skill name (advanced_memory_search.py) attempts _sandboxed_run
- _build_sandbox_command produces a bwrap invocation for .py and .sh skills
- _sandboxed_run handles bwrap absence and timeout gracefully

No real LLM, network, or subprocess calls are made.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Stub FastMCP and heavy deps before loading the module
# ---------------------------------------------------------------------------

def _make_fake_fastmcp():
    instance = MagicMock()
    # Decorators must return the original function unchanged
    instance.tool.return_value = lambda f: f
    instance.resource.return_value = lambda f: f
    instance.run = MagicMock()
    return instance

_fake_mcp_instance = _make_fake_fastmcp()
_fake_mcp_class = MagicMock(return_value=_fake_mcp_instance)

_fastmcp_mod = types.ModuleType("fastmcp")
_fastmcp_mod.FastMCP = _fake_mcp_class
sys.modules["fastmcp"] = _fastmcp_mod

# Stub heavy deps
for _m in ["keyring", "requests", "google", "google.genai"]:
    sys.modules.setdefault(_m, types.ModuleType(_m))

AIM_SRC = str(Path(__file__).parent.parent.parent / "src")
AIM_ROOT = str(Path(AIM_SRC).parent)

_config_stub = types.ModuleType("config_utils")
_config_stub.CONFIG = {}
_config_stub.AIM_ROOT = AIM_ROOT
sys.modules["config_utils"] = _config_stub

if AIM_SRC not in sys.path:
    sys.path.insert(0, AIM_SRC)

# ---------------------------------------------------------------------------
# Load mcp_server once at module level (shared across all test classes)
# ---------------------------------------------------------------------------

MCP_SERVER_PATH = os.path.join(AIM_SRC, "mcp_server.py")


def _load_mcp_server():
    spec = importlib.util.spec_from_file_location("mcp_server_integ", MCP_SERVER_PATH)
    mod = importlib.util.module_from_spec(spec)
    retriever_stub = types.ModuleType("retriever")
    retriever_stub.perform_search = MagicMock(return_value=[])
    with patch.dict(sys.modules, {"retriever": retriever_stub,
                                   "config_utils": _config_stub}):
        spec.loader.exec_module(mod)
    return mod


mcp = _load_mcp_server()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_skill_dir(skill_names=None):
    """Return (tmpdir, Path) with optional .py skill files pre-created."""
    tmpdir = tempfile.mkdtemp()
    skills_path = Path(tmpdir)
    for name in (skill_names or []):
        (skills_path / f"{name}.py").write_text(f"# {name} stub\nprint('hello')\n")
    return tmpdir, skills_path


# ---------------------------------------------------------------------------
# 1. Module import and tool registration
# ---------------------------------------------------------------------------

class TestMCPModuleImport(unittest.TestCase):

    def test_module_loaded_without_error(self):
        self.assertIsNotNone(mcp)

    def test_search_engram_is_callable(self):
        self.assertTrue(callable(getattr(mcp, "search_engram", None)),
                        "search_engram is not defined or not callable on mcp_server")

    def test_run_skill_is_callable(self):
        self.assertTrue(callable(getattr(mcp, "run_skill", None)),
                        "run_skill is not defined or not callable on mcp_server")

    def test_get_project_context_is_defined(self):
        self.assertTrue(callable(getattr(mcp, "get_project_context", None)),
                        "get_project_context is not defined on mcp_server")

    def test_skills_dir_attribute_exists(self):
        self.assertTrue(hasattr(mcp, "SKILLS_DIR"),
                        "SKILLS_DIR constant missing from mcp_server")

    def test_archive_dir_attribute_exists(self):
        self.assertTrue(hasattr(mcp, "ARCHIVE_DIR"),
                        "ARCHIVE_DIR constant missing from mcp_server")

    def test_mcp_object_is_created(self):
        # FastMCP was instantiated with a name during module load
        _fake_mcp_class.assert_called()


# ---------------------------------------------------------------------------
# 2. search_engram() — direct call with mocked perform_search
# ---------------------------------------------------------------------------

class TestSearchEngramIntegration(unittest.TestCase):

    def _search(self, query, results=None):
        mock_results = results if results is not None else []
        with patch.object(mcp, "perform_search", return_value=mock_results):
            return mcp.search_engram(query)

    def test_returns_string(self):
        result = self._search("test query")
        self.assertIsInstance(result, str)

    def test_empty_results_returns_no_fragments_message(self):
        result = self._search("zero results query", results=[])
        self.assertIn("No fragments found", result)
        self.assertIn("zero results query", result)

    def test_single_result_formatted_correctly(self):
        result = self._search("hybrid rag", results=[
            {"session_file": "POLICY_HANDBOOK.md", "content": "Hybrid RAG pipeline.", "score": 0.9321}
        ])
        self.assertIn("Hybrid RAG pipeline.", result)
        self.assertIn("POLICY_HANDBOOK.md", result)
        self.assertIn("0.9321", result)

    def test_multiple_results_all_appear_in_output(self):
        results = [
            {"session_file": "a.md", "content": "Content A", "score": 0.9},
            {"session_file": "b.md", "content": "Content B", "score": 0.7},
            {"session_file": "c.md", "content": "Content C", "score": 0.5},
        ]
        output = self._search("multi", results=results)
        for r in results:
            self.assertIn(r["content"], output)

    def test_output_includes_result_header(self):
        result = self._search("header check", results=[
            {"session_file": "f.md", "content": "text", "score": 0.5}
        ])
        self.assertIn("---", result)

    def test_perform_search_called_with_top_k_5(self):
        with patch.object(mcp, "perform_search", return_value=[]) as mock_ps:
            mcp.search_engram("k test")
        mock_ps.assert_called_once_with("k test", top_k=5)

    def test_returns_error_when_perform_search_is_none(self):
        original = mcp.perform_search
        mcp.perform_search = None
        try:
            result = mcp.search_engram("anything")
        finally:
            mcp.perform_search = original
        self.assertIn("Error", result)

    def test_returns_retrieval_error_on_exception(self):
        with patch.object(mcp, "perform_search", side_effect=RuntimeError("DB locked")):
            result = mcp.search_engram("broken")
        self.assertIn("Retrieval Error", result)
        self.assertIn("DB locked", result)


# ---------------------------------------------------------------------------
# 3. run_skill() — non-existent skill
# ---------------------------------------------------------------------------

class TestRunSkillNotFound(unittest.TestCase):

    def setUp(self):
        self.tmpdir, self.skills_path = _make_skill_dir()
        self._original_skills_dir = mcp.SKILLS_DIR
        mcp.SKILLS_DIR = self.skills_path

    def tearDown(self):
        mcp.SKILLS_DIR = self._original_skills_dir

    def test_returns_json_error_for_missing_skill(self):
        result = mcp.run_skill("does_not_exist")
        data = json.loads(result)
        self.assertIn("error", data)

    def test_error_message_contains_skill_name(self):
        result = mcp.run_skill("phantom_skill_xyz")
        data = json.loads(result)
        self.assertIn("phantom_skill_xyz", data["error"])

    def test_error_message_contains_not_found(self):
        result = mcp.run_skill("ghost_skill")
        data = json.loads(result)
        self.assertIn("not found", data["error"])

    def test_invalid_args_json_returns_error(self):
        # Create a real skill so the skill lookup succeeds
        (self.skills_path / "real_skill.py").write_text("print('hi')")
        result = mcp.run_skill("real_skill", args_json="not_valid_json{{{")
        data = json.loads(result)
        self.assertIn("error", data)


# ---------------------------------------------------------------------------
# 4. run_skill() — real skill name (advanced_memory_search.py)
# ---------------------------------------------------------------------------

class TestRunSkillRealSkill(unittest.TestCase):

    def setUp(self):
        self._original_skills_dir = mcp.SKILLS_DIR
        # Point SKILLS_DIR at the real skills directory
        mcp.SKILLS_DIR = Path(AIM_ROOT) / "skills"

    def tearDown(self):
        mcp.SKILLS_DIR = self._original_skills_dir

    def test_advanced_memory_search_skill_file_exists(self):
        skill_path = mcp.SKILLS_DIR / "advanced_memory_search.py"
        self.assertTrue(skill_path.exists(),
                        f"Expected skill at {skill_path}")

    def test_run_skill_attempts_sandboxed_run_for_existing_skill(self):
        """run_skill() should reach _sandboxed_run when the skill file exists."""
        with patch.object(mcp, "_sandboxed_run", return_value='{"status": "ok"}') as mock_run:
            result = mcp.run_skill("advanced_memory_search", args_json="{}")
        mock_run.assert_called_once()
        skill_arg = mock_run.call_args[0][0]
        self.assertEqual(skill_arg.name, "advanced_memory_search.py")

    def test_run_skill_passes_empty_dict_for_empty_args(self):
        with patch.object(mcp, "_sandboxed_run", return_value="ok") as mock_run:
            mcp.run_skill("advanced_memory_search", args_json="{}")
        _, args_dict = mock_run.call_args[0]
        self.assertEqual(args_dict, {})

    def test_run_skill_passes_parsed_args_dict(self):
        with patch.object(mcp, "_sandboxed_run", return_value="ok") as mock_run:
            mcp.run_skill("advanced_memory_search", args_json='{"query": "test query"}')
        _, args_dict = mock_run.call_args[0]
        self.assertEqual(args_dict, {"query": "test query"})

    def test_run_skill_returns_sandboxed_run_output(self):
        with patch.object(mcp, "_sandboxed_run", return_value='{"results": []}'):
            result = mcp.run_skill("advanced_memory_search")
        self.assertEqual(result, '{"results": []}')


# ---------------------------------------------------------------------------
# 5. _build_sandbox_command (Native Execution)
# ---------------------------------------------------------------------------

class TestBuildSandboxCommand(unittest.TestCase):

    def test_python_skill_uses_sys_executable(self):
        cmd = mcp._build_sandbox_command(Path("/tmp/skill.py"), {})
        self.assertIn(sys.executable, cmd)

    def test_shell_skill_uses_bash(self):
        cmd = mcp._build_sandbox_command(Path("/tmp/skill.sh"), {})
        self.assertIn("bash", cmd)

    def test_args_dict_serialised_to_json_string(self):
        cmd = mcp._build_sandbox_command(Path("/tmp/skill.py"), {"key": "val"})
        self.assertIn('{"key": "val"}', cmd)

    def test_no_json_arg_when_args_dict_empty(self):
        cmd_with = mcp._build_sandbox_command(Path("/tmp/skill.py"), {"k": "v"})
        cmd_without = mcp._build_sandbox_command(Path("/tmp/skill.py"), {})
        self.assertGreater(len(cmd_with), len(cmd_without))

    def test_skill_path_appears_in_command(self):
        skill = Path("/tmp/unique_skill_path.py")
        cmd = mcp._build_sandbox_command(skill, {})
        self.assertIn(str(skill), cmd)


# ---------------------------------------------------------------------------
# 6. _sandboxed_run (Native wrapper now)
# ---------------------------------------------------------------------------

class TestSandboxedRunIntegration(unittest.TestCase):

    def test_returns_stdout_on_success(self):
        mock_proc = MagicMock()
        mock_proc.stdout = '{"result": "success"}'
        mock_proc.stderr = ""
        with patch("subprocess.run", return_value=mock_proc):
            result = mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        self.assertEqual(result, '{"result": "success"}')

    def test_falls_back_to_stderr_when_stdout_empty(self):
        mock_proc = MagicMock()
        mock_proc.stdout = ""
        mock_proc.stderr = "stderr warning"
        with patch("subprocess.run", return_value=mock_proc):
            result = mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        self.assertEqual(result, "stderr warning")

    def test_returns_completed_message_when_both_outputs_empty(self):
        mock_proc = MagicMock()
        mock_proc.stdout = ""
        mock_proc.stderr = ""
        with patch("subprocess.run", return_value=mock_proc):
            result = mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        self.assertIn("completed", result)

    def test_returns_error_json_on_timeout(self):
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("script", 65)):
            result = mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        data = json.loads(result)
        self.assertIn("error", data)
        self.assertIn("timed out", data["error"])

    def test_returns_error_json_on_os_error(self):
        with patch("subprocess.run", side_effect=OSError("permission denied")):
            result = mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        data = json.loads(result)
        self.assertIn("error", data)

    def test_subprocess_run_called_with_native_cmd(self):
        mock_proc = MagicMock()
        mock_proc.stdout = "done"
        mock_proc.stderr = ""
        with patch("subprocess.run", return_value=mock_proc) as mock_run:
            mcp._sandboxed_run(Path("/tmp/skill.py"), {})
        call_args = mock_run.call_args[0][0]
        self.assertIn(sys.executable, call_args)


# ---------------------------------------------------------------------------
# 7. get_project_context resource
# ---------------------------------------------------------------------------

class TestGetProjectContext(unittest.TestCase):

    def test_returns_claude_md_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            claude_md = os.path.join(tmpdir, "CLAUDE.md")
            Path(claude_md).write_text("# Test AIM mandate")
            # Patch AIM_ROOT to point at our tempdir
            with patch.object(mcp, "AIM_ROOT", tmpdir):
                # get_project_context is a plain function on the module
                result = mcp.get_project_context()
        self.assertIn("Test AIM mandate", result)

    def test_returns_fallback_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(mcp, "AIM_ROOT", tmpdir):
                result = mcp.get_project_context()
        self.assertIn("not found", result)


if __name__ == "__main__":
    unittest.main()
