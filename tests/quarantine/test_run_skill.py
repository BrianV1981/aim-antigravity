import os
import sys
import shutil

plugin_dir = os.path.join(os.path.dirname(__file__), "../plugins/run_skill")
sys.path.insert(0, plugin_dir)
import run

def test_sandboxed_run_isolation(monkeypatch, tmp_path):
    """
    Empirically verify that the underlying execution sandbox binds and executes
    standard skills natively without demanding the old headless API structure.
    """
    monkeypatch.setattr(run, "AIM_ROOT", str(tmp_path))
    monkeypatch.setattr(run, "SKILLS_DIR", tmp_path / "skills")
    monkeypatch.setattr(run, "ARCHIVE_DIR", tmp_path / "archive")
    
    os.makedirs(tmp_path / "skills", exist_ok=True)
    os.makedirs(tmp_path / "archive", exist_ok=True)
    
    # Mock a dummy payload
    dummy_skill = tmp_path / "skills" / "dummy_skill.py"
    dummy_skill.write_text("print('Mock isolated execution successful.')")
    
    output = run._sandboxed_run(dummy_skill, {})
    
    # Assert whether the bubblewrap proxy effectively passed, or successfully
    # trapped the failure if the user's host OS is incapable of unshare.
    if not shutil.which("bwrap"):
        assert "bubblewrap (bwrap) not installed" in output
    else:
        assert "Mock isolated execution successful." in output
