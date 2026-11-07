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
echo "Core tests passed. Preparing natural voice and editorial preview..."
if bash scripts/setup_piper.sh && bash scripts/prepare_editorial_media.sh; then
  . .venv/bin/activate
  python render.py briefs/visual-demo.json --tts piper \
    --model models/en_US-kristin-medium.onnx --quality production \
    -o output/Klyptiq_Piper_review_1080p.mp4
  echo "Review-only MP4 created: $PWD/output/Klyptiq_Piper_review_1080p.mp4"
else
  echo "WARNING: Preview asset/voice download failed. Core tests passed."
  echo "Retry: bash scripts/setup_piper.sh && bash scripts/prepare_editorial_media.sh"
fi
echo "Never publish automatically until reviewed."
