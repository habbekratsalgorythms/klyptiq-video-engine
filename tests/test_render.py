import json,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
import render
class Tests(unittest.TestCase):
    def test_opaque_image(self):
        with tempfile.TemporaryDirectory() as td:
            im=Image.new("RGB",(640,360),(255,80,40));src=Path(td)/"source.png";im.save(src)
            dst=Path(td)/"slide.png"
            render.make_slide(dst,360,640,"TEST TITLE","READABLE CAPTION",str(src),"news","TEST LABEL")
            rgb=Image.open(dst).convert("RGB");c=rgb.getpixel((180,315))
            self.assertGreater(c[0],210);self.assertLess(c[2],100)
    def test_missing_asset(self):
        with tempfile.TemporaryDirectory() as td:
            x=Path(td)/"b.json";x.write_text(json.dumps({"title":"a","script":"hello","scenes":[{"caption":"one","asset":"not_found.png"},{"caption":"two"}]}))
            with self.assertRaises(FileNotFoundError):render.parse_brief(x)
    def test_invalid_scene(self):
        with tempfile.TemporaryDirectory() as td:
            x=Path(td)/"b.json";x.write_text(json.dumps({"title":"a","script":"hello","scenes":[{"caption":"one"},{}]}))
            with self.assertRaises(ValueError):render.parse_brief(x)
if __name__=="__main__": unittest.main()
