import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile

# Add hooks to path to import session_summarizer
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "hooks"))

import session_summarizer

class TestSessionSummarizerSingleShot(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        
        # Mock MEMORY_PATH dynamically in the module
        self.mock_memory_path = os.path.join(self.tmp_dir, "MEMORY.md")
        self.orig_memory_path = session_summarizer.MEMORY_PATH
        session_summarizer.MEMORY_PATH = self.mock_memory_path
        
        self.transcript_path = os.path.join(self.tmp_dir, "raw_transcript.md")
        with open(self.transcript_path, "w", encoding="utf-8") as f:
            f.write("# Sample IDE Transcript")

    def tearDown(self):
        session_summarizer.MEMORY_PATH = self.orig_memory_path
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_compiler_missing_transcript(self, mock_generate):
        # Should return False and handle exception if file is missing
        result = session_summarizer.compile_single_shot("does_not_exist.md")
        self.assertFalse(result)
        mock_generate.assert_not_called()

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_compiler_handles_no_memory_md(self, mock_generate):
        # Even if MEMORY.md does not exist yet, it should proceed
        mock_generate.return_value = "Mocked Single Shot Synthesis Delta"
        
        result = session_summarizer.compile_single_shot(self.transcript_path)
        self.assertTrue(result)
        mock_generate.assert_called_once()
        
        # Verify it created a new MEMORY.md
        self.assertTrue(os.path.exists(self.mock_memory_path))
        with open(self.mock_memory_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Mocked Single Shot Synthesis Delta", content)
            self.assertIn("Session Delta", content)

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_compiler_appends_to_existing_memory(self, mock_generate):
        # Create an existing MEMORY.md
        with open(self.mock_memory_path, "w", encoding="utf-8") as f:
            f.write("EXISTING MEMORY RULES\n")
            
        mock_generate.return_value = "Mocked New Architectural Rule"
        
        result = session_summarizer.compile_single_shot(self.transcript_path)
        self.assertTrue(result)
        mock_generate.assert_called_once()
        
        # Verify it appended
        with open(self.mock_memory_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("EXISTING MEMORY RULES", content)
            self.assertIn("Mocked New Architectural Rule", content)

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_compiler_fails_on_lockout(self, mock_generate):
        mock_generate.return_value = "[ERROR: CAPACITY_LOCKOUT]"
        
        result = session_summarizer.compile_single_shot(self.transcript_path)
        self.assertFalse(result)
        
        # Verify memory remains untouched
        self.assertFalse(os.path.exists(self.mock_memory_path))

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_compiler_fails_on_none_response(self, mock_generate):
        mock_generate.return_value = None
        
        result = session_summarizer.compile_single_shot(self.transcript_path)
        self.assertFalse(result)
        
        self.assertFalse(os.path.exists(self.mock_memory_path))

    @patch('session_summarizer.generate_reasoning')
    def test_single_shot_truncates_massive_transcripts(self, mock_generate):
        # Create a massive file > 50000 chars
        massive_path = os.path.join(self.tmp_dir, "massive.md")
        with open(massive_path, "w", encoding="utf-8") as f:
            f.write("A" * 60000)
            
        mock_generate.return_value = "Truncation Handled"
        
        result = session_summarizer.compile_single_shot(massive_path)
        self.assertTrue(result)
        
        # Check what arguments generate_reasoning was called with
        args, kwargs = mock_generate.call_args
        combined_prompt = args[0]
        
        # It should end with ...[TRUNCATED] or similar from our logic
        self.assertIn("[TRUNCATED]", combined_prompt)
        self.assertLess(len(combined_prompt), 60000)

if __name__ == "__main__":
    unittest.main()
