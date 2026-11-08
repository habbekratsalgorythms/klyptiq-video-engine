"""Opt-in licensed gameplay cuts, with synthetic media and no third-party downloads."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import render

class LicensedClipTests(unittest.TestCase):
    def make_brief(self,root,rights="self_recorded"):
        data={"title":"OFFLINE VIDEO TEST","label":"SYNTHETIC TEST FOOTAGE",
          "script":"Look at this moving demo. And here is a still image.",
          "scenes":[
             {"caption":"ACTUAL MOVING VIDEO","voiceover":"Look at this moving demo.",
              "asset_video":"clip.mp4","media_rights":rights},
             {"caption":"STILL PHOTO","voiceover":"And here is a still image.",
              "asset":"photo.png"}]}
        p=root/"brief.json";p.write_text(json.dumps(data));return p

    def create_media(self,root):
        render.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
           "-f","lavfi","-i","testsrc2=size=320x180:rate=30",
           "-t","1.6","-an","-c:v","libx264","-pix_fmt","yuv420p",
           root/"clip.mp4"])
        Image.new("RGB",(640,360),(220,75,105)).save(root/"photo.png")

    def test_declaration_required_before_using_footage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.create_media(root)
            brief=self.make_brief(root,rights="unknown")
            with self.assertRaisesRegex(ValueError,"media_rights"):
                render.parse_brief(brief)

    def test_video_requires_pop_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.create_media(root)
            brief=self.make_brief(root)
            with self.assertRaisesRegex(ValueError,"--pop"):
                render.render(brief,root/"output.mp4","espeak",None,"en-us",
                              320,568,25,quality="preview",pop=False)

    def test_mixed_video_photo_renders_with_narration_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.create_media(root)
            brief=self.make_brief(root)
            output=root/"output.mp4"
            result=render.render(brief,output,"espeak",None,"en-us",
                320,568,25,quality="preview",pop=True)
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size,22000)
            self.assertEqual(result["scenes"],2)
            self.assertGreater(result["duration_seconds"],3)
            codecs=render.run(["ffprobe","-v","error",
                "-show_entries","stream=codec_name,codec_type",
                "-of","csv=p=0",output]).stdout
            self.assertIn("h264",codecs)
            self.assertIn("aac",codecs)

if __name__=="__main__":unittest.main()
