# Klyptiq Video Engine — Local MVP

Offline 9:16 video renderer for Klyptiq Gaming. Creates MP4 with local English voice-over, overlaid phrase captions, fully opaque image foreground, blurred backgrounds and H.264/AAC output. **This is a technical test, not final social content.**

## Download the test video directly from GitHub

1. Go to [Actions — Render downloadable demo](https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/workflows/render-demo.yml).
2. Select the most recent **successful** workflow run.
3. Under **Artifacts**, download **Klyptiq-testvideo-MP4**.
4. Unzip the download and play `Klyptiq_testvideo.mp4`.

You may need to sign in to GitHub to download workflow artifacts. The CI preview is rendered at 360×640 to keep processing quick. It deliberately contains no Rockstar gameplay images, and the free eSpeak voice sounds robotic. Do not publish it.

## Install on Ubuntu

```bash
git clone https://github.com/habbekratsalgorythms/klyptiq-video-engine.git
cd klyptiq-video-engine
bash install_and_test.sh
```

Setup installs FFmpeg, eSpeak, Python and Pillow (free software). It may request sudo permission.

Full resolution:

```bash
. .venv/bin/activate
python render.py briefs/example.json -o output/first-video.mp4
```

The optional `--tts piper --model /path/to/voice.onnx` uses an already installed local Piper and local voice model, if licensed appropriately. No models are automatically downloaded. To include an authorized image, place it under `assets/` locally and add a path like `"asset":"../assets/approved.jpg"` to a scene in the JSON briefing. The local `assets/` directory is ignored by Git.

## Limitations and safeguards

- No automatic research, copyrighted media downloading, Metricool publishing or paid APIs.
- eSpeak is a low-quality fallback voice; test-only until an acceptable natural voice is installed.
- Captions are timed approximately to phrase-level speech, not word-level alignment.
- All renders require human quality review before posting.
- No secrets, customer data, SpotlessPro Agent Lab access or automatic purchases.

GitHub Actions runs three unit tests, makes a small downloadable technical MP4 and checks it has valid audio/video streams after code changes. No external publishing occurs.
