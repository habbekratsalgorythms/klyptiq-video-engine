# Klyptiq Gaming — energetic narrator direction (local, no Descript credits)

## Creative target

- English-language gaming Shorts voice: conversational, bright, curious, and fast-paced.
- Start directly with a short hook. No slow formal welcome or robotic list-reading.
- Speak around 165–185 words per minute when clear. Split narration into short 3–12 word beats.
- Vary emphasis with question marks, punctuation and **subtle** pace shifts, not chipmunk playback or excessive pitch correction.
- Let narration audio control scene lengths and subtitle timing.
- Keep captions concise and the imagery fully opaque/sharp with mild cinematic motion.
- Distinguish **Rockstar-confirmed facts** from fan speculation.
- Do not clone, copy or impersonate the voice of the example YouTube narrator; emulate only general energetic presentation.

## Models and voices

- `Piper` is maintained as a free fallback for simpler or documentary-style previews.
- `Kokoro` is an optional local CPU ONNX voice engine installed with `bash scripts/setup_kokoro.sh`.
- The script downloads verified upstream **FP16 model + voices** (total about 192 MB), stored in ignored `models/`.
- Package license: MIT; model license: Apache-2.0. Check upstream publisher policies and model terms before redistribution.
- Test male voices: `am_puck` (lively), `am_fenrir` (punchier), `am_michael` (conversational). Characterizations are provisional until listening.
- Generate 3 WAV samples with `. .venv/bin/activate && python scripts/audition_kokoro.py`.
- Render animated video preview:
  ```bash
  . .venv/bin/activate
  python render.py briefs/energetic-story-kokoro.json --tts kokoro \
    --model models/kokoro-v1.0.fp16.onnx --voice am_puck \
    --pace 1.12 --motion --quality production \
    -o output/Klyptiq_gaming_narrator_1080p.mp4
  ```

## Safeguards

- The YouTube reference https://www.youtube.com/shorts/LHAGrPUeJw4 was not directly playable through the current automation tools. We cannot claim to have heard that exact speaker.
- Before any automatic social posting, listen to the 3 voice samples, verify that game names are pronounced correctly, and watch the full 1080p rendered video.
- Do not overwrite previous approved Descript exports, store passwords in this repository, or automatically republish the same video.
- GitHub CI is a test facility, not an always-on revenue-generating service. No upgrades, purchases or paid API calls authorized.
