"""Real local end-to-end director-style cut testing; no external or copyrighted assets."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import director_cut
import render

class DirectorTests(unittest.TestCase):
    def media(self, root):
        for i,pattern in enumerate(("testsrc2","smptebars"),1):
            render.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                        "-f","lavfi","-i",f"{pattern}=size=320x180:rate=30",
                        "-t","2","-c:v","libx264","-pix_fmt","yuv420p",
                        root/f"v{i}.mp4"])
        Image.new("RGB",(500,360),(221,67,42)).save(root/"a.png")
        Image.new("RGB",(500,360),(45,175,205)).save(root/"b.png")

    def brief(self,root):
        data={
            "title":"TEST REAL CUTS","script":"This footage is moving. Watch the second detail.",
            "label":"SYNTHETIC REVIEW",
            "scenes":[
                {"caption":"FAST HOOK REAL MOTION","voiceover":"This footage is moving.",
                 "shots":[
                    {"asset_video":"v1.mp4","media_rights":"self_recorded","text":"REAL MOTION"},
                    {"asset":"a.png","media_rights":"self_recorded","text":"FAST HOOK"}]},
                {"caption":"SECOND VISUAL DETAIL","voiceover":"Watch the second detail.",
                 "shots":[
                    {"asset_video":"v2.mp4","media_rights":"self_recorded","text":"NEW CAMERA"},
                    {"asset":"b.png","media_rights":"self_recorded","text":"QUICK CUT"}]}
            ]
        }
        p=root/"test.json";p.write_text(json.dumps(data));return p

    def test_rejects_slideshow_and_missing_rights(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            data=render.parse_brief(p)
            self.assertEqual(director_cut.prepare(data,p)["moving_shots"],2)
            data["scenes"][0]["shots"][0].pop("media_rights")
            with self.assertRaisesRegex(ValueError,"media_rights"):
                director_cut.prepare(data,p)
            data=render.parse_brief(p)
            for s in data["scenes"]:
                s["shots"]=[{"asset":"a.png","media_rights":"self_recorded"},
                            {"asset":"b.png","media_rights":"self_recorded"}]
            with self.assertRaisesRegex(ValueError,"video"):
                director_cut.prepare(data,p)

    def test_no_opaque_slideshow_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"caption.png"
            director_cut.overlay_file(p,320,568,"BIG NEW HOOK",.3,first=True)
            im=Image.open(p).convert("RGBA")
            self.assertEqual(im.getpixel((160,260))[3],0)
            self.assertGreater(im.getpixel((160,450))[3],0)
            self.assertGreater(im.getpixel((50,566))[3],0)

    def test_four_edited_shots_with_original_sfx(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            output=root/"director.mp4"
            result=render.render(p,output,"espeak",None,"en-us",
                                 320,568,27,quality="preview",director=True)
            self.assertEqual(result["shot_count"],4)
            self.assertEqual(result["cuts"],3)
            self.assertEqual(result["moving_shots"],2)
            self.assertFalse(result["source_audio_used"])
            self.assertTrue(output.stat().st_size>15000)
            info=render.run(["ffprobe","-v","error","-show_entries",
                             "stream=codec_name,codec_type","-of","csv=p=0",output]).stdout
            self.assertIn("h264",info)
            self.assertIn("aac",info)

if __name__=="__main__":
    unittest.main()
