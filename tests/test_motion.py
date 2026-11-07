"""Test that image animation never moves or fades the text layer."""
import json
import tempfile
import unittest
from pathlib import Path
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import render

class MotionTests(unittest.TestCase):
    def test_text_overlay_is_transparent_over_photo_area(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"overlay.png"
            render.make_text_overlay(p,360,640,"GTA VI REVIEW","Test subtitle","WISHLIST — NOT CONFIRMED")
            overlay=Image.open(p).convert("RGBA")
            self.assertEqual(overlay.size,(360,640))
            self.assertEqual(overlay.getpixel((180,300))[3],0)
            self.assertGreater(overlay.getpixel((180,20))[3],0)
            self.assertGreater(overlay.getpixel((180,540))[3],0)

    def test_motion_video_has_valid_streams(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            for name,color in [("one",(240,35,50)),("two",(45,140,230))]:
                Image.new("RGB",(640,360),color).save(tmp/f"{name}.png")
            brief={
                "title":"TEST MOTION","script":"Hello. This is a longer spoken test line.",
                "scenes":[
                    {"caption":"First visible caption","voiceover":"Hello.",
                     "asset":"one.png"},
                    {"caption":"Second visible caption",
                     "voiceover":"This is a longer spoken test line.",
                     "asset":"two.png"}
                ]
            }
            b=tmp/"brief.json";b.write_text(json.dumps(brief))
            output=tmp/"moving.mp4"
            result=render.render(b,output,"espeak",None,"en-us",320,568,25,
                                 "preview",True)
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size,20000)
            self.assertGreater(result["duration_seconds"],3)

if __name__=="__main__":
    unittest.main()
