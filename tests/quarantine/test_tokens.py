import sys
import os

# Append scripts directory to path for testing
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(os.path.dirname(current_dir), "scripts")
sys.path.insert(0, scripts_dir)

import aim_cli

def test_cmd_tokens_exists():
    """TDD: Prove the token generator function actually exists in the CLI router."""
    assert hasattr(aim_cli, "cmd_tokens"), "cmd_tokens function must exist in aim_cli.py"

def test_cmd_tokens_execution_safe(capsys):
    """TDD: Prove firing the tokens command doesn't trigger fatal tracebacks even when no logs exist."""
    try:
        aim_cli.cmd_tokens(None)
        captured = capsys.readouterr()
        # Verify it successfully runs and outputs the header
        assert "ACTIVE CONTEXT GAUGE" in captured.out
    except Exception as e:
        assert False, f"cmd_tokens threw an exception: {e}"
