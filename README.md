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

Setup installs free FFmpeg, Python and Pillow, runs tests, then first tries to install a **more expressive local Kokoro neural voice** and render a **1080×1920 review MP4 with slow photo movement**. If Kokoro is unavailable, it falls back to Piper. It may request sudo permission and network access for dependencies and official editorial sample media. The video stays local: nothing is published to Metricool.

### More energetic gaming voice — preferred

The original Piper narrator was judged too flat for Klyptiq Gaming. Use Kokoro for new gaming Shorts instead. Kokoro-ONNX is MIT licensed and the official Kokoro weights are Apache-2.0 licensed. Upstream SHA-256 verified model and voices are kept in ignored `models/`, not in Git.

```bash
bash scripts/setup_kokoro.sh
bash scripts/prepare_editorial_media.sh
. .venv/bin/activate
python scripts/audition_kokoro.py
python render.py briefs/energetic-story-kokoro.json --tts kokoro \
  --model models/kokoro-v1.0.fp16.onnx --voice am_puck \
  --pace 1.12 --motion --quality production \
  -o output/Klyptiq_energetic_story_1080p.mp4
```

- Voice options `am_puck`, `am_fenrir` and `am_michael` are provided in `output/voice-auditions/` for listening.
- The clip at https://www.youtube.com/shorts/LHAGrPUeJw4 is inspiration for **general pacing and energy**, not a source for cloning the speaker.
- Per-scene `pace` from 0.85 to 1.30 controls emphasis without brute-force speeding up the entire exported MP4.
- The GitHub Actions workflow `kokoro-audition.yml` generates three audition WAVs and one 1080p review MP4, without any social publication.
- The model download totals approximately 192 MB; inference happens locally without paid AI credits.

### Piper fallback — still available



The optional fallback uses `en_US-kristin-medium`, a voice trained from LibriVox public-domain recordings. The downloaded model is checksum-verified and stored under ignored `models/`. Read the upstream MODEL_CARD before using any voice commercially.

If only the voice needs preparation:

```bash
bash scripts/setup_piper.sh
bash scripts/prepare_editorial_media.sh
. .venv/bin/activate
python render.py briefs/visual-demo.json --tts piper \
  --model models/en_US-kristin-medium.onnx \
  --quality production -o output/klyptiq-Piper-1080p.mp4
```

The `--quality production` guard requires either Piper or Kokoro (and rejects eSpeak) or below-1080×1920 video, so robotic technical previews cannot accidentally be treated as production quality. Production still requires a human to approve final content before uploading.

For cheaper technical testing, use `--quality preview --width 360 --height 640`. Never publish these previews.

### Real gameplay/video clips — opt in

Klyptiq's `--pop` mode now also accepts **local video clips** instead of only photographs, mixed in any order. Use only material you have the appropriate rights to distribute. The imported clip's original audio is deliberately not copied. See [VIDEO_INPUTS.md](docs/VIDEO_INPUTS.md) for setup and an example JSON scene with `asset_video` and mandatory `media_rights`. No new footage is generated or downloaded.

### New footage-first Director Cut — explicitly NOT another photo slideshow

Use `--director` with a per-scene `shots` storyboard. Unlike the old photo slideshow, it requires at least two distinct sources per scene, moving video in at least two thirds of the shots, cuts of 0.5–2.1 seconds, scene-synced captions, original synthetic drum/bass music automatically ducked under offline narration, and original short sound accents. It removes the giant slide title and black lower-third boxes. A shot with `layout: "stacked"` can now compose **two separate cleared video streams simultaneously** above and below an "AND/OR" divider, with separate offsets and rights declarations. Short one-second clips slow no more than 1.8× instead of looping visibly.

**Editorial experiment:** The [real GTA VI review workflow](docs/REAL_FOOTAGE_REVIEW.md) temporarily retrieves a SHA-pinned official Rockstar archive, prepares the `Six More Faces` 19-shot V3 review and runs independent visual/audio checks. All original footage stays out of Git and **no social content is published**. `editorial_review_only` clips are permitted **only** when `distribution: "internal_review"`. A successful render does not grant commercial rights or prove creative quality. The old `--pop` and `--motion` modes are still unchanged.

### Caption timing

A scene can now specify `"voiceover":"One complete spoken sentence."` alongside `"caption":"Short screen phrase"`. If *all* scenes contain voiceover, the renderer synthesizes each spoken sentence separately, measures the real WAV duration, and aligns its image and caption to that duration. Old single-script briefs remain supported, but use approximate timing.

### Assets and rights

**Commercial release is blocked for the existing Rockstar-footage V3/V4 review videos** until appropriately scoped commercial permissions have been documented. Read the [November 2026 official-source monetization audit](docs/COMMERCIAL_RIGHTS_AUDIT.md) before any ad revenue, sponsor, affiliate or paid reuse; fan-video allowances are not a commercialization license. Original, rights-cleared hardware/tool videos are the suggested monetization track.

The optional `scripts/prepare_editorial_media.sh` retrieves images previously imported into the owner's Metricool workspace for evaluation. Files remain local under ignored `assets/` and are not committed or redistributed. This is **not** an assertion that all Rockstar screenshots or footage may be used commercially. Verify the relevant media rights and publisher policies before monetized posting. No fabricated gameplay or misleading claims.

You can place other authorized image files in `assets/` and reference them from scene JSON as `"asset":"../assets/approved.jpg"`.

### Free GitHub test builds

The branch's `quality-check.yml` validates scene timing with synthetic artwork. `piper-preview.yml` renders a **Piper fallback evaluation preview** using the downloaded Piper voice and the owner's editorial images. Neither workflow posts to social networks.

## Limitations and safeguards

- No automatic research, media publishing, paid APIs or automatic Metricool posting.
- eSpeak is a low-quality fallback voice; test-only until an acceptable natural voice is installed.
- Captions are timed approximately to phrase-level speech, not word-level alignment.
- All renders require human quality review before posting.
- No secrets, customer data, SpotlessPro Agent Lab access or automatic purchases.

GitHub Actions runs unit and integration tests, makes a small downloadable technical MP4 and checks it has valid audio/video streams after code changes. No external publishing occurs.
