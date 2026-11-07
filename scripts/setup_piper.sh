#!/usr/bin/env bash
# Optional, free local Piper voice setup. No cloud API or paid subscription.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v curl >/dev/null || { echo "ERROR: curl is required" >&2; exit 1; }
command -v sha256sum >/dev/null || { echo "ERROR: sha256sum is required" >&2; exit 1; }
test -x .venv/bin/python || { echo "Run bash install_and_test.sh first" >&2; exit 1; }
source .venv/bin/activate
python -m pip install "piper-tts"
mkdir -p models
model=models/en_US-kristin-medium.onnx
url="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kristin/medium"
sha="5849957f929cbf720c258f8458692d6103fff2f0e3d3b19c8259474bb06a18d4"
if [ -f "$model" ] && echo "$sha  $model" | sha256sum -c --status; then
  echo "Verified existing model."
else
  curl --fail --location --retry 3 --connect-timeout 20 "$url/en_US-kristin-medium.onnx" -o "$model.partial"
  echo "$sha  $model.partial" | sha256sum -c
  mv "$model.partial" "$model"
fi
curl --fail --location --retry 3 "$url/en_US-kristin-medium.onnx.json" -o "$model.json.partial"
echo "70bc97d350c796c64ea5e4d08241afac  $model.json.partial" | md5sum -c
mv "$model.json.partial" "$model.json"
curl --fail --location --retry 3 "$url/MODEL_CARD" -o models/en_US-kristin-medium.MODEL_CARD
python - <<'PY'
import json
from pathlib import Path
p=Path("models/en_US-kristin-medium.onnx.json")
config=json.loads(p.read_text())
assert config["audio"]["sample_rate"] == 22050
print("Piper configuration validated.")
PY
echo "Installed a free local Piper model with public-domain source recordings."
echo "Review models/en_US-kristin-medium.MODEL_CARD before monetized publication."
echo "Try:"
echo "  . .venv/bin/activate"
echo "  python render.py briefs/visual-demo.json --tts piper --model models/en_US-kristin-medium.onnx -o output/klyptiq-piper-preview.mp4"
