# Real video / gameplay clips — local-only, opt-in

The Klyptiq renderer supports both still photos and video clips in the **opt-in** `--pop` Shorts format.

## What this enables
- Per-scene 1080×1920 gameplay clips, ideally the channel owner's own recordings.
- A mixture of real moving video and photographs in one Short.
- Automatic crop to 9:16 with fixed on-screen headers and changing high-contrast captions.
- Narration uses only Kokoro/Piper audio. Sound from imported gameplay clips is intentionally **discarded** (including any licensed in-game music) to avoid accidental redistribution.
- A video shorter than its voiced scene is looped. Use sufficiently varied permitted footage for better results.

## How to supply media
1. Put video files under the ignored local `assets/` folder, e.g. `assets/owned_gameplay.mp4`. Do **not** commit raw gameplay to public GitHub.
2. In each selected scene of a JSON briefing, use:
```json
{
  "caption": "THE CITY NEVER SLEEPS",
  "voiceover": "This game world feels alive in so many small ways.",
  "asset_video": "../assets/owned_gameplay.mp4",
  "media_rights": "self_recorded"
}
```
3. For other scenes, the existing `"asset":"../assets/approved.jpg"` still works.
4. Run:
```bash
. .venv/bin/activate
python render.py briefs/my_approved_brief.json \
  --tts kokoro --model models/kokoro-v1.0.fp16.onnx \
  --voice am_puck --pace 1.12 --pop \
  --quality production -o output/Klyptiq-clip-review.mp4
```

## Rights gate

For each `asset_video`, declare one of:
- `"self_recorded"`: video recorded by the content creator, with permission to share;
- `"licensed"`: appropriate commercial video license held;
- `"permission_documented"`: written use permission held.

A declaration alone **does not prove licensing** or exempt copyrighted music, in-game video or platform restrictions. Permission must actually exist, and should be documented before commercial publication.

Check the publisher's terms. Rockstar's published fan-content policy is mostly limited to non-commercial use: https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material

Malformed files, missing video streams, absent rights declarations, or using a video scene without `--pop` are rejected before a finished MP4 is exported.

## Limitations
- This is a tool, not a rights-acquisition service. It **never downloads clips automatically**.
- It does not create or fabricate new GTA VI gameplay footage.
- The video crop centers the action; manually inspect clips where characters near the edge could be cut off.
- The renderer does not yet cut to word-level beats; timing remains at scene level with optional changing caption cards.
- No Metricool tokens, credentials, auto-upload or paid API calls are required.

## Validation
`tests/test_clips.py` creates its own synthetic, copyright-free FFmpeg video clip and a photo, then renders a narration-only mixed scene. Production publication remains blocked pending editorial and rights review.
