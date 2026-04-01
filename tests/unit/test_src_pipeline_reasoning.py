"""
Comprehensive unit tests for A.I.M. memory pipeline modules and the reasoning engine.

Modules under test:
  - src/daily_refiner.py       (Tier 3 Daily Refiner)
  - src/weekly_consolidator.py (Tier 4 Weekly Consolidator)
  - src/memory_proposer.py     (Tier 2 Memory Proposer)
  - src/reasoning_utils.py     (Multi-provider AI Router)

All network calls, subprocess calls, and keyring access are fully mocked.
"""

# ---------------------------------------------------------------------------
# Bootstrap: stub heavy optional deps before any src import
# ---------------------------------------------------------------------------
import sys
import os
import types
import json
import tempfile
import unittest
import importlib
import importlib.util
from unittest.mock import MagicMock, patch, call


def _build_requests_stub():
    """Build a stub 'requests' module with the attributes reasoning_utils needs."""
    mod = types.ModuleType('requests')
    mod.post = MagicMock()
    mod.get = MagicMock()
    exc_sub = types.ModuleType('requests.exceptions')

    class _HTTPError(Exception):
        def __init__(self, *args, response=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.response = response

    exc_sub.HTTPError = _HTTPError
    mod.exceptions = exc_sub
    return mod


def _build_keyring_stub():
    mod = types.ModuleType('keyring')
    mod.get_password = MagicMock(return_value=None)
    return mod


# Only install stubs if the real packages are not present
if 'requests' not in sys.modules:
    sys.modules['requests'] = _build_requests_stub()
if 'requests.exceptions' not in sys.modules:
    req_mod = sys.modules['requests']
    if not hasattr(req_mod, 'exceptions'):
        # requests was installed as a bare stub — attach our exceptions submodule
        req_mod = _build_requests_stub()
        sys.modules['requests'] = req_mod
    sys.modules['requests.exceptions'] = req_mod.exceptions

if 'keyring' not in sys.modules:
    sys.modules['keyring'] = _build_keyring_stub()

for _mod_name in ['google', 'google.genai']:
    if _mod_name not in sys.modules:
        sys.modules[_mod_name] = types.ModuleType(_mod_name)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
MINIMAL_CONFIG = {
    "memory_pipeline": {
        "intervals": {"tier2": 12, "tier3": 24, "tier4": 72},
        "cleanup_mode": "archive"
    },
    "models": {
        "reasoning_provider": "anthropic",
        "reasoning_model": "claude-3-haiku",
        "tiers": {
            "tier1": {"provider": "local", "model": "qwen", "endpoint": "http://localhost:11434/api/generate", "auth_type": "api_key"},
            "tier2": {"provider": "google", "model": "gemini-2.5-flash", "endpoint": "", "auth_type": "OAuth (System Default / CLI)"},
            "tier3": {"provider": "google", "model": "gemini-2.5-flash", "endpoint": "", "auth_type": "OAuth (System Default / CLI)"},
            "tier4": {"provider": "google", "model": "gemini-2.5-flash-lite", "endpoint": "", "auth_type": "OAuth"},
            "ollama_tier": {"provider": "ollama", "model": "llama3", "endpoint": "http://localhost:11434/api/generate", "auth_type": ""},
            "openai_tier": {"provider": "openai-compat", "model": "gpt-4o-mini", "endpoint": "http://localhost:1234/v1/chat/completions", "auth_type": ""},
            "anthropic_tier": {"provider": "anthropic", "model": "claude-3-haiku", "endpoint": "", "auth_type": "API Key"},
            "openrouter_tier": {"provider": "openrouter", "model": "meta-llama/llama-3-8b-instruct", "endpoint": "", "auth_type": ""},
            "codex_tier": {"provider": "codex-cli", "model": "o3", "endpoint": "", "auth_type": ""},
        }
    }
}


def _make_fake_aim_root(tmp_dir, config=None):
    """Build a minimal aim-root directory tree inside tmp_dir."""
    core_dir = os.path.join(tmp_dir, 'core')
    os.makedirs(core_dir, exist_ok=True)
    cfg = config if config is not None else MINIMAL_CONFIG
    with open(os.path.join(core_dir, 'CONFIG.json'), 'w') as f:
        json.dump(cfg, f)
    with open(os.path.join(core_dir, 'MEMORY.md'), 'w') as f:
        f.write("# Current Memory\nSome existing facts.\n")
    os.makedirs(os.path.join(tmp_dir, 'memory', 'proposals'), exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, 'memory', 'hourly'), exist_ok=True)
    return tmp_dir


def _load_pipeline_module(module_filename, fake_root):
    """
    Load a pipeline src module using importlib, patching os.getcwd so that
    the module's top-level find_aim_root() resolves to fake_root.
    """
    src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', module_filename)
    module_name = module_filename.replace('.py', '') + '_isolated'
    spec = importlib.util.spec_from_file_location(module_name, src_path)
    mod = importlib.util.module_from_spec(spec)
    with patch('os.getcwd', return_value=fake_root):
        spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# reasoning_utils — force-load the real module regardless of any stub that
# prior test files (e.g. hook tests) may have installed in sys.modules.
# ---------------------------------------------------------------------------
sys.modules.pop('reasoning_utils', None)
import reasoning_utils as ru

# Convenience aliases for patching at the module where the name is bound
_RU_REQUESTS_POST = 'reasoning_utils.requests.post'
_RU_KEYRING_GP    = 'reasoning_utils.keyring.get_password'
_RU_SUBPROCESS    = 'reasoning_utils.subprocess.run'


# ===========================================================================
# TestLoadConfig
# ===========================================================================
class TestLoadConfig(unittest.TestCase):
    """reasoning_utils.load_config()"""

    def test_returns_empty_dict_when_no_file(self):
        with patch.object(ru, 'CONFIG_PATH', '/nonexistent/path/CONFIG.json'):
            result = ru.load_config()
        self.assertEqual(result, {})

    def test_returns_empty_dict_on_bad_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("not valid json{{")
            tmp = f.name
        try:
            with patch.object(ru, 'CONFIG_PATH', tmp):
                result = ru.load_config()
            self.assertEqual(result, {})
        finally:
            os.unlink(tmp)

    def test_returns_parsed_config(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"key": "value"}, f)
            tmp = f.name
        try:
            with patch.object(ru, 'CONFIG_PATH', tmp):
                result = ru.load_config()
            self.assertEqual(result['key'], 'value')
        finally:
            os.unlink(tmp)


# ===========================================================================
# TestExecuteOllama
# ===========================================================================
class TestExecuteOllama(unittest.TestCase):
    """reasoning_utils.execute_ollama()"""

    def _mock_resp(self, status_code, body):
        m = MagicMock()
        m.status_code = status_code
        m.json.return_value = body
        m.text = str(body)
        return m

    def test_returns_response_on_200(self):
        mock_resp = self._mock_resp(200, {'response': 'Hello from Ollama'})
        with patch(_RU_REQUESTS_POST, return_value=mock_resp) as mock_post:
            result = ru.execute_ollama('my prompt', 'sys', 'llama3', 'http://localhost:11434/api/generate')
        self.assertEqual(result, 'Hello from Ollama')
        mock_post.assert_called_once()

    def test_uses_default_endpoint_when_none_given(self):
        mock_resp = self._mock_resp(200, {'response': 'ok'})
        with patch(_RU_REQUESTS_POST, return_value=mock_resp) as mock_post:
            ru.execute_ollama('p', 's', 'm', None)
        args, _ = mock_post.call_args
        self.assertIn('11434', args[0])

    def test_returns_error_on_non_200(self):
        mock_resp = self._mock_resp(503, {'error': 'service unavailable'})
        with patch(_RU_REQUESTS_POST, return_value=mock_resp):
            result = ru.execute_ollama('p', 's', 'm', 'http://localhost:11434/api/generate')
        self.assertIn('Ollama Error', result)
        self.assertIn('503', result)

    def test_returns_error_on_exception(self):
        with patch(_RU_REQUESTS_POST, side_effect=ConnectionError("refused")):
            result = ru.execute_ollama('p', 's', 'm', 'http://localhost:11434/api/generate')
        self.assertIn('Ollama Error', result)


# ===========================================================================
# TestExecuteAnthropic
# ===========================================================================
class TestExecuteAnthropic(unittest.TestCase):
    """reasoning_utils.execute_anthropic()"""

    def _mock_resp(self, status_code, body):
        m = MagicMock()
        m.status_code = status_code
        m.json.return_value = body
        m.text = str(body)
        return m

    def test_returns_text_on_success(self):
        body = {'content': [{'text': 'Anthropic says hello'}]}
        mock_resp = self._mock_resp(200, body)
        with patch(_RU_KEYRING_GP, return_value='test-key'), \
             patch(_RU_REQUESTS_POST, return_value=mock_resp):
            result = ru.execute_anthropic('user prompt', 'sys', 'claude-3-haiku')
        self.assertEqual(result, 'Anthropic says hello')

    def test_returns_error_when_no_api_key(self):
        with patch(_RU_KEYRING_GP, return_value=None):
            result = ru.execute_anthropic('p', 's', 'm')
        self.assertIn('Error', result)
        self.assertIn('Anthropic', result)

    def test_returns_error_on_non_200(self):
        body = {'error': {'message': 'unauthorized'}}
        mock_resp = self._mock_resp(401, body)
        with patch(_RU_KEYRING_GP, return_value='test-key'), \
             patch(_RU_REQUESTS_POST, return_value=mock_resp):
            result = ru.execute_anthropic('p', 's', 'm')
        self.assertIn('Anthropic Error', result)
        self.assertIn('401', result)

    def test_returns_error_on_exception(self):
        with patch(_RU_KEYRING_GP, return_value='test-key'), \
             patch(_RU_REQUESTS_POST, side_effect=Exception("network fail")):
            result = ru.execute_anthropic('p', 's', 'm')
        self.assertIn('Anthropic API Exception', result)

    def test_sends_correct_payload_structure(self):
        body = {'content': [{'text': 'ok'}]}
        mock_resp = self._mock_resp(200, body)
        with patch(_RU_KEYRING_GP, return_value='my-key'), \
             patch(_RU_REQUESTS_POST, return_value=mock_resp) as mock_post:
            ru.execute_anthropic('the user prompt', 'system text', 'claude-3-haiku')
        _, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['model'], 'claude-3-haiku')
        self.assertEqual(payload['system'], 'system text')
        self.assertEqual(payload['messages'][0]['content'], 'the user prompt')


# ===========================================================================
# TestExecuteOpenAI
# ===========================================================================
class TestExecuteOpenAI(unittest.TestCase):
    """reasoning_utils.execute_openai()"""

    def _mock_resp(self, status_code, body):
        m = MagicMock()
        m.status_code = status_code
        m.json.return_value = body
        m.text = str(body)
        m.raise_for_status = MagicMock()
        return m

    def test_returns_content_on_success(self):
        body = {'choices': [{'message': {'content': 'OpenAI response'}}]}
        mock_resp = self._mock_resp(200, body)
        with patch(_RU_KEYRING_GP, return_value='sk-test'), \
             patch(_RU_REQUESTS_POST, return_value=mock_resp):
            result = ru.execute_openai('prompt', 'sys', 'gpt-4o-mini', 'http://localhost:1234/v1/chat/completions')
        self.assertEqual(result, 'OpenAI response')

    def test_returns_error_on_exception(self):
        with patch(_RU_KEYRING_GP, return_value='sk-test'), \
             patch(_RU_REQUESTS_POST, side_effect=Exception("timeout")):
            result = ru.execute_openai('p', 's', 'm', 'http://localhost:1234/v1/chat/completions')
        self.assertIn('OpenAI Error', result)


# ===========================================================================
# TestGenerateReasoningRouting
# ===========================================================================
class TestGenerateReasoningRouting(unittest.TestCase):
    """reasoning_utils.generate_reasoning() — provider routing logic."""

    def _cfg(self, provider, model='test-model', endpoint='', auth_type='API Key'):
        return {
            'models': {
                'tiers': {
                    'mytier': {
                        'provider': provider,
                        'model': model,
                        'endpoint': endpoint,
                        'auth_type': auth_type,
                    }
                }
            }
        }

    def test_routes_to_ollama_for_local_provider(self):
        cfg = self._cfg('local', endpoint='http://localhost:11434/api/generate')
        with patch.object(ru, 'execute_ollama', return_value='ollama-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'ollama-result')

    def test_routes_to_ollama_for_ollama_provider(self):
        cfg = self._cfg('ollama', endpoint='http://localhost:11434/api/generate')
        with patch.object(ru, 'execute_ollama', return_value='ollama2') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'ollama2')

    def test_routes_to_anthropic(self):
        cfg = self._cfg('anthropic')
        with patch.object(ru, 'execute_anthropic', return_value='ant-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'ant-result')

    def test_routes_to_openai_compat(self):
        cfg = self._cfg('openai-compat', endpoint='http://localhost:1234/v1/chat')
        with patch.object(ru, 'execute_openai', return_value='openai-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'openai-result')

    def test_routes_to_openrouter(self):
        cfg = self._cfg('openrouter')
        with patch.object(ru, 'execute_openrouter', return_value='or-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'or-result')

    def test_routes_to_codex_cli(self):
        cfg = self._cfg('codex-cli')
        with patch.object(ru, 'execute_codex', return_value='codex-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'codex-result')

    def test_routes_to_google(self):
        cfg = self._cfg('google', auth_type='OAuth (System Default / CLI)')
        with patch.object(ru, 'execute_google', return_value='google-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'google-result')

    def test_returns_error_for_unknown_provider(self):
        cfg = self._cfg('unknown-provider-xyz')
        result = ru.generate_reasoning('prompt', brain_type='mytier', config=cfg)
        self.assertIn('Error', result)
        self.assertIn('Unsupported', result)

    def test_fallback_to_global_reasoning_config(self):
        """When no tier-specific config exists, falls back to global reasoning_provider."""
        cfg = {
            'models': {
                'reasoning_provider': 'ollama',
                'reasoning_model': 'llama3',
                'reasoning_endpoint': 'http://localhost:11434/api/generate',
                'tiers': {}
            }
        }
        with patch.object(ru, 'execute_ollama', return_value='fallback-result') as m:
            result = ru.generate_reasoning('prompt', brain_type='nonexistent_tier', config=cfg)
        m.assert_called_once()
        self.assertEqual(result, 'fallback-result')


# ===========================================================================
# TestGoogleOAuthJsonParser
# ===========================================================================
class TestGoogleOAuthJsonParser(unittest.TestCase):
    """execute_google() — OAuth path with subprocess and the brace-matching parser."""

    def _proc(self, stdout='', stderr='', returncode=0):
        p = MagicMock()
        p.stdout = stdout
        p.stderr = stderr
        p.returncode = returncode
        return p

    def test_extracts_response_from_valid_json_in_stdout(self):
        payload = json.dumps({"response": "parsed answer"})
        noise = f"Warning: noise\n{payload}\nmore noise"
        with patch(_RU_SUBPROCESS, return_value=self._proc(stdout=noise)):
            result = ru.execute_google('prompt', 'sys', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertEqual(result, 'parsed answer')

    def test_picks_last_valid_json_with_response_key(self):
        j1 = json.dumps({"irrelevant": "data"})
        j2 = json.dumps({"response": "correct answer"})
        with patch(_RU_SUBPROCESS, return_value=self._proc(stdout=f"{j1}\n{j2}")):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertEqual(result, 'correct answer')

    def test_returns_error_when_no_json_in_output(self):
        with patch(_RU_SUBPROCESS, return_value=self._proc(stdout='no json here', stderr='')):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertIn('Error', result)

    def test_capacity_lockout_in_stderr(self):
        p = self._proc(stdout='', stderr='MODEL_CAPACITY_EXHAUSTED', returncode=1)
        with patch(_RU_SUBPROCESS, return_value=p):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertEqual(result, '[ERROR: CAPACITY_LOCKOUT]')

    def test_capacity_lockout_in_stdout(self):
        p = self._proc(stdout='MODEL_CAPACITY_EXHAUSTED info', stderr='', returncode=0)
        with patch(_RU_SUBPROCESS, return_value=p):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertEqual(result, '[ERROR: CAPACITY_LOCKOUT]')

    def test_nonzero_returncode_returns_cli_error(self):
        p = self._proc(stdout='', stderr='some gemini error\nmore details', returncode=1)
        with patch(_RU_SUBPROCESS, return_value=p):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash',
                                       auth_type='OAuth (System Default / CLI)')
        self.assertIn('Gemini CLI Error', result)

    def test_google_api_key_route_returns_response(self):
        body = {'candidates': [{'content': {'parts': [{'text': 'api key answer'}]}}]}
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = body
        mock_resp.raise_for_status = MagicMock()
        with patch(_RU_KEYRING_GP, return_value='my-google-key'), \
             patch(_RU_REQUESTS_POST, return_value=mock_resp):
            result = ru.execute_google('prompt', 'sys', 'gemini-2.5-flash', auth_type='API Key')
        self.assertEqual(result, 'api key answer')

    def test_google_api_key_missing_returns_error(self):
        with patch(_RU_KEYRING_GP, return_value=None):
            result = ru.execute_google('p', 's', 'gemini-2.5-flash', auth_type='API Key')
        self.assertIn('Error', result)


# ===========================================================================
# Pipeline module test base
# ===========================================================================
class PipelineTestBase(unittest.TestCase):
    """
    Base: creates an isolated fake aim-root for each test, then loads the
    target pipeline module via importlib so top-level globals resolve there.
    """
    MODULE_FILENAME = None  # subclasses set this

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        _make_fake_aim_root(self.tmp)
        self.mod = _load_pipeline_module(self.MODULE_FILENAME, self.tmp)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    @property
    def proposals_dir(self):
        return os.path.join(self.tmp, 'memory', 'proposals')

    @property
    def hourly_dir(self):
        return os.path.join(self.tmp, 'memory', 'hourly')

    def _write(self, directory, filename, content='test content'):
        path = os.path.join(directory, filename)
        with open(path, 'w') as f:
            f.write(content)
        return path


# ===========================================================================
# daily_refiner.py
# ===========================================================================
class TestDailyRefinerGetRecentProposals(PipelineTestBase):
    MODULE_FILENAME = 'daily_refiner.py'

    def test_empty_dir_returns_empty(self):
        files, combined = self.mod.get_recent_proposals()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_non_matching_files_skipped(self):
        for name in ['PROPOSAL_20240101_DAILY.md', 'notes.txt', 'PROPOSAL_abc_WEEKLY.md']:
            self._write(self.proposals_dir, name)
        files, combined = self.mod.get_recent_proposals()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_matching_files_returned_sorted(self):
        names = ['PROPOSAL_20240103_DELTA.md', 'PROPOSAL_20240101_DELTA.md', 'PROPOSAL_20240102_DELTA.md']
        for name in names:
            self._write(self.proposals_dir, name, f'content of {name}')
        files, _ = self.mod.get_recent_proposals()
        self.assertEqual([os.path.basename(p) for p in files], sorted(names))

    def test_combined_text_contains_headers_and_content(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DELTA.md', 'delta content here')
        _, combined = self.mod.get_recent_proposals()
        self.assertIn('TIER 2 PROPOSAL', combined)
        self.assertIn('PROPOSAL_20240101_DELTA.md', combined)
        self.assertIn('delta content here', combined)


class TestDailyRefinerMain(PipelineTestBase):
    MODULE_FILENAME = 'daily_refiner.py'

    def test_exits_early_when_should_run_tier_false(self):
        with patch.object(self.mod, 'should_run_tier', return_value=False) as mock_srt, \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_srt.assert_called_once_with('tier3', unittest.mock.ANY)
        mock_gr.assert_not_called()

    def test_skips_when_no_proposals(self):
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_gr.assert_not_called()

    def test_full_run_calls_generate_mark_cleanup(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DELTA.md', 'proposal content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='daily state') as mock_gr, \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr, \
             patch.object(self.mod, 'cleanup_consumed_files') as mock_ccf:
            self.mod.main()
        mock_gr.assert_called_once()
        mock_mtr.assert_called_once_with('tier3')
        mock_ccf.assert_called_once()

    def test_no_mark_when_capacity_lockout(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DELTA.md', 'content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='[ERROR: CAPACITY_LOCKOUT]'), \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr:
            self.mod.main()
        mock_mtr.assert_not_called()

    def test_no_mark_when_generate_returns_none(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DELTA.md', 'content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value=None), \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr:
            self.mod.main()
        mock_mtr.assert_not_called()

    def test_saves_proposal_with_daily_suffix(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DELTA.md', 'content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='daily output'), \
             patch.object(self.mod, 'mark_tier_run'), \
             patch.object(self.mod, 'cleanup_consumed_files'):
            self.mod.main()
        import glob as _glob
        saved = _glob.glob(os.path.join(self.proposals_dir, 'PROPOSAL_*_DAILY.md'))
        self.assertEqual(len(saved), 1)


# ===========================================================================
# weekly_consolidator.py
# ===========================================================================
class TestWeeklyConsolidatorGetRecentDailyStates(PipelineTestBase):
    MODULE_FILENAME = 'weekly_consolidator.py'

    def test_empty_dir_returns_empty(self):
        files, combined = self.mod.get_recent_daily_states()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_non_matching_files_skipped(self):
        for name in ['PROPOSAL_20240101_DELTA.md', 'PROPOSAL_20240101_WEEKLY.md', 'notes.txt']:
            self._write(self.proposals_dir, name)
        files, combined = self.mod.get_recent_daily_states()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_daily_files_returned_sorted(self):
        names = ['PROPOSAL_20240103_DAILY.md', 'PROPOSAL_20240101_DAILY.md']
        for name in names:
            self._write(self.proposals_dir, name, f'content {name}')
        files, _ = self.mod.get_recent_daily_states()
        self.assertEqual([os.path.basename(p) for p in files], sorted(names))

    def test_combined_contains_daily_state_header_and_content(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DAILY.md', 'daily data here')
        _, combined = self.mod.get_recent_daily_states()
        self.assertIn('DAILY STATE', combined)
        self.assertIn('daily data here', combined)


class TestWeeklyConsolidatorMain(PipelineTestBase):
    MODULE_FILENAME = 'weekly_consolidator.py'

    def test_exits_early_when_should_run_tier_false(self):
        with patch.object(self.mod, 'should_run_tier', return_value=False) as mock_srt, \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_srt.assert_called_once_with('tier4', unittest.mock.ANY)
        mock_gr.assert_not_called()

    def test_skips_when_no_daily_states(self):
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_gr.assert_not_called()

    def test_full_run_calls_generate_and_saves_weekly_file(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DAILY.md', 'daily content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='weekly output') as mock_gr, \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr, \
             patch.object(self.mod, 'cleanup_consumed_files'):
            self.mod.main()
        mock_gr.assert_called_once()
        mock_mtr.assert_called_once_with('tier4')
        import glob as _glob
        saved = _glob.glob(os.path.join(self.proposals_dir, 'PROPOSAL_*_WEEKLY.md'))
        self.assertEqual(len(saved), 1)

    def test_no_mark_on_capacity_lockout(self):
        self._write(self.proposals_dir, 'PROPOSAL_20240101_DAILY.md', 'daily content')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='[ERROR: CAPACITY_LOCKOUT]'), \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr:
            self.mod.main()
        mock_mtr.assert_not_called()


# ===========================================================================
# memory_proposer.py
# ===========================================================================
class TestMemoryProposerGetRecentSummaries(PipelineTestBase):
    MODULE_FILENAME = 'memory_proposer.py'

    def test_empty_hourly_dir_returns_empty(self):
        files, combined = self.mod.get_recent_summaries()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_md_files_in_hourly_dir_returned(self):
        for name in ['report_001.md', 'report_002.md']:
            self._write(self.hourly_dir, name, f'content of {name}')
        files, combined = self.mod.get_recent_summaries()
        self.assertEqual(len(files), 2)
        self.assertIn('content of report_001.md', combined)
        self.assertIn('HOURLY REPORT', combined)

    def test_non_md_files_are_skipped(self):
        self._write(self.hourly_dir, 'report.txt', 'text file')
        files, combined = self.mod.get_recent_summaries()
        self.assertEqual(files, [])
        self.assertEqual(combined, '')

    def test_files_returned_sorted(self):
        names = ['report_c.md', 'report_a.md', 'report_b.md']
        for name in names:
            self._write(self.hourly_dir, name, 'x')
        files, _ = self.mod.get_recent_summaries()
        self.assertEqual([os.path.basename(p) for p in files], sorted(names))


class TestMemoryProposerMain(PipelineTestBase):
    MODULE_FILENAME = 'memory_proposer.py'

    def test_exits_early_when_should_run_tier_false(self):
        with patch.object(self.mod, 'should_run_tier', return_value=False) as mock_srt, \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_srt.assert_called_once_with('tier2', unittest.mock.ANY)
        mock_gr.assert_not_called()

    def test_skips_when_no_summaries(self):
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning') as mock_gr:
            self.mod.main()
        mock_gr.assert_not_called()

    def test_full_run_saves_delta_file(self):
        self._write(self.hourly_dir, 'report_001.md', 'hourly session data')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='arc proposal') as mock_gr, \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr, \
             patch.object(self.mod, 'cleanup_consumed_files'):
            self.mod.main()
        mock_gr.assert_called_once()
        mock_mtr.assert_called_once_with('tier2')
        import glob as _glob
        saved = _glob.glob(os.path.join(self.proposals_dir, 'PROPOSAL_*_DELTA.md'))
        self.assertEqual(len(saved), 1)

    def test_no_mark_on_capacity_lockout(self):
        self._write(self.hourly_dir, 'report_001.md', 'hourly data')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value='[ERROR: CAPACITY_LOCKOUT]'), \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr:
            self.mod.main()
        mock_mtr.assert_not_called()

    def test_no_mark_on_none_result(self):
        self._write(self.hourly_dir, 'report_001.md', 'hourly data')
        with patch.object(self.mod, 'should_run_tier', return_value=True), \
             patch.object(self.mod, 'generate_reasoning', return_value=None), \
             patch.object(self.mod, 'mark_tier_run') as mock_mtr:
            self.mod.main()
        mock_mtr.assert_not_called()


if __name__ == '__main__':
    unittest.main()
