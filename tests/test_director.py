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
                    {"asset_video":"v2.mp4","media_rights":"self_recorded","text":"FAST HOOK"}]},
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
            self.assertEqual(director_cut.prepare(data,p)["moving_shots"],3)
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

    def test_duo_rejects_uncleared_secondary_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            data=render.parse_brief(p)
            pair=data["scenes"][0]["shots"][0]
            pair["layout"]="stacked"
            pair["secondary_asset_video"]="v2.mp4"
            with self.assertRaisesRegex(ValueError,"second media rights"):
                director_cut.prepare(data,p)
            pair["secondary_media_rights"]="editorial_review_only"
            with self.assertRaisesRegex(ValueError,"Unlicensed second video"):
                director_cut.prepare(data,p)
            data["distribution"]="internal_review"
            self.assertEqual(director_cut.prepare(data,p)["media_sources"],3)

    def test_duo_overlay_has_center_divider_and_clear_faces(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"duo.png"
            director_cut.overlay_file(p,320,568,"PICK ONE",.5,pair_label="OR")
            im=Image.open(p).convert("RGBA")
            self.assertGreater(im.getpixel((160,284))[3],0)
            self.assertEqual(im.getpixel((160,190))[3],0)
            self.assertGreater(im.getpixel((160,440))[3],0)

    def test_v3_brief_is_noncommercial_and_has_real_comparison_layouts(self):
        p=Path(__file__).resolve().parents[1]/"briefs/review/six-more-faces-story-v3.json"
        data=json.loads(p.read_text())
        self.assertEqual(data["distribution"],"internal_review")
        self.assertEqual(data["script"]," ".join(s["voiceover"] for s in data["scenes"]))
        shots=[x for scene in data["scenes"] for x in scene["shots"]]
        self.assertGreaterEqual(len(shots),18)
        duos=[x for x in shots if x.get("layout")=="stacked"]
        self.assertGreaterEqual(len(duos),4)
        self.assertTrue(all(x["secondary_media_rights"]=="editorial_review_only" for x in duos))
        self.assertTrue(all(x["asset_video"].endswith(".mp4") for x in shots))
        for shot in shots:
            if "Cover_Art" in shot["asset_video"]:
                self.assertGreaterEqual(shot.get("start",0),7.0)

    def test_four_edited_shots_with_original_sfx(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            # First synthetic shot uses two simultaneous, independently sourced clips.
            raw=json.loads(p.read_text())
            first=raw["scenes"][0]["shots"][0]
            first.update({"layout":"stacked","secondary_asset_video":"v2.mp4",
                          "secondary_media_rights":"self_recorded","pair_label":"AND"})
            p.write_text(json.dumps(raw))
            output=root/"director.mp4"
            result=render.render(p,output,"espeak",None,"en-us",
                                 320,568,27,quality="preview",director=True)
            self.assertEqual(result["shot_count"],4)
            self.assertEqual(result["cuts"],3)
            self.assertEqual(result["moving_shots"],3)
            self.assertFalse(result["source_audio_used"])
            self.assertTrue(output.stat().st_size>15000)
            info=render.run(["ffprobe","-v","error","-show_entries",
                             "stream=codec_name,codec_type","-of","csv=p=0",output]).stdout
            self.assertIn("h264",info)
            self.assertIn("aac",info)
            # First shot is visibly top+bottom moving sources, not the old single panel.
            import io,subprocess
            captured=subprocess.run(["ffmpeg","-v","error","-ss","0.35","-i",str(output),
                "-frames:v","1","-f","image2pipe","-vcodec","png","pipe:1"],
                check=True,capture_output=True).stdout
            image=Image.open(io.BytesIO(captured)).convert("RGB")
            self.assertEqual(image.size,(320,568))
            self.assertNotEqual(image.getpixel((160,125)),image.getpixel((160,408)))

    def test_editorial_sources_must_stay_internal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            data=render.parse_brief(p)
            data["scenes"][0]["shots"][0]["media_rights"]="editorial_review_only"
            with self.assertRaisesRegex(ValueError,"internal_review"):
                director_cut.prepare(data,p)
            data["distribution"]="internal_review"
            self.assertEqual(director_cut.prepare(data,p)["moving_shots"],3)

    def test_no_looping_short_character_clips_or_bad_start_offsets(self):
        self.assertAlmostEqual(director_cut.stretch_for_shot(1.0,0,1.3),1.3)
        self.assertEqual(director_cut.stretch_for_shot(1.5,0,.9),1.0)
        with self.assertRaisesRegex(ValueError,"too much slow-motion"):
            director_cut.stretch_for_shot(1.0,0,2.2)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.media(root);p=self.brief(root)
            data=render.parse_brief(p)
            data["scenes"][0]["shots"][0]["start"]=1.95
            with self.assertRaisesRegex(ValueError,"start offset"):
                director_cut.prepare(data,p)

    def test_real_source_preview_never_starts_on_rating_card(self):
        p=Path(__file__).resolve().parents[1]/"briefs/review/eight-faces-director.json"
        data=json.loads(p.read_text())
        for scene in data["scenes"]:
            for shot in scene["shots"]:
                if "Cover_Art" in shot.get("asset_video",""):
                    self.assertGreaterEqual(shot.get("start",0),7.0)
                if shot.get("text") in ("LUCIA CAMINOS","JASON DUVAL","TEAM LUCIA?","TEAM JASON?"):
                    self.assertEqual(shot.get("framing"),"center")

    def test_original_music_is_audible_and_is_not_external_audio(self):
        import wave
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"music.wav"
            director_cut.original_music_bed(p,4.0,bpm=142)
            with wave.open(str(p)) as w:
                self.assertEqual(w.getnchannels(),1)
                self.assertEqual(w.getframerate(),22050)
                self.assertGreater(w.getnframes(),85000)
                raw=w.readframes(w.getnframes())
            import array
            samples=array.array("h");samples.frombytes(raw)
            self.assertGreater(max(samples),200)
            self.assertLess(min(samples),-200)

    def test_editorial_storyboard_no_slideshow_fallback(self):
        p=Path(__file__).resolve().parents[1]/"briefs/review/eight-faces-director.json"
        data=json.loads(p.read_text())
        self.assertEqual(data["distribution"],"internal_review")
        self.assertEqual(data["source_url"],"https://www.rockstargames.com/VI/media/videos")
        self.assertEqual(data["script"]," ".join(s["voiceover"] for s in data["scenes"]))
        shots=[x for scene in data["scenes"] for x in scene["shots"]]
        self.assertGreaterEqual(len(shots),16)
        self.assertTrue(all(x["media_rights"]=="editorial_review_only" for x in shots))
        self.assertTrue(all(x.get("asset_video","").endswith(".mp4") for x in shots))
        self.assertGreaterEqual(len({x["asset_video"] for x in shots}),9)
        self.assertTrue(all(len(s["shots"])>=3 for s in data["scenes"]))

if __name__=="__main__":
    unittest.main()
