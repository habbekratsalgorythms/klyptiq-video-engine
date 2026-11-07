"""Checks for honest scene timing and high-quality export safeguards."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import render

class VoiceAndQualityTests(unittest.TestCase):
    def make_brief(self, directory, lines):
        path=Path(directory)/"brief.json"
        path.write_text(json.dumps({"title":"Unit test",
           "script":" ".join(lines),
           "scenes":[{"caption":line, "voiceover":line} for line in lines]}))
        return path

    def test_reject_partial_voiceover(self):
        with tempfile.TemporaryDirectory() as tmp:
            b=Path(tmp)/"brief.json"
            b.write_text(json.dumps({"title":"a", "script":"words",
              "scenes":[{"caption":"first", "voiceover":"One."},
                        {"caption":"second"}]}))
            with self.assertRaisesRegex(ValueError,"every scene"):
                render.parse_brief(b)

    def test_scene_voiceover_matches_actual_audio_durations(self):
        with tempfile.TemporaryDirectory() as tmp:
            brief=self.make_brief(tmp,["Hello.", "This longer second sentence contains more words than the first sentence."])
            data=render.parse_brief(brief)
            wav,durations,spoken,total=render.build_narration(
                Path(tmp),data,data["scenes"],"espeak",None,"en-us")
            self.assertTrue(wav.is_file())
            self.assertGreater(durations[1],durations[0])
            self.assertAlmostEqual(sum(durations),total,delta=0.04)
            self.assertAlmostEqual(render.length(wav),spoken,delta=0.04)

    def test_no_espeak_in_production(self):
        with self.assertRaisesRegex(ValueError,"Piper"):
            render.render("/unavailable/brief.json","/tmp/not-written.mp4",
                "espeak",None,"en-us",1080,1920,20,quality="production")

    def test_preview_legacy_brief_still_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            b=Path(tmp)/"brief.json"
            b.write_text(json.dumps({"title":"a","script":"Hello from Klyptiq. This is a test.",
                "scenes":[{"caption":"first"},{"caption":"second"}]}))
            brief=render.parse_brief(b)
            wav,durations,spoken,total=render.build_narration(
                Path(tmp),brief,brief["scenes"],"espeak",None,"en-us")
            self.assertEqual(len(durations),2)
            self.assertAlmostEqual(sum(durations),total,delta=0.04)
            self.assertTrue(wav.is_file())

if __name__=="__main__":
    unittest.main()
