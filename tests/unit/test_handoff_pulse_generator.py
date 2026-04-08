import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile

# Add src to path to import handoff_pulse_generator
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))


class TestHandoffPulseGenerator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    @patch('handoff_pulse_generator.extract_latest_markdown_export', return_value="# Dummy Transcript")
    @patch('handoff_pulse_generator.parse_markdown_transcript', return_value=[{'role': 'user', 'text': 'test'}])
    @patch('sqlite3.connect')
    @patch('subprocess.run')
    def test_handoff_pulse_executes_sync_issue_tracker(self, mock_subprocess, mock_sql, mock_parse, mock_extract):
        # We need to test if sync_issue_tracker is executed 
        import handoff_pulse_generator
        
        # Override pathways so we don't pollute the real workspace
        orig_aim_root = handoff_pulse_generator.AIM_ROOT
        orig_continuity = handoff_pulse_generator.CONTINUITY_DIR
        orig_archive = handoff_pulse_generator.ARCHIVE_RAW_DIR
        
        handoff_pulse_generator.AIM_ROOT = self.tmp_dir
        handoff_pulse_generator.CONTINUITY_DIR = os.path.join(self.tmp_dir, "continuity")
        handoff_pulse_generator.ARCHIVE_RAW_DIR = os.path.join(self.tmp_dir, "raw")
        
        # Try running it
        handoff_pulse_generator.generate_handoff_pulse()
        
        # Verify sync_issue_tracker was executed via subprocess or verify it was called
        # We can check if subprocess.run was called with sync_issue_tracker.py
        sync_called = False
        for call_args in mock_subprocess.call_args_list:
            args, _ = call_args
            if 'sync_issue_tracker.py' in args[0][-1]:
                sync_called = True
                break
                
        self.assertTrue(sync_called, "Handoff pulse did not invoke the sync_issue_tracker.py script.")
        
        # Restore paths
        handoff_pulse_generator.AIM_ROOT = orig_aim_root
        handoff_pulse_generator.CONTINUITY_DIR = orig_continuity
        handoff_pulse_generator.ARCHIVE_RAW_DIR = orig_archive

if __name__ == "__main__":
    unittest.main()
