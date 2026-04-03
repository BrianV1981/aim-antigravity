#!/usr/bin/env python3
"""
TDD Tests for history_scribe.py Event-Driven Chunker (Issues #22 + #26)

Tests that the stateless Markdown chunker:
- Parses a transcript into turns and writes chunks to memory/hourly/
- Uses 10-turn windows per chunk
- Is idempotent (no duplicate chunks on re-run)
- Handles empty/malformed transcripts gracefully
- Batch mode skips already-scribed files
"""
import os
import sys
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Bootstrap path
AIM_SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
AIM_ROOT = os.path.abspath(os.path.join(AIM_SRC, '..'))
sys.path.insert(0, AIM_SRC)
sys.path.insert(0, os.path.join(AIM_ROOT, 'scripts'))


def _build_sample_transcript(num_turns=25):
    """Build a fake Antigravity-style Markdown transcript with N user/model turn pairs."""
    lines = ["# Sample Session Transcript\n\n"]
    for i in range(num_turns):
        lines.append(f"### User Input\n\nUser message number {i+1}. This is a test prompt.\n\n")
        lines.append(f"### Planner Response\n\nModel response number {i+1}. This is a test response with enough content to be meaningful.\n\n")
    return "".join(lines)


class TestScribeSession(unittest.TestCase):
    """Tests for the primary scribe_session() entry point."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.hourly_dir = os.path.join(self.tmpdir, "memory", "hourly")
        self.archive_dir = os.path.join(self.tmpdir, "archive", "raw")
        self.state_file = os.path.join(self.tmpdir, "archive", "scribe_state.json")
        os.makedirs(self.archive_dir, exist_ok=True)

        # Write a sample transcript
        self.transcript_path = os.path.join(self.archive_dir, "session_20260403_120000.md")
        with open(self.transcript_path, 'w', encoding='utf-8') as f:
            f.write(_build_sample_transcript(25))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _import_scribe(self):
        import history_scribe as hs
        return hs

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    def test_produces_correct_number_of_chunks(self, mock_state, mock_hourly):
        """25 turn-pairs = 50 turns. At 10 turns per chunk = 5 chunks."""
        mock_hourly.__str__ = lambda s: self.hourly_dir
        mock_state.__str__ = lambda s: self.state_file
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file

        hs.scribe_session(self.transcript_path)

        chunks = [f for f in os.listdir(self.hourly_dir) if f.endswith('.md')]
        self.assertEqual(len(chunks), 5, f"Expected 5 chunks for 50 turns, got {len(chunks)}: {chunks}")

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    def test_chunk_files_contain_turn_content(self, mock_state, mock_hourly):
        """Each chunk file should contain actual USER and A.I.M. turn text."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file

        hs.scribe_session(self.transcript_path)

        chunks = sorted([f for f in os.listdir(self.hourly_dir) if f.endswith('.md')])
        self.assertTrue(len(chunks) > 0)

        first_chunk_path = os.path.join(self.hourly_dir, chunks[0])
        with open(first_chunk_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("User message number 1", content)
        self.assertIn("Model response number 1", content)

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    def test_idempotency_no_duplicate_chunks(self, mock_state, mock_hourly):
        """Running scribe_session twice on the same file produces no duplicates."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file

        hs.scribe_session(self.transcript_path)
        first_run_count = len([f for f in os.listdir(self.hourly_dir) if f.endswith('.md')])

        hs.scribe_session(self.transcript_path)
        second_run_count = len([f for f in os.listdir(self.hourly_dir) if f.endswith('.md')])

        self.assertEqual(first_run_count, second_run_count,
                         "Second run should not create additional chunks")

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    def test_empty_transcript_produces_no_chunks(self, mock_state, mock_hourly):
        """An empty or header-only transcript should produce zero chunks."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file

        empty_path = os.path.join(self.archive_dir, "session_empty.md")
        with open(empty_path, 'w', encoding='utf-8') as f:
            f.write("# Empty Session\n\nNo turns here.\n")

        hs.scribe_session(empty_path)

        if os.path.exists(self.hourly_dir):
            chunks = [f for f in os.listdir(self.hourly_dir) if f.endswith('.md')]
            self.assertEqual(len(chunks), 0)

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    def test_small_transcript_produces_single_chunk(self, mock_state, mock_hourly):
        """A transcript with fewer than 10 turns should produce exactly 1 chunk."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file

        small_path = os.path.join(self.archive_dir, "session_small.md")
        with open(small_path, 'w', encoding='utf-8') as f:
            f.write(_build_sample_transcript(3))  # 6 turns

        hs.scribe_session(small_path)

        chunks = [f for f in os.listdir(self.hourly_dir) if f.endswith('.md')]
        self.assertEqual(len(chunks), 1)


class TestScribeAllSessions(unittest.TestCase):
    """Tests for the batch scribe_all_sessions() function."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.hourly_dir = os.path.join(self.tmpdir, "memory", "hourly")
        self.archive_dir = os.path.join(self.tmpdir, "archive", "raw")
        self.state_file = os.path.join(self.tmpdir, "archive", "scribe_state.json")
        os.makedirs(self.archive_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    @patch('history_scribe.RAW_DIR')
    def test_batch_processes_multiple_transcripts(self, mock_raw, mock_state, mock_hourly):
        """Batch mode should process all .md files in archive/raw/."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file
        hs.RAW_DIR = self.archive_dir

        # Write 2 transcripts
        for i in range(2):
            path = os.path.join(self.archive_dir, f"session_{i}.md")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(_build_sample_transcript(5))  # 10 turns each → 1 chunk each

        hs.scribe_all_sessions()

        chunks = [f for f in os.listdir(self.hourly_dir) if f.endswith('.md')]
        self.assertEqual(len(chunks), 2)

    @patch('history_scribe.HOURLY_DIR')
    @patch('history_scribe.STATE_FILE')
    @patch('history_scribe.RAW_DIR')
    def test_batch_skips_already_scribed(self, mock_raw, mock_state, mock_hourly):
        """Batch mode should skip files already in the state ledger."""
        hs = self._import_scribe()
        hs.HOURLY_DIR = self.hourly_dir
        hs.STATE_FILE = self.state_file
        hs.RAW_DIR = self.archive_dir

        path = os.path.join(self.archive_dir, "session_done.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(_build_sample_transcript(5))

        # First run
        hs.scribe_all_sessions()
        first_count = len([f for f in os.listdir(self.hourly_dir) if f.endswith('.md')])

        # Second run
        hs.scribe_all_sessions()
        second_count = len([f for f in os.listdir(self.hourly_dir) if f.endswith('.md')])

        self.assertEqual(first_count, second_count)

    def _import_scribe(self):
        import history_scribe as hs
        return hs


class TestStateTracking(unittest.TestCase):
    """Tests for the idempotency state ledger."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.tmpdir, "scribe_state.json")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_state_file_created_after_scribe(self):
        """The state ledger JSON should exist after scribing."""
        hs = __import__('history_scribe')
        hs.STATE_FILE = self.state_file
        hs.HOURLY_DIR = os.path.join(self.tmpdir, "hourly")

        transcript = os.path.join(self.tmpdir, "test.md")
        with open(transcript, 'w') as f:
            f.write(_build_sample_transcript(3))

        hs.scribe_session(transcript)

        self.assertTrue(os.path.exists(self.state_file))

    def test_state_file_records_processed_filename(self):
        """The state ledger should contain the basename of the processed file."""
        hs = __import__('history_scribe')
        hs.STATE_FILE = self.state_file
        hs.HOURLY_DIR = os.path.join(self.tmpdir, "hourly")

        transcript = os.path.join(self.tmpdir, "session_xyz.md")
        with open(transcript, 'w') as f:
            f.write(_build_sample_transcript(3))

        hs.scribe_session(transcript)

        with open(self.state_file, 'r') as f:
            state = json.load(f)

        self.assertIn("session_xyz.md", state)


if __name__ == "__main__":
    unittest.main()
