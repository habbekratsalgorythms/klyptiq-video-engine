#!/usr/bin/env python3
"""Offline Klyptiq 9:16 short-video renderer. No external APIs or publishing."""
from __future__ import annotations
import argparse, json, math, os, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ROOT=Path(__file__).resolve().parent
COLORS={"news":(17,24,41),"analysis":(12,28,27),"countdown":(38,23,40)}

def run(cmd,**kw):
    return subprocess.run([str(c) for c in cmd],check=True,capture_output=True,text=True,**kw)

def font(size,bold=False):
    names=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for name in names:
        if Path(name).exists(): return ImageFont.truetype(name,size)
    return ImageFont.load_default()

def wrap(draw,text,face,limit):
    lines=[]; current=""
    for word in text.split():
        trial=(current+" "+word).strip()
        if current and draw.textbbox((0,0),trial,font=face,stroke_width=0)[2]>limit:
            lines.append(current); current=word
        else: current=trial
    if current: lines.append(current)
    return lines

def cover(im,size):
    w,h=size;scale=max(w/im.width,h/im.height)
    im=im.resize((math.ceil(im.width*scale),math.ceil(im.height*scale)),Image.Resampling.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width+w)//2,(im.height+h)//2))

def contain(im,size):
    w,h=size;scale=min(w/im.width,h/im.height)
    return im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.LANCZOS)

def background(w,h,source,style):
    bg=Image.new("RGB",(w,h),COLORS.get(style,COLORS["news"]))
    if source:
        photo=Image.open(source).convert("RGB")
        blurred=cover(photo,(w,h)).filter(ImageFilter.GaussianBlur(max(12,w//24)))
        bg.paste(ImageEnhance.Brightness(blurred).enhance(0.36),(0,0))
        # Fully opaque photo must be painted LAST and remain sharp.
        foreground=contain(photo,(w-64,int(h*.51)))
        bg.paste(foreground,((w-foreground.width)//2,(h-foreground.height)//2-38))
    return bg

def centered(draw,y,txt,face,color,w,stroke=0):
    bb=draw.textbbox((0,0),txt,font=face,stroke_width=stroke)
    draw.text(((w-(bb[2]-bb[0]))//2,y),txt,font=face,fill=color,stroke_width=stroke,stroke_fill=(0,0,0))

def make_slide(path,w,h,title,subtitle,source,style,label):
    im=background(w,h,source,style)
    panel=Image.new("RGBA",(w,int(h*.16)),(5,9,18,205))
    im.paste(panel,(0,0),panel);d=ImageDraw.Draw(im)
    centered(d,int(h*.025),label,font(int(w*.028),True),(125,239,220),w)
    title_font=font(int(w*.053),True)
    for idx,line in enumerate(wrap(d,title.upper(),title_font,w-92)[:3]):
        centered(d,int(h*.064)+idx*int(w*.066),line,title_font,(255,255,255),w,2)
    bottom=int(h*.765)
    panel=Image.new("RGBA",(w-64,int(h*.135)),(0,0,0,215))
    im.paste(panel,(32,bottom-12),panel);d=ImageDraw.Draw(im)
    sf=font(int(w*.047),True)
    for idx,line in enumerate(wrap(d,subtitle,sf,w-116)[:3]):
        centered(d,bottom+idx*int(w*.065),line,sf,(255,255,255),w,3)
    centered(d,int(h*.948),"KLYPTIQ GAMING  |  INDEPENDENT FAN COVERAGE",font(int(w*.021),True),(165,185,193),w)
    im.save(path)

def length(path):
    return float(run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path]).stdout.strip())

def speak(script,path,engine,model,voice):
    if engine=="piper":
        if not model or not Path(model).is_file(): raise ValueError("Specify existing --model /path/to/voice.onnx")
        subprocess.run(["piper","--model",model,"--output_file",path],input=script,text=True,check=True,capture_output=True)
    elif engine=="espeak":
        run(["espeak","-v",voice,"-s","145","-a","200","-w",path,script])
    else: raise ValueError("Unknown speech engine")

def parse_brief(path):
    brief=json.loads(Path(path).read_text(encoding="utf8"))
    for req in ("title","script","scenes"):
        if not brief.get(req): raise ValueError("Missing required value: "+req)
    scenes=brief["scenes"]
    if not 2<=len(scenes)<=16: raise ValueError("Must have 2–16 scenes")
    if len(brief["script"])>2200: raise ValueError("Script too long")
    for scene in scenes:
        if not scene.get("caption"): raise ValueError("Each scene needs caption")
        if scene.get("asset"):
            path_asset=(Path(path).resolve().parent/scene["asset"]).resolve()
            if not path_asset.is_file(): raise FileNotFoundError("Missing image asset: "+str(path_asset))
            scene["_asset"]=str(path_asset)
    return brief

def render(brief_path,out,engine,model,voice,width,height,crf):
    for name in ("ffmpeg","ffprobe",engine):
        if not shutil.which(name): raise RuntimeError("Missing required executable: "+name)
    brief=parse_brief(brief_path)
    out=Path(out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="klyptiq-") as tmp:
        work=Path(tmp);wav=work/"speech.wav"
        speak(brief["script"],str(wav),engine,model,voice)
        audio_length=length(wav)
        if not 3<=audio_length<=180: raise ValueError("Invalid audio duration")
        scenes=brief["scenes"]
        weights=[max(3,len(s["caption"].split())) for s in scenes]
        total_length=audio_length+0.6
        durations=[total_length*n/sum(weights) for n in weights]
        manifest=work/"frames.txt"
        with manifest.open("w") as f:
            for i,(scene,secs) in enumerate(zip(scenes,durations)):
                slide=work/f"scene{i:02d}.png"
                make_slide(slide,width,height,brief["title"],scene["caption"],scene.get("_asset"),brief.get("style","news"),brief.get("label","NEWS / ANALYSIS"))
                f.write(f"file '{slide}'\nduration {secs:.5f}\n")
            f.write(f"file '{slide}'\n")
        target=work/"video.mp4"
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",manifest,"-i",wav,"-vf",f"fps=30,scale={width}:{height}:flags=lanczos,format=yuv420p","-af","loudnorm=I=-16:TP=-1.5:LRA=7","-c:v","libx264","-preset","veryfast","-crf",str(crf),"-c:a","aac","-b:a","192k","-movflags","+faststart","-t",str(total_length),target])
        # Quality gates: a blank-background video or missing/quiet voice must fail, not publish.
        if not all(scene.get("_asset") for scene in scenes):
            raise ValueError("No finished videos without an approved image for every scene")
        measure=run(["ffmpeg","-hide_banner","-i",target,"-vn","-af","volumedetect","-f","null","-"]).stderr
        import re
        found=re.search(r"mean_volume:\\s*(-?[0-9.]+) dB",measure)
        if not found or float(found.group(1))<-33:
            raise RuntimeError("Voice too quiet or inaudible: loudness validation failed")
        os.replace(target,out)
        return {"video":str(out),"duration_seconds":round(length(out),2),"audio_seconds":round(audio_length,2),"resolution":f"{width}x{height}","scenes":len(scenes)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("brief");p.add_argument("-o","--output",default="output/klyptiq-short.mp4")
    p.add_argument("--tts",choices=["espeak","piper"],default="espeak");p.add_argument("--model");p.add_argument("--voice",default="en-us")
    p.add_argument("--width",type=int,default=1080);p.add_argument("--height",type=int,default=1920);p.add_argument("--crf",type=int,default=20)
    a=p.parse_args()
    if a.width<320 or a.height<568 or a.width%2 or a.height%2: p.error("Resolution must be even and at least 320x568")
    try:print(json.dumps(render(a.brief,a.output,a.tts,a.model,a.voice,a.width,a.height,a.crf),indent=2))
    except Exception as e:print(f"ERROR: {type(e).__name__}: {e}",file=sys.stderr);sys.exit(1)

if __name__=="__main__": main()
