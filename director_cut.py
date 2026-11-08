"""Footage-first, original-SFX director mode for Klyptiq review shorts.

Unlike the older five-card slideshow, this mode REQUIRES a shot list with
multiple distinct cleared media sources per narrated scene. No media scraping,
new paid generation, automatic uploads or claims of game-play ownership.
"""
from __future__ import annotations
import math
import random
import subprocess
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RIGHTS = {"self_recorded", "licensed", "permission_documented"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm"}

def run(cmd):
    return subprocess.run([str(x) for x in cmd], check=True, capture_output=True, text=True)

def prepare(brief, brief_path):
    """Fail closed: per-shot rights, multiple sources and real moving footage."""
    total = moving = 0
    roots = set()
    for scene in brief["scenes"]:
        shots = scene.get("shots")
        if not isinstance(shots, list) or not 2 <= len(shots) <= 6:
            raise ValueError("Director mode requires 2-6 planned shots per scene")
        distinct = set()
        for shot in shots:
            if not isinstance(shot, dict):
                raise ValueError("Each director shot must be an object")
            is_video = bool(shot.get("asset_video"))
            is_photo = bool(shot.get("asset"))
            if is_video == is_photo:
                raise ValueError("Each director shot must choose exactly one image or video")
            if shot.get("media_rights") not in RIGHTS:
                raise ValueError("Each director shot needs explicit media_rights")
            key = "asset_video" if is_video else "asset"
            src = (Path(brief_path).resolve().parent / shot[key]).resolve()
            if not src.is_file():
                raise FileNotFoundError("Director shot missing licensed source: " + str(src))
            if is_video:
                if src.suffix.lower() not in VIDEO_SUFFIXES:
                    raise ValueError("Unsupported director video extension")
                probe = run(["ffprobe","-v","error","-select_streams","v:0",
                             "-show_entries","stream=codec_type",
                             "-of","csv=p=0",src]).stdout.strip()
                if probe != "video":
                    raise ValueError("Director footage has no video stream")
                moving += 1
            else:
                try:
                    with Image.open(src) as img: img.verify()
                except Exception as exc:
                    raise ValueError("Unusable director photograph") from exc
            start = shot.get("start", 0)
            if isinstance(start, bool) or not isinstance(start, (float, int)) or not math.isfinite(start) or not 0 <= start <= 120:
                raise ValueError("Director start must be 0-120 finite seconds")
            if shot.get("text") and (not isinstance(shot["text"], str) or len(shot["text"]) > 50):
                raise ValueError("Shot text must contain 50 characters or fewer")
            shot["_source"] = str(src)
            shot["_moving"] = is_video
            distinct.add(str(src))
            roots.add(str(src))
            total += 1
        if len(distinct) < 2:
            raise ValueError("Director scenes require at least TWO different approved media sources")
    if moving * 3 < 2 * total:
        raise ValueError("Director mode requires real rights-cleared video for at least two thirds of shots; no slideshow fallback")
    if len(roots) < 3:
        raise ValueError("Director mode needs visual variety: at least three distinct media sources")
    return {"shots": total, "moving_shots": moving, "media_sources": len(roots)}

def face(size, bold=True):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, max(12, size))

def wrap(d, text, f, width):
    lines = []; line = ""
    for word in text.split():
        test = (line + " " + word).strip()
        if line and d.textbbox((0,0), test, font=f)[2] > width:
            lines.append(line); line = word
        else:
            line = test
    if line: lines.append(line)
    return lines

def text_for_shot(scene, idx):
    shot = scene["shots"][idx]
    if shot.get("text"): return shot["text"]
    words = scene["caption"].split()
    slots = len(scene["shots"])
    start = int(len(words) * idx / slots)
    stop = int(len(words) * (idx+1) / slots)
    chunk = words[start:stop]
    return " ".join(chunk or words[-min(3,len(words)):])

def overlay_file(path, w, h, caption, progress, first=False):
    """Real media remains edge-to-edge; no giant fixed slide heading or frame."""
    im = Image.new("RGBA", (w,h), (0,0,0,0))
    d = ImageDraw.Draw(im)
    # Soft transparent fade behind captions rather than the slideshow's huge black card.
    for y in range(int(h*.67), int(h*.91)):
        alpha = int(154 * ((y/h-.67)/.24))
        d.line((0,y,w,y), fill=(4,10,20,max(0,min(154,alpha))))
    d.rounded_rectangle((int(w*.047),int(h*.05),int(w*.265),int(h*.082)),
                        radius=int(w*.01), fill=(0,12,23,205))
    d.text((int(w*.061),int(h*.055)), "KLYPTIQ", font=face(int(w*.028)), fill=(135,249,225,255))
    f = face(int(w*.08))
    message = caption.upper()
    while f.size > 18 and len(wrap(d,message,f,int(w*.89))) > 3:
        f = face(f.size-2)
    lines = wrap(d,message,f,int(w*.89))[:3]
    yy = int(h*.79) - (len(lines)-1)*int(f.size*1.1)
    for ln in lines:
        bb = d.textbbox((0,0),ln,font=f,stroke_width=2)
        x = max(12,(w-(bb[2]-bb[0]))//2)
        highlight = (250,228,91,255) if first else (255,255,255,255)
        d.text((x,yy),ln,font=f,fill=highlight,stroke_width=max(2,int(w*.004)),stroke_fill=(4,9,18,255))
        yy += int(f.size*1.18)
    # Thin progress line makes shot changes visible without huge numbering cards.
    d.rectangle((0,h-int(h*.008),int(w*progress),h),fill=(100,245,228,245))
    im.save(path)

def original_cut_sfx(path, positions, total):
    """Tiny synthetic impacts. No sound samples, commercial music or assets."""
    sr = 22050
    samples = [0] * max(1, int(total*sr))
    rng = random.Random(64)
    for position in positions:
        offset = round(position*sr)
        width = int(sr*.105)
        for i in range(width):
            ix = offset+i
            if ix >= len(samples): break
            t = i/sr
            envelope = max(0,1-i/width)**2
            bass = math.sin(2*math.pi*(95-40*i/width)*t)
            noise = (rng.random()*2-1)*.25
            samples[ix] += int((bass*.65+noise)*3800*envelope)
    with wave.open(str(path),"wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        import array
        f.writeframes(array.array("h",(max(-32768,min(32767,x)) for x in samples)).tobytes())

def render_director(work, brief, scenes, durations, w, h, crf, wav, total_length, target):
    """Cut every 0.5-2.1 s, mix original micro-impacts under the voice."""
    clips = []
    cut_positions = []
    at = 0.0
    total_shots = sum(len(s["shots"]) for s in scenes)
    shot_n = 0
    for i,(scene,seconds) in enumerate(zip(scenes,durations)):
        shots = scene["shots"]
        per = seconds / len(shots)
        if per > 2.1 or per < .5:
            raise ValueError("Director footage-first rhythm needs 0.5-2.1 s per shot; adjust shot count and/or script")
        for j,shot in enumerate(shots):
            seconds_this = per if j < len(shots)-1 else seconds - per*(len(shots)-1)
            if shot_n:
                cut_positions.append(at)
            png = work / f"director_overlay_{shot_n:03}.png"
            clip = work / f"director_clip_{shot_n:03}.mp4"
            overlay_file(png,w,h,text_for_shot(scene,j),(shot_n+1)/total_shots, first=shot_n==0)
            src = shot["_source"]
            inputs = []
            if shot["_moving"]:
                # Original clip audio intentionally dropped: no game music or voices.
                inputs = ["-stream_loop","-1","-ss",str(shot.get("start",0)),"-i",src]
                framing = shot.get("framing","center")
                if framing not in ("left","center","right"):
                    raise ValueError("Director framing must be left, center or right")
                x = {"left":"0","center":"(iw-ow)/2","right":"iw-ow"}[framing]
                picture = (f"[0:v]fps=30,scale={w}:{h}:force_original_aspect_ratio=increase,"
                           f"crop={w}:{h}:{x}:(ih-oh)/2,setsar=1[media];")
            else:
                inputs = ["-loop","1","-framerate","30","-i",src]
                picture = (f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,"
                           f"zoompan=z='min(1.14,zoom+0.002)':"
                           f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
                           f"d=1:s={w}x{h}:fps=30,setsar=1[media];")
            graph = picture + "[media][1:v]overlay=0:0:shortest=1,format=yuv420p[v]"
            run(["ffmpeg","-hide_banner","-loglevel","error","-y",*inputs,
                 "-loop","1","-framerate","30","-i",png,
                 "-filter_complex",graph,"-map","[v]","-an",
                 "-t",f"{seconds_this:.5f}","-r","30",
                 "-c:v","libx264","-preset","veryfast",
                 "-crf",str(crf),"-pix_fmt","yuv420p",clip])
            clips.append(clip)
            shot_n += 1
            at += seconds_this
    manifest = work / "director_manifest.txt"
    manifest.write_text("".join(f"file '{p}'\n" for p in clips))
    fx = work / "original_fx.wav"
    original_cut_sfx(fx,cut_positions,total_length)
    run(["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-safe","0","-f","concat","-i",manifest,"-i",wav,"-i",fx,
         "-filter_complex",
         "[2:a]volume=0.35[fx];[1:a][fx]amix=inputs=2:duration=first:normalize=0,"
         "loudnorm=I=-16:TP=-1.5:LRA=7[a]",
         "-map","0:v:0","-map","[a]","-c:v","copy","-c:a","aac",
         "-b:a","192k","-movflags","+faststart","-t",str(total_length),target])
    return {"shot_count":shot_n,"cuts":len(cut_positions),
            "source_audio_used":False,"original_sound_cues":len(cut_positions)}
