#!/usr/bin/env bash
# Retrieves the owner's previously prepared Rockstar editorial screenshots.
# Assets stay local/CI-only (ignored by Git). Does not publish or monetize them.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v curl >/dev/null || { echo "curl required" >&2; exit 1; }
test -x .venv/bin/python || { echo "Run bash install_and_test.sh first" >&2; exit 1; }
mkdir -p assets
base="https://static.metricool.com/planner/202611"
brand="7945934"
get_image() {
  local name="$1" file="$2"
  if [ -s "assets/$name.jpg" ]; then
    echo "$name: local file exists, skipping"
    return
  fi
  curl --fail --location --retry 3 --connect-timeout 20 \
    "${base}/${brand}-file-${file}.jpeg" -o "assets/$name.jpg.part"
  .venv/bin/python - "assets/$name.jpg.part" <<'PY'
from PIL import Image
import sys
with Image.open(sys.argv[1]) as im:
    im.verify()
with Image.open(sys.argv[1]) as im:
    assert im.width >= 600 and im.height >= 300, "Suspiciously small image"
PY
  mv "assets/$name.jpg.part" "assets/$name.jpg"
  echo "$name: verified"
}
get_image lucia 3102169556167648104
get_image keys 374510237267671926
get_image vice 13685730624239388127
get_image park 10394665368765891791
get_image jason 15139828663160242076
echo "Source images prepared locally. Editorial review only; check publisher rights before monetization."
