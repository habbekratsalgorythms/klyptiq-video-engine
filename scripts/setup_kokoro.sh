#!/usr/bin/env bash
# Free local Kokoro-ONNX voice setup for Klyptiq. No API keys or paid plans.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v curl >/dev/null || { echo "ERROR: curl required" >&2; exit 1; }
command -v sha256sum >/dev/null || { echo "ERROR: sha256sum required" >&2; exit 1; }
test -x .venv/bin/python || { echo "Run bash install_and_test.sh first" >&2; exit 1; }
source .venv/bin/activate
python -m pip install "kokoro-onnx>=0.4,<1" "soundfile>=0.12,<1"
mkdir -p models
base="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1"
fetch_verified() {
  local filename="$1" sha="$2"
  if [ -s "models/$filename" ] && echo "$sha  models/$filename" | sha256sum --check --status; then
    echo "$filename: already verified"
    return
  fi
  curl --fail --location --retry 3 --connect-timeout 30 \
    "$base/$filename" -o "models/$filename.partial"
  echo "$sha  models/$filename.partial" | sha256sum --check
  mv "models/$filename.partial" "models/$filename"
}
fetch_verified "kokoro-v1.0.fp16.onnx" "f3a290d384fbb27966d462905c71a46cef9e5fd00516b40df32a0b4afe77ac96"
fetch_verified "voices-v1.0.bin" "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d"
python - <<'PY'
from pathlib import Path
assert Path("models/kokoro-v1.0.fp16.onnx").stat().st_size > 150_000_000
assert Path("models/voices-v1.0.bin").stat().st_size > 20_000_000
from kokoro_onnx import Kokoro
tts=Kokoro("models/kokoro-v1.0.fp16.onnx","models/voices-v1.0.bin")
print("Local Kokoro neural voice available. No cloud connection required for synthesis.")
PY
echo "Source model license Apache 2.0; package MIT. Review upstream licenses before commercial redistribution."
echo "Audition: .venv/bin/python scripts/audition_kokoro.py"
