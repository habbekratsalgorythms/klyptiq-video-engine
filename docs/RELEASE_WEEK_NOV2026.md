# GTA VI release-week batch — Klyptiq editorial drafts

Status: three distinct 1080 × 1920 Kokoro + kinetic-caption MP4 review files generated and tested. Not scheduled on social media.

Source checked 8 November 2026:
- https://www.rockstargames.com/VI
- Pre-load announced for 10 November 2026; scheduled launch 19 November 2026 (PS5, Xbox Series X|S).
- Rockstar's official biographies for Jason Duval and Lucia Caminos.
- Rockstar copyright terms: https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material
  Most fan-use permissions described in these terms concern **non-commercial** usage. This project must not assume monetization rights to Rockstar artwork or video.

## Three reviewed script candidates

| File | Editorial angle | Suggested window (Europe/Amsterdam) |
|---|---|---|
| `preload-nov10.json` | Nov 10 pre-load and Nov 19 planned release | Nov 9–10, only after re-checking official news |
| `lucia-backstory.json` | Confirmed Lucia profile | Nov 10–12 |
| `jason-backstory.json` | Confirmed Jason profile | Nov 11–13 |

These dates are **suggestions**, not confirmed Metricool availability or scheduled posts.

## Verified build

- [GitHub Actions release-week review run](https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42497800523): all three separate matrix jobs succeeded.
- Artifacts: `Klyptiq-preload-nov10-editorial-review`, `Klyptiq-lucia-backstory-editorial-review`, `Klyptiq-jason-backstory-editorial-review`.
- FFprobe verifies H.264 video and AAC soundtrack, 1080x1920, nonempty outputs.
- `tests/test_release_week.py` checks three unique briefs, exact source URL, dates and valid scene descriptions. Such automated tests cannot themselves confirm a publisher's latest announcement.

## Before publishing

1. Independently watch and listen to each video, check factual subtitles and pronunciation.
2. Obtain and document the right to reuse/monetize the underlying images and any music; otherwise use licensed, original visual material and a non-commercial setting that complies with Rockstar's policy.
3. Confirm publication details with the current official Rockstar website again, especially pre-load/release dates.
4. Check Metricool for duplicate topics, post failures, and the existing Instagram/TikTok/YouTube scheduled videos.
5. Upload only an approved video to each platform, **never** a placeholder, trial soundtrack, or unapproved rights-sensitive material.
6. Maintain the existing published/scheduled content. No auto-updating a published post without explicit purpose.

## Cost & security

- All speech synthesis/renders use offline Kokoro/FFmpeg and standard GitHub public runners. No Descript credits or paid API requests.
- Workflow has only GitHub `contents: read` permissions, no Metricool tokens, no payment connections, no publishing steps.
- Klyptiq remains separate from SpotlessPro Agent Lab and other Habbekrats projects.

Next improvement: licensed gameplay cuts with appropriately timed visual cues. Current drafts remain moving-image posters rather than gameplay recordings.
