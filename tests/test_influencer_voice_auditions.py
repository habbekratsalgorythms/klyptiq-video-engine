"""Fast offline tests: no Kokoro installation/model download required."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import influencer_voice_auditions as voices


class InfluencerVoiceTests(unittest.TestCase):
    def test_four_distinct_original_character_voices(self):
        self.assertEqual(set(voices.PROFILES), {"vexa-volt", "pip", "patch", "blop"})
        voice_ids = [v["voice"] for v in voices.PROFILES.values()]
        self.assertEqual(len(voice_ids), len(set(voice_ids)))
        for p in voices.PROFILES.values():
            self.assertTrue(p["line"])
            self.assertLess(len(p["line"]), 75)
            self.assertGreaterEqual(p["speed"], 0.85)
            self.assertLessEqual(p["speed"], 1.3)

    def test_plan_never_claims_lipsync_or_publishing(self):
        data = voices.voice_plan()
        self.assertEqual(data["status"], "AUDITION_ONLY_NOT_LIPSYNCED")
        self.assertEqual(data["paid_api_calls"], 0)
        self.assertFalse(data["automatic_publication"])
        self.assertEqual(len(data["characters"]), 4)

    def test_default_dry_run_writes_no_files(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "never-created"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(voices.main(["--out", str(out)]), 0)
            self.assertFalse(out.exists())
            self.assertIn("SAFE DRY-RUN", buf.getvalue())
            self.assertIn('"id": "vexa-volt"', buf.getvalue())

    def test_execute_requires_local_verified_model_files(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "not-created"
            with self.assertRaises(FileNotFoundError):
                voices.synthesize(Path(temp)/"missing.onnx", Path(temp)/"missing.bin", out)
            self.assertFalse(out.exists())

    def test_refuses_to_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/"previous-review"
            output.mkdir()
            (output / "vexa-volt.wav").write_bytes(b"previous")
            m = Path(temp)/"model.onnx"
            v = Path(temp)/"voices.bin"
            m.write_bytes(b"test")
            v.write_bytes(b"test")
            with self.assertRaises(FileExistsError):
                voices.synthesize(m, v, output)


if __name__ == "__main__":
    unittest.main()
