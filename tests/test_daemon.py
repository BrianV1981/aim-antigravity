import os
import sys

# Append the source directory so we can natively import our background daemon
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
import daemon

def test_inject_pulse(monkeypatch, tmp_path):
    """
    Empirically verifies that the daemon decouples from standard input by successfully
    generating the Autonomic YAML heartbeat file within the local workflows boundary.
    """
    # Isolate AIM_ROOT to a temporary test directory so we don't litter the repo
    monkeypatch.setattr(daemon, "AIM_ROOT", str(tmp_path))
    monkeypatch.setattr(daemon, "DAEMON_LOG", str(tmp_path / "daemon.log"))
    
    mock_prompt = "Mock TDD System Directive"
    daemon.inject_pulse(mock_prompt)
    
    workflow_dir = tmp_path / ".agents" / "workflows"
    pulse_file = workflow_dir / "daemon_pulse.md"
    
    # Assert the State Engineering framework physically generated the file
    assert os.path.exists(pulse_file), "Daemon failed to decouple: Pulse file was not generated."
    
    with open(pulse_file, "r") as f:
        content = f.read()
        
    # Assert YAML frontmatter and explicitly passed prompts exist
    assert "description: Current Project Status and Autonomic Pulse." in content
    assert "**DIRECTIVE:**\nMock TDD System Directive" in content
