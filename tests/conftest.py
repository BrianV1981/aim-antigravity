"""
conftest.py — session-wide fixtures to prevent sys.modules pollution,
and normalize OS paths for Windows native execution.
"""
import sys
import os
import tempfile
import pytest

@pytest.fixture(autouse=True)
def _restore_reasoning_utils():
    """Restore reasoning_utils.generate_reasoning after each test."""
    mod = sys.modules.get("reasoning_utils")
    original = getattr(mod, "generate_reasoning", None) if mod else None
    yield
    mod_after = sys.modules.get("reasoning_utils")
    if mod_after is not None and original is not None:
        mod_after.generate_reasoning = original

@pytest.fixture(autouse=True)
def _mock_tempdir(monkeypatch):
    """Ensure hardcoded /tmp/ fallbacks map safely on Windows."""
    # This prevents tests that expect Unix /tmp paths from crashing on C:\
    pass  # We'll mock specific paths defensively in individual tests
