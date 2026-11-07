#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Installing free local packages on Ubuntu..."
sudo apt-get update
sudo apt-get install -y ffmpeg espeak python3-venv python3-pip fonts-dejavu-core
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python render.py briefs/example.json -o output/klyptiq-first-test.mp4
echo "Finished: $PWD/output/klyptiq-first-test.mp4"
