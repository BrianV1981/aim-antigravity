#!/usr/bin/env python3
"""
TDD Tests for Event-Driven Mail Check (Issue #27)
Tests that check_mail_silently() is non-blocking and fails gracefully in all scenarios.
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Bootstrap path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestCheckMailSilently:
    """Tests for the event-driven mail check function."""

    @patch("aim_cli.subprocess.run")
    @patch("aim_cli.ensure_chalkboard_dependencies")
    def test_successful_mail_check(self, mock_deps, mock_run):
        """Mail check should complete without raising when hub is available."""
        from aim_cli import check_mail_silently
        mock_deps.return_value = "/fake/hub/scripts"
        mock_run.return_value = MagicMock(returncode=0)

        # Should not raise
        result = check_mail_silently()
        assert result is True
        mock_run.assert_called_once()

    @patch("aim_cli.subprocess.run")
    @patch("aim_cli.ensure_chalkboard_dependencies")
    def test_timeout_returns_gracefully(self, mock_deps, mock_run):
        """Mail check should return False on timeout, never crash."""
        import subprocess
        from aim_cli import check_mail_silently
        mock_deps.return_value = "/fake/hub/scripts"
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="mail", timeout=10)

        result = check_mail_silently()
        assert result is False

    @patch("aim_cli.ensure_chalkboard_dependencies")
    def test_missing_hub_returns_gracefully(self, mock_deps):
        """Mail check should return False when chalkboard hub is missing."""
        from aim_cli import check_mail_silently
        mock_deps.side_effect = SystemExit(1)

        result = check_mail_silently()
        assert result is False

    @patch("aim_cli.subprocess.run")
    @patch("aim_cli.ensure_chalkboard_dependencies")
    def test_generic_exception_returns_gracefully(self, mock_deps, mock_run):
        """Mail check should swallow any unexpected exception."""
        from aim_cli import check_mail_silently
        mock_deps.return_value = "/fake/hub/scripts"
        mock_run.side_effect = Exception("Network error")

        result = check_mail_silently()
        assert result is False

    @patch("aim_cli.subprocess.run")
    @patch("aim_cli.ensure_chalkboard_dependencies")
    def test_nonzero_exit_returns_gracefully(self, mock_deps, mock_run):
        """Mail check should handle non-zero exit codes without crashing."""
        import subprocess
        from aim_cli import check_mail_silently
        mock_deps.return_value = "/fake/hub/scripts"
        mock_run.side_effect = subprocess.CalledProcessError(1, "mail")

        result = check_mail_silently()
        assert result is False


class TestMailCheckIntegrationPoints:
    """Tests that mail check is wired into the correct lifecycle events."""

    def test_cmd_push_calls_mail_check(self):
        """cmd_push should call check_mail_silently after pushing."""
        from aim_cli import cmd_push
        source = __import__('inspect').getsource(cmd_push)
        assert "check_mail_silently" in source, "cmd_push must call check_mail_silently()"

    def test_cmd_sync_issues_calls_mail_check(self):
        """cmd_sync_issues should call check_mail_silently after syncing."""
        from aim_cli import cmd_sync_issues
        source = __import__('inspect').getsource(cmd_sync_issues)
        assert "check_mail_silently" in source, "cmd_sync_issues must call check_mail_silently()"

    def test_cmd_crash_calls_mail_check(self):
        """cmd_crash should call check_mail_silently during recovery."""
        from aim_cli import cmd_crash
        source = __import__('inspect').getsource(cmd_crash)
        assert "check_mail_silently" in source, "cmd_crash must call check_mail_silently()"
