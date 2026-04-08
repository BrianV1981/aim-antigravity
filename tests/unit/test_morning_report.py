import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "hooks"))

class TestMorningReport(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.report_path = os.path.join(self.tmp_dir, "MORNING_REPORT.md")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    @patch('subprocess.run')
    def test_morning_report_generates_correctly(self, mock_subprocess):
        import morning_report
        
        # Override pathways
        orig_aim_root = morning_report.AIM_ROOT
        orig_report_path = morning_report.REPORT_PATH
        orig_continuity = morning_report.CONTINUITY_DIR
        
        morning_report.AIM_ROOT = self.tmp_dir
        morning_report.CONTINUITY_DIR = os.path.join(self.tmp_dir, "continuity")
        morning_report.REPORT_PATH = self.report_path
        
        # Write dummy files to simulate environment
        with open(os.path.join(self.tmp_dir, "MEMORY.md"), "w") as f:
            f.write("# Memory State")
        
        os.makedirs(os.path.join(self.tmp_dir, "continuity"), exist_ok=True)
        with open(os.path.join(self.tmp_dir, "continuity", "ISSUE_TRACKER.md"), "w") as f:
            f.write("# Active Issues\n* #1 Test Issue")
            
        def mock_run_side_effect(cmd, *args, **kwargs):
            mock_result = MagicMock()
            if "rev-parse" in cmd:
                mock_result.stdout = "fix/issue-59\n"
            elif "status" in cmd:
                mock_result.stdout = "M src/test.py\n"
            elif "log" in cmd:
                mock_result.stdout = "ab12c3f Commit Message\n"
            else:
                mock_result.stdout = ""
            return mock_result
            
        mock_subprocess.side_effect = mock_run_side_effect
        
        # Run report generation
        morning_report.generate_morning_report()
        
        # Verify it created the report
        self.assertTrue(os.path.exists(self.report_path), "Morning report was not generated.")
        
        with open(self.report_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("fix/issue-59", content, "Does not contain git branch.")
            self.assertIn("Test Issue", content, "Does not contain issue tracker data.")
            
        # Restore logic
        morning_report.AIM_ROOT = orig_aim_root
        morning_report.CONTINUITY_DIR = orig_continuity
        morning_report.REPORT_PATH = orig_report_path

if __name__ == "__main__":
    unittest.main()
