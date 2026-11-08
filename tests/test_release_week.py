"""Static fact-provenance and format validation for editorial GTA VI release-week drafts.

These checks do NOT replace checking live official information on publication day.
"""
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
BRIEFS=ROOT/"briefs"/"release-week"
EXPECTED={"preload-nov10","lucia-backstory","jason-backstory"}
class ReleaseWeekTests(unittest.TestCase):
    def test_briefs_source_provenance_and_original_lines(self):
        present={p.stem for p in BRIEFS.glob("*.json")}
        self.assertEqual(present,EXPECTED)
        starts=[]
        for slug in sorted(EXPECTED):
            data=json.loads((BRIEFS/f"{slug}.json").read_text())
            self.assertEqual(data.get("content_status"),"official_only")
            url=urlparse(data.get("source_url",""))
            self.assertEqual((url.scheme,url.netloc),("https","www.rockstargames.com"))
            self.assertEqual(url.path,"/VI")
            self.assertEqual(data.get("verified_as_of"),"2026-11-08")
            self.assertEqual(len(data["scenes"]),5)
            self.assertEqual(data["script"]," ".join(s["voiceover"] for s in data["scenes"]))
            starts.append(data["scenes"][0]["voiceover"])
            for scene in data["scenes"]:
                self.assertTrue(scene["caption"].strip())
                self.assertGreater(len(scene["voiceover"]),12)
                self.assertTrue(scene["asset"].startswith("../../assets/"))
                self.assertTrue(scene["asset"].endswith(".jpg"))
                self.assertGreaterEqual(scene["pace"],0.85)
                self.assertLessEqual(scene["pace"],1.3)
        self.assertEqual(len(set(starts)),len(starts),"Three scripts need different hooks")
    def test_preload_facts_do_not_say_game_already_released(self):
        data=json.loads((BRIEFS/"preload-nov10.json").read_text())
        script=data["script"].lower()
        self.assertIn("november tenth",script)
        self.assertIn("november nineteenth",script)
        self.assertNotIn("out now",script)
        self.assertNotIn("available today",script)

if __name__=="__main__":unittest.main()
