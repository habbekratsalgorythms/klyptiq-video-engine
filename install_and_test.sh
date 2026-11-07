#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Installing free Klyptiq local video dependencies..."
sudo apt-get update
sudo apt-get install -y ffmpeg espeak curl python3-venv python3-pip fonts-dejavu-core
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
echo "Core tests passed. Preparing local editorial imagery..."
if ! bash scripts/prepare_editorial_media.sh; then
  echo "WARNING: Could not prepare editorial imagery. No video produced." >&2
  echo "Retry later with: bash scripts/prepare_editorial_media.sh" >&2
  exit 1
fi
if bash scripts/setup_kokoro.sh; then
  echo "Using preferred expressive local Kokoro gaming voice..."
  . .venv/bin/activate
  python render.py briefs/energetic-story-kokoro.json \
    --tts kokoro --model models/kokoro-v1.0.fp16.onnx \
    --voice am_puck --pace 1.12 --motion --quality production \
    -o output/Klyptiq_Kokoro_review_1080p.mp4
  echo "Unpublished 1080p review MP4: $PWD/output/Klyptiq_Kokoro_review_1080p.mp4"
elif bash scripts/setup_piper.sh; then
  echo "WARNING: Kokoro unavailable. Rendering fallback Piper review, NOT an approved production voice." >&2
  . .venv/bin/activate
  python render.py briefs/visual-demo.json --tts piper \
    --model models/en_US-kristin-medium.onnx --motion --quality production \
    -o output/Klyptiq_Piper_fallback_1080p.mp4
else
  echo "ERROR: No local neural voice available. Tests passed; no video was produced." >&2
  exit 1
fi
echo "Only review videos were created. Never publish automatically until voice/content approval."
