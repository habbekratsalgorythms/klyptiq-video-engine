#!/usr/bin/env python3
"""Acquire ONLY selected short excerpts of Rockstar's official 2026 launch trailer.

Internal, non-commercial video-editing review. The downloaded media is NOT
licensed for commercial Klyptiq distribution and never enters git.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

URL="https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4"
EXPECTED_BYTES=781757793
TIMES=(8,16,25,34,45,58,76)

def execute(*cmd):
    return subprocess.run([str(x) for x in cmd],check=True,capture_output=True,text=True)

def acquire(dest:Path,internal_review_only:bool):
    if not internal_review_only:
        raise ValueError("Explicit --internal-review-only is required")
    dest.mkdir(parents=True,exist_ok=True)
    # HEAD must match the already independently inspected official media URL.
    headers=execute("curl","-sfLI","--retry","2","--max-time","30",URL).stdout.lower()
    if "content-type: video/mp4" not in headers or "accept-ranges: bytes" not in headers:
        raise ValueError("Official trailer no longer supplies expected seekable MP4")
    if f"content-length: {EXPECTED_BYTES}" not in headers:
        raise ValueError("Official trailer has changed: inspect before extracting")
    duration=float(execute("ffprobe","-v","error","-rw_timeout","18000000",
        "-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",URL).stdout.strip())
    if not 89 < duration < 90:
        raise ValueError(f"Unexpected trailer duration: {duration}")
    items=[]
    for sec in TIMES:
        path=dest/f"launch_{sec:02d}.mp4"
        # Seeking before remote input uses HTTP byte ranges; only ~2.3 seconds decoded.
        execute("ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
            "-rw_timeout","18000000","-ss",str(sec),"-i",URL,
            "-t","2.25","-an","-vf","scale=960:-2,fps=30",
            "-c:v","libx264","-preset","veryfast","-crf","24",
            "-pix_fmt","yuv420p","-movflags","+faststart",path)
        secs=float(execute("ffprobe","-v","error","-show_entries","format=duration",
             "-of","default=noprint_wrappers=1:nokey=1",path).stdout.strip())
        if not 1.75 < secs < 2.5 or path.stat().st_size < 40000:
            raise ValueError(f"Remote trailer excerpt {sec}s failed integrity check")
        items.append({"file":path.name,"source_time_seconds":sec,"duration":round(secs,3),
            "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "usage":"internal_editorial_review_only",
            "commercial_rights":"NOT_ESTABLISHED"})
        print("REMOTE OFFICIAL EXCERPT:",sec,"seconds; local duration",round(secs,2),flush=True)
    (dest/"launch-excerpts-manifest.json").write_text(json.dumps({
      "source":URL,"asserted_source_content_length":EXPECTED_BYTES,
      "distribution":"INTERNAL_REVIEW_ONLY","no_automatic_social_upload":True,
      "files":items},indent=2))
    return items

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="assets/rockstar_review")
    p.add_argument("--internal-review-only",action="store_true")
    a=p.parse_args()
    acquire(Path(a.output),a.internal_review_only)
