#!/usr/bin/env python3
"""Extract ONLY the nine official GTA VI clips from a SHA256-pinned Rockstar archive.

For local noncommercial editorial evaluation, NOT for paid content or redistribution.
No download in this program; CI obtains the ZIP exclusively from the Rockstar CDN.
Never check extracted footage into Git.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

SOURCE_URL="https://media.rockstargames.com/VI/downloads/videos/GTAVI_Videos.zip"
KNOWN_SHA256="017b806729ae09d54180e9c83c31ef201ff4288751186f20d11ea2c513de7698"
EXPECTED={
    "GTAVI_Official_Cover_Art_Landscape.mp4",
    "Jason_Duval_Video_Clip.mp4",
    "Lucia_Caminos_Video_Clip.mp4",
    "Cal_Hampton_Video_Clip.mp4",
    "Boobie_Ike_Video_Clip.mp4",
    "DreQuan_Priest_Video_Clip.mp4",
    "Real_Dimez_Video_Clip.mp4",
    "Raul_Bautista_Video_Clip.mp4",
    "Brian_Heder_Video_Clip.mp4",
}

def extract(archive, dest, license_ack=False):
    if not license_ack:
        raise ValueError("Explicit --internal-review-only flag is required: no commercial rights established")
    archive=Path(archive)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest!=KNOWN_SHA256:
        raise ValueError("Official source archive changed; independently re-verify before use")
    dest=Path(dest)
    dest.mkdir(parents=True,exist_ok=True)
    manifest=[]
    with zipfile.ZipFile(archive) as z:
        entries={x.filename: x for x in z.infolist() if not x.is_dir()}
        if set(entries)!=EXPECTED:
            raise ValueError("Archive members have changed; fail closed rather than extracting unexpected content")
        if sum(x.file_size for x in entries.values())>160_000_000:
            raise ValueError("Unexpected uncompressed archive size")
        for name in sorted(EXPECTED):
            info=entries[name]
            if info.file_size>50_000_000 or info.file_size<500_000:
                raise ValueError("Implausible official video size: "+name)
            out=dest/name
            with z.open(info) as src,open(out,"wb") as fd:
                shutil.copyfileobj(src,fd)
            check=subprocess.run(["ffprobe","-v","error","-show_entries",
                                  "stream=codec_type,width,height:format=duration",
                                  "-of","json",str(out)],text=True,capture_output=True,check=True)
            data=json.loads(check.stdout)
            videos=[s for s in data["streams"] if s["codec_type"]=="video"]
            if len(videos)<1 or float(data["format"]["duration"])<0.8:
                raise ValueError("Bad official video stream: "+name)
            manifest.append({"file":name,"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
                             "duration":round(float(data["format"]["duration"]),2),
                             "width":videos[0].get("width"),
                             "height":videos[0].get("height"),
                             "source":SOURCE_URL,
                             "usage":"internal_review_only",
                             "commercial_license":"NOT_ESTABLISHED"})
    (dest/"editorial_manifest.json").write_text(json.dumps({
        "archive_source":SOURCE_URL,
        "archive_sha256":KNOWN_SHA256,
        "distribution":"internal_review_only",
        "commercial_rights":"UNVERIFIED — DO NOT MONETIZE OR AUTOPOST",
        "files":manifest
    },indent=2))
    print("Prepared",len(manifest),"official short-video assets. Local internal review only.")
    return manifest

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",default="assets/rockstar_review")
    p.add_argument("--internal-review-only",action="store_true")
    a=p.parse_args()
    extract(a.archive,a.output,a.internal_review_only)

if __name__=="__main__":main()
