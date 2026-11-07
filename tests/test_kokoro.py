"""No paid models needed for unit tests: mock the local Kokoro runtime."""
import json
import tempfile
import unittest
import types
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import render

class KokoroTests(unittest.TestCase):
    def test_reject_unsafe_pace(self):
        with tempfile.TemporaryDirectory() as td:
            b=Path(td)/"b.json"
            b.write_text(json.dumps({
                "title":"Gaming","script":"Hello there!",
                "scenes":[{"caption":"one","voiceover":"One!","pace":1.85},
                          {"caption":"two","voiceover":"Two!"}]}))
            with self.assertRaisesRegex(ValueError,"pace"):
                render.parse_brief(b)

    def test_reuses_model_and_passes_voice_and_speed(self):
        constructed=[]
        called=[]
        class FakeKokoro:
            def __init__(self,model,voices):
                constructed.append((model,voices))
            def create(self,text,voice,speed,lang):
                called.append((text,voice,speed,lang))
                return [0.1]*1600, 16000
        sf=types.ModuleType("soundfile")
        sf.write=lambda path,samples,sr,subtype:Path(path).write_bytes(b"fake")
        module=types.ModuleType("kokoro_onnx")
        module.Kokoro=FakeKokoro
        with tempfile.TemporaryDirectory() as td:
            model=Path(td)/"test.onnx";model.write_bytes(b"fake")
            (Path(td)/"voices-v1.0.bin").write_bytes(b"fake")
            render._KOKORO_CACHE.clear()
            with patch.dict(sys.modules,{"kokoro_onnx":module,"soundfile":sf}):
                render.speak("First line",str(Path(td)/"a.wav"),"kokoro",str(model),"am_puck",1.12)
                render.speak("Second line",str(Path(td)/"b.wav"),"kokoro",str(model),"am_puck",1.07)
            self.assertEqual(len(constructed),1)
            self.assertEqual([x[2] for x in called],[1.12,1.07])
            self.assertTrue((Path(td)/"a.wav").exists())

    def test_production_allows_neural_kokoro(self):
        # Missing brief is reached ONLY if the neural production guard passes.
        with self.assertRaises(FileNotFoundError):
            render.render("/does-not-exist.json","/tmp/out.mp4",
                "kokoro",None,"am_puck",1080,1920,20,
                "production",False,1.1)

if __name__=="__main__":
    unittest.main()
