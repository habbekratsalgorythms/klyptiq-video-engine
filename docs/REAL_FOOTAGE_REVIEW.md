# Klyptiq real-footage review pipeline — 8 November 2026

This is NOT a Descript project. Rendering runs entirely through our own `render.py`, `director_cut.py`, FFmpeg, Pillow and **local Kokoro**. No cloud AI payments, editing subscriptions, social tokens or publishing.

## Source

The original verified source is Rockstar's official GTA VI media archive:

- Website: https://www.rockstargames.com/VI/media/videos
- Download: https://media.rockstargames.com/VI/downloads/videos/GTAVI_Videos.zip
- Verified ZIP SHA-256: `017b806729ae09d54180e9c83c31ef201ff4288751186f20d11ea2c513de7698`
- ~121 MB downloaded in GitHub Actions, **not** stored in Git or copied into public releases.
- Nine video files: eight named character clips (most 1–1.5 seconds) plus a longer official cover animation (~32.7 seconds).
- Short character clips are real Rockstar moving video, *not* leaked gameplay or AI-invented GTA VI scenes. However, they provide VERY LIMITED unique motion and cannot by themselves create the visual variety of a 2-minute gameplay trailer.

The extracted files remain in ignored `assets/rockstar_review/`, each with SHA metadata and explicit `commercial_rights: NOT_ESTABLISHED`.

**Licensing:** Rockstar's support policy does not grant commercial reuse rights to these clips. This workflow is a noncommercial editorial evaluation only; it is not a commercial-ready post. See https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material . Never assume a media download button means a monetization license.

## V2: initial 18-shot pilot (superseded as preferred example)

- Brief: `briefs/review/eight-faces-director.json`
- Topic: **GTA VI — 8 faces, one state** (character names only; source factual)
- 4 spoken scenes; **18 actual video shots**; 9 different official video files.
- English Kokoro speech synthesized completely offline.
- Original synth beat with kick/backbeat/bass/hat, *ducked* automatically under narration.
- Original short sound accents at edit points.
- No source music/audio included, preserving media rights caution.
- Mobile 9:16, 1080×1920, H.264/AAC, captions unobtrusive.

## V3: 19-shot Six More Faces character story — the current review candidate

- Brief: `briefs/review/six-more-faces-story-v3.json`; the V2 brief remains in the repo for comparison.
- Story hook: everyone knows Jason and Lucia, but Rockstar has introduced six additional characters. Names based on original publisher character clips.
- Four spoken scenes, **19 cuts/shots, 18 actual transitions and six two-source stacked comparison compositions**; individual character shots fill the frame. All 19 primary sources contain real motion.
- No automatically repeated one-second video. Every shot checks the clip's actual duration and slows at most 1.8× if needed; rating-card intro avoided by source offsets 8+ seconds in the official cover animation.
- First V2 test: ~18.5s, 18 shots, 17 cuts. V3: **20.23s, 19 shots, 18 cuts**, 1080×1920, H.264/AAC, nine source files, nine different temporal QA sample signatures, mean audio around -15.9 dB.
- Tests: [V3 full 1080p render and mechanical quality report](https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42508403910) and [complete Python/FFmpeg regression suite](https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42508403903), both successful.
- V3 saved on the user's session as a review MP4. The GitHub workflow artifacts expire after only three days.
- **This is a real-source noncommercial review, not a monetization license or a subjective endorsement.** The original clips and full final MP4 can be viewed in artifact downloads of a *public GitHub repo*: do not mistake review-only labels for access control. Do not attach private data.

## Run from GitHub, no VM required

1. Open [GitHub Actions — Klyptiq 1080p REAL-footage Director review](https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/workflows/rockstar-director-review.yml).
2. Select a **successful** run and download the artifact `KLYPTIQ-SIX-MORE-FACES-V3-REVIEW-ONLY`.
3. Extract and play `KLYPTIQ-Six-More-Faces-Director-V3-1080p-REVIEW.mp4` with sound.
4. Inspect `REVIEW-contact-sheet.jpg` for cropped faces, awkward scenes and boring visuals. Read `review-quality.json` for mechanical properties.
5. Never upload it to Metricool, Instagram, TikTok or YouTube just because the technical CI says PASS.

If GitHub Actions is unavailable, on an isolated Ubuntu environment with git checkout and free dependencies:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
bash scripts/setup_kokoro.sh
mkdir -p assets/rockstar_review
curl -fL --retry 3 https://media.rockstargames.com/VI/downloads/videos/GTAVI_Videos.zip -o /tmp/GTAVI_Videos.zip
python scripts/prepare_official_review_clips.py \
  --archive /tmp/GTAVI_Videos.zip --output assets/rockstar_review \
  --internal-review-only
python render.py briefs/review/eight-faces-director.json \
  --tts kokoro --model models/kokoro-v1.0.fp16.onnx \
  --voice am_puck --pace 1.15 --director --quality production \
  --width 1080 --height 1920 -o output/KLYPTIQ-REVIEW.mp4
python scripts/evaluate_director_review.py output/KLYPTIQ-REVIEW.mp4 \
  --summary output/quality.json --contact-sheet output/sheet.jpg
```

For the tested local speech setup use **Python 3.12 and kokoro-onnx >=0.6.0**; older 0.4.7 passes an int32 speed tensor that breaks this model's float input. The GitHub workflow pins the runtime-version check. This is a reproducibility requirement, not a subscription.

## Creative acceptance is separate from mechanical tests

Do NOT call the project 'creator-grade' without personally reviewing it. A green CI only proves it renders and the source files, timing, streams, sound levels and visible frame variety meet mechanical constraints. Subjective questions remain:

- Is the first half-second compelling **before** hearing the audio?
- Is the hook actually interesting, not another generic 'GTA VI is coming' headline?
- Are images cropping faces or showing the wrong named character?
- Is there enough variety? Nine one-second official clips constrain the creativity severely.
- Is the music clear, energetic, ORIGINAL and still quieter than the narrator?
- Are spoken names pronounced naturally? Do captions match the person shown?
- Would this stop someone scrolling, compared with the user's favorite gaming channel?
- Is the footage permitted in the intended commercial context? **Not yet established.**

For genuine next-level montage, get rights-cleared longer gameplay footage and/or produce original 3D/animated data visuals for analysis; footage cannot be replaced with faked GTA VI content. **No autopublishing until owner approves one actual video as both creative and legally appropriate.**
