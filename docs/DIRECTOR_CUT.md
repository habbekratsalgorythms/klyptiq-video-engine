# Klyptiq: Director Cut (review-only, footage-first)

**Why this is a separate mode:** The previous `--pop` format is a five-card photo slideshow with animated captions. Better typography alone does not make it a creator-grade gaming Short. `--director` uses multiple rights-cleared video/photo shots *per spoken scene*, full-bleed media, minimal branding, visible cut rhythm, a short hook and originally generated impact cues.

## Hard production limits

- Two to six distinct planned shots per spoken scene (minimum two different sources per scene).
- At least **one third of shots must be moving video footage**, and at least three distinct sources across the whole video. **No silent fallback** to stock, fake game scenes, static image loops or downloaded Rockstar content.
- **0.5–2.1 seconds per shot**. More voiceover requires more shots: do not simply stretch one picture.
- Each shot declares `media_rights`: `self_recorded`, `licensed` or `permission_documented`. These are declarations, not automatic permission grants. Check real rights independently.
- Original gameplay/source audio is **never copied** (including copyrighted soundtrack). Only approved offline Kokoro/Piper voiceover and original, synthesized short impact cues.
- Small Klyptiq branding, no persistent giant header, no opaque black subtitle block hiding the action.
- No paid APIs, no model-generated fake game footage, no uploads or social posting.
- The old `--pop` and `--motion` commands remain unchanged.

## Storyboarding example (replace filenames with genuine authorized local assets)

Store the JSON as `briefs/my-director-short.json`; place footage and stills in the git-ignored `assets/` folder. Use a strong, source-verified hook plus 3-5 fast evidence moments, ending with one question. Example `scenes` array, to include within a complete brief with `title` and `script`:

```json
[
  {
    "caption": "THREE DETAILS YOU MISSED",
    "voiceover": "Three details from this reveal deserve a closer look.",
    "shots": [
      {"asset_video": "../assets/owned-opening.mp4", "media_rights": "self_recorded", "start": 0.5, "framing": "center", "text": "LOOK AGAIN"},
      {"asset_video": "../assets/owned-action.mp4", "media_rights": "self_recorded", "start": 2.5, "framing": "left", "text": "DETAIL ONE"},
      {"asset": "../assets/licensed-detail.jpg", "media_rights": "licensed", "text": "DID YOU SEE IT?"}
    ]
  },
  {
    "caption": "HERE IS THE SECOND CLUE",
    "voiceover": "And here's the second detail you might have missed.",
    "shots": [
      {"asset_video": "../assets/owned-third.mp4", "media_rights": "self_recorded", "start": 1.0, "framing": "right", "text": "SECOND CLUE"},
      {"asset": "../assets/licensed-map.jpg", "media_rights": "licensed", "text": "LOOK CLOSER"},
      {"asset_video": "../assets/owned-outro.mp4", "media_rights": "self_recorded", "text": "YOUR TAKE?"}
    ]
  }
]
```

For a complete brief, its `script` should match the spoken voiceover text (joined in scene order). A director-short requires fitting the voiceover duration to 0.5-2.1 seconds per planned shot; this gets checked against the rendered audio.

```bash
bash scripts/setup_kokoro.sh
. .venv/bin/activate
python render.py briefs/my-director-short.json \
  --tts kokoro --model models/kokoro-v1.0.fp16.onnx \
  --voice am_puck --pace 1.14 --director \
  --quality production --width 1080 --height 1920 \
  -o output/Klyptiq-DIRECTOR-REVIEW.mp4
```

## Release gate: technical PASS is not creative approval

Run `python -m unittest discover -s tests -v`. Its generated FFmpeg footage is **synthetic color/test patterns**: it proves genuine edits, source gating, video+audio output and original cues, but it cannot prove engaging creative quality. Only a review of a *real* licensed-media cut can establish that.

Before any publishing, manually review the 3-second hook, cut rhythm, visible details, caption accuracy, voice energy, volume, copyright/monetization permissions, final end-card and duplicate topics. Prefer no video's release over another uninteresting slideshow.

Official Rockstar press/media footage is available to download for review, but Rockstar's copyright policy generally describes **non-commercial** fan uses, not automatic commercial monetization rights. Consult <https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material> and contact Take-Two for commercial rights when needed.

## Next honest quality milestone

1. Obtain 6-12 diverse **rights-cleared** footage moments of the chosen game or several distinct games (prefer first-party gameplay captures or permissioned creator clips).
2. Produce one 20-30 second Director Cut with a real video hook, 12+ actual shot changes, active captions, original light SFX and a memorable takeaway.
3. Compare it side-by-side against a strong real creator example. If still boring, do not turn on autopublishing; improve shot selection and editorial storytelling, not just motion speed.
