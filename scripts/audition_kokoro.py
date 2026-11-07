#!/usr/bin/env python3
"""Audition three distinct ORIGINAL preset gaming narrator voices.

Does not clone or imitate any person's identity, or contact a paid service.
"""
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"/"voice-auditions"
OUT.mkdir(parents=True,exist_ok=True)
MODEL=ROOT/"models"/"kokoro-v1.0.fp16.onnx"
VOICES=ROOT/"models"/"voices-v1.0.bin"
tts=Kokoro(str(MODEL),str(VOICES))
script=(
  "GTA Six has a huge story twist right at the start! "
  "Jason and Lucia thought this would be an easy score. "
  "One mistake changes everything. "
  "Now they're caught in a criminal conspiracy across Leonida. "
  "Who would you play as first?"
)
for voice,pace in [("am_puck",1.12),("am_fenrir",1.10),("am_michael",1.15)]:
    audio,sample_rate=tts.create(script,voice=voice,speed=pace,lang="en-us")
    if len(audio)<sample_rate*5:
        raise RuntimeError(f"Suspiciously short speech generated for {voice}")
    output=OUT/f"{voice}.wav"
    sf.write(str(output),audio,sample_rate,subtype="PCM_16")
    print(f"{voice}: {len(audio)/sample_rate:.2f}s -> {output}")
print("Listen and choose the most natural energetic voice; no voice cloning performed.")
