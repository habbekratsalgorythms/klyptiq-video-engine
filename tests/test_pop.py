import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import render

class PopTests(unittest.TestCase):
    def test_short_caption_beats_no_empty_and_max_four(self):
        self.assertEqual(render.split_caption_beats("GTA SIX IS HERE"),["GTA SIX IS","HERE"])
        self.assertEqual(len(render.split_caption_beats(" ".join("word"+str(i) for i in range(14)))),4)
        with self.assertRaises(ValueError):render.split_caption_beats("  ")

    def test_high_contrast_overlay_keeps_original_photo_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"beat.png"
            render.make_pop_caption(p,320,568,"ONE BIG MOMENT",0,5)
            img=Image.open(p).convert("RGBA")
            self.assertEqual(img.getpixel((160,250))[3],0)
            self.assertGreater(img.getpixel((160,450))[3],0)
            self.assertEqual(img.size,(320,568))

    def test_real_ffmpeg_pop_render_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            Image.new("RGB",(640,360),(175,45,95)).save(root/"scene1.png")
            Image.new("RGB",(640,360),(20,155,205)).save(root/"scene2.png")
            brief={
                "title":"KLYPTIQ POP TEST",
                "label":"WISHLIST — NOT CONFIRMED",
                "script":"One big gaming moment. And a second clear detail.",
                "scenes":[
                    {"caption":"ONE BIG GAMING MOMENT","voiceover":"One big gaming moment.","asset":"scene1.png"},
                    {"caption":"A SECOND CLEAR DETAIL","voiceover":"And a second clear detail.","asset":"scene2.png"}
                ]
            }
            b=root/"brief.json"
            b.write_text(json.dumps(brief))
            output=root/"pop.mp4"
            result=render.render(b,output,"espeak",None,"en-us",320,568,25,
                                 quality="preview",motion=False,pace=1.0,pop=True)
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size,10000)
            self.assertGreater(result["duration_seconds"],3)

if __name__=="__main__":unittest.main()
