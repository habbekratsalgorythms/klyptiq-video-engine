# Klyptiq V4 — launch-trailer Director Cut (8 November 2026)

**Creative direction:** leave repetitive five-card AI slides behind. Use 20 actual moving shot positions assembled from **seven different short excerpts** of the full official 89-second GTA VI launch trailer plus short official moving character clips. Combined with original English narration, original synth accompaniment and micro-impacts, from the existing Klyptiq FFmpeg/Python/locally executed Kokoro pipeline. This is not a Descript project.

## Why this should feel substantially different

- V3 overused the 1–1.5s Rockstar character shorts; V4 introduces location/action imagery at several points across an 89s trailer (8, 16, 25, 34, 45, 58, 76 seconds).
- The first scene deliberately starts with five different trailer cuts, rather than an animated poster.
- One visual idea per beat: opening, landscape/mood, people, response question. Twenty clip positions across four scene-level voiceovers.
- No fake GTA gameplay, no image-only fallback, no clip audio reuse. New story and small on-screen text are editorial commentary, not Rockstar quotes.

## Files and reproducibility

- `briefs/review/launch-trailer-v4.json` — four original narrated scenes, twenty specified shots.
- `scripts/prepare_launch_trailer_excerpts.py` — acquire seven ~2.25s remote range-seeked excerpts with frozen source URL, trailer byte count/duration checks and local SHA manifest. Do not download/store the entire ~782MB trailer.
- `.github/workflows/launch-trailer-v4-review.yml` — install free dependencies, prepare verified character ZIP, acquire seven new short excerpts, locally synthesize Kokoro, create a 1080x1920 H.264/AAC V4 MP4, verify audio/video and generate a contact sheet. CI has read-only repo permissions and no social credentials.
- `scripts/evaluate_director_review.py` — mechanical QC. **Passing QC is not the same as passing creative editorial review.**

## Review gates

1. Download the `KLYPTIQ-LAUNCH-TRAILER-V4-REVIEW-ONLY` artifact in the latest green <https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/workflows/launch-trailer-v4-review.yml> run (3-day retention).
2. Play full MP4 **with audio**; assess first second, image cropping, cut rhythm, alignment of voice and subtitles, originality, whether soundtrack competes with narration, face recognition, meaningful story.
3. Compare frame-by-frame with V3 at <https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42508403910>. Determine whether the difference is substantial, not merely a higher cut count.
4. Check publisher rights. The Rockstar official media archive is viewable but the commercial/monetization license is not established. `distribution=internal_review` strictly blocks a claim of release readiness.
5. Only after rights and subjective quality are approved should new media be considered for Metricool. No automated social publishing, no paid APIs, no Descript.

If it fails, mark precise creative defects and adjust the **shot selections and narrative**, not just typography, zoom or voice speed.
