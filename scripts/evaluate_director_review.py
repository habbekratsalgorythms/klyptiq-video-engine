#!/usr/bin/env python3
"""Independent mechanical QC and contact sheet for one Klyptiq director edit.

No external AI calls. Measured stream + movement properties are not a claim
that an edit is creatively engaging or has commercial reuse rights.
"""
import argparse
import io
import json
import math
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat

def call(args):
    return subprocess.run([str(x) for x in args],capture_output=True,check=True)

def probe(path):
    return json.loads(call(["ffprobe","-v","error","-show_format","-show_streams","-of","json",path]).stdout)

def frame_at(path, seconds, width=270):
    got=call(["ffmpeg","-hide_banner","-loglevel","error","-ss",f"{seconds:.3f}",
              "-i",path,"-frames:v","1","-vf",f"scale={width}:-1",
              "-f","image2pipe","-vcodec","mjpeg","pipe:1"]).stdout
    return Image.open(io.BytesIO(got)).convert("RGB")

def perceptual_signature(img):
    small=img.convert("L").resize((24,24))
    vals=list(small.getdata())
    mean=sum(vals)/len(vals)
    return "".join("1" if v>mean else "0" for v in vals)

def evaluate(path,sheet_path,summary_path):
    src=Path(path)
    if not src.is_file(): raise ValueError("Finished video is missing")
    p=probe(src)
    video=next(s for s in p["streams"] if s["codec_type"]=="video")
    audio=next(s for s in p["streams"] if s["codec_type"]=="audio")
    duration=float(p["format"]["duration"])
    assert video.get("codec_name")=="h264",video
    assert audio.get("codec_name")=="aac",audio
    assert (int(video["width"]),int(video["height"]))==(1080,1920)
    if not (12<=duration<=36):
        raise ValueError(f"Unusual director review runtime: {duration}")
    samples=[duration*(.025+i*.95/8) for i in range(9)]
    frames=[frame_at(src,min(duration-.05,x)) for x in samples]
    sigs=[perceptual_signature(x) for x in frames]
    distinct=len(set(sigs))
    if distinct<6:
        raise ValueError("Too little visual variety across contact frames")
    light=[ImageStat.Stat(x.convert("L")).mean[0] for x in frames]
    if sum(light)/len(light)<18:
        raise ValueError("Video is mostly black")
    # Measure within-shot movement, excluding early video overlays/caption changes.
    motion=[]
    for t in (duration*.08,duration*.22,duration*.35,duration*.51,duration*.69,duration*.83):
        a=frame_at(src,t,96).convert("L")
        b=frame_at(src,min(duration-.05,t+.16),96).convert("L")
        difference=ImageStat.Stat(ImageChops.difference(a,b)).mean[0]
        motion.append(round(difference,2))
    if sum(x>1.0 for x in motion)<2:
        raise ValueError("Not enough actually moving visual moments")
    detect=call(["ffmpeg","-hide_banner","-i",src,"-vn","-af","volumedetect",
                 "-f","null","-"]).stderr.decode("utf8","replace")
    match=re.search(r"mean_volume:\s*(-?[0-9.]+) dB",detect)
    if not match or float(match.group(1))<-32:
        raise ValueError("Narration/music mix is inaudible")
    # Review contact sheet: nine proportional frames labeled with video timestamp.
    w,h=270,480
    canvas=Image.new("RGB",(3*w,3*(h+36)),(13,18,29))
    draw=ImageDraw.Draw(canvas)
    font_file="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font=ImageFont.truetype(font_file,20)
    for i,(image,time) in enumerate(zip(frames,samples)):
        col,row=i%3,i//3
        x,y=col*w,row*(h+36)
        frame=Image.new("RGB",(w,h),(12,16,28))
        factor=min(w/image.width,h/image.height)
        resized=image.resize((max(1,round(image.width*factor)),max(1,round(image.height*factor))))
        frame.paste(resized,((w-resized.width)//2,(h-resized.height)//2))
        canvas.paste(frame,(x,y))
        draw.text((x+12,y+h+6),f"{time:04.1f} SEC",font=font,fill=(140,236,221))
    Path(sheet_path).parent.mkdir(parents=True,exist_ok=True)
    canvas.save(sheet_path,quality=90)
    report={
        "video":src.name,"duration_seconds":round(duration,2),
        "resolution":"1080x1920","codec_video":"h264","codec_audio":"aac",
        "contact_sample_count":len(frames),
        "distinct_sample_signatures":distinct,
        "avg_luminance":round(sum(light)/len(light),2),
        "motion_samples_mean_absolute_delta":motion,
        "audio_mean_db":float(match.group(1)),
        "editing_quality":"NOT AUTOMATICALLY PROVEN — HUMAN REVIEW REQUIRED",
        "copyright":"THIRD-PARTY ROCKSTAR SOURCE — NOT CLEARED FOR MONETIZATION",
        "distribution":"INTERNAL REVIEW ONLY"
    }
    Path(summary_path).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--summary",required=True)
    parser.add_argument("--contact-sheet",required=True)
    args=parser.parse_args()
    evaluate(args.video,args.contact_sheet,args.summary)
