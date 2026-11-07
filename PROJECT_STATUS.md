# Klyptiq Video Engine — execution status

Updated 2026-11-07. Project is independent from SpotlessPro Agent Lab, the hours app, other HabbekratsAlgorythms income tracks, and production Metricool scheduling.

## Verified baseline

- GitHub repository: https://github.com/habbekratsalgorythms/klyptiq-video-engine
- Main branch contains FFmpeg + Pillow + eSpeak fallback and successful downloadable demo; no automatic video posting.
- Enhancement branch: `feature/local-piper-production-gates-20261107`.
- Initial successful automated tests: https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42423047008
- Neural Piper voice preview run succeeded: https://github.com/habbekratsalgorythms/klyptiq-video-engine/actions/runs/42423186148
- GitHub workflows used only the standard runners on this **public** repository; no purchase or subscription.

## Implemented on enhancement branch

1. `scripts/setup_piper.sh` installs a free offline neural voice and verifies model SHA-256. It saves weights only in ignored `models/`.
2. Uses Piper `en_US-kristin-medium`, trained from public-domain LibriVox recordings per upstream voice MODEL_CARD. Voice engine Piper is GPL-3.0; review publisher and model rights before monetized use.
3. `scripts/prepare_editorial_media.sh` retrieves already-imported Rockstar stills from owner's existing Metricool CDN for local editorial review; files are ignored by Git.
4. `render.py` aligns scenes to separately synthesized spoken lines using `scenes[].voiceover`; old script-only briefs still work.
5. `--quality production` rejects robotic eSpeak audio and images smaller than 1080x1920.
6. `install_and_test.sh` prepares local voice, source media and review-only 1080p MP4 in one command after installing free dependencies.
7. `quality-check.yml` tests Python, sound synchronisation, stream validity and a synthetic visual preview.
8. `piper-preview.yml` creates a neural-voice review video as a GitHub Actions artifact. No publishing credentials or networks in CI.

## Immediate next work

- Verify latest 1080p Piper preview workflow result and inspect sampled frames and audio streams.
- Improve motion and transitions using only local tools; keep static captions readable and foreground photos fully opaque.
- Test on Ubuntu VM once available, not on SpotlessPro production VM directories.
- Prepare more facts-checked briefings, then connect **only reviewed MP4s** to Metricool Instagram Reels, TikTok and YouTube Shorts.

## Owner tasks

- No action required while the GitHub branch tests and previews run.
- Later: turn on Ubuntu VM and allow local installation; review one high-quality narrated MP4 before unattended publishing.
- No purchases, subscriptions or budget changes without explicit consent.

## Jesse tasks

- Set consistent Klyptiq Gaming / `klyptiqgaming` names and existing profile bios across Instagram, TikTok and YouTube.
- Use `habbekratsalgorythms@gmail.com` as business contact.
- Check brand profile photos; spot-check social posting success and sound after future posts.
- Threads isn't connected to Metricool and does not block current strategy; 2FA is postponed by owner.

## Safety / current limitations

- Do not claim any videos here are published to social media; these are test artifacts.
- eSpeak previews are technical-only. Piper 1080p improves speech but creative quality still requires visual/audio review.
- No automatic news research, fact verification, game footage rights acquisition, affiliate monetization or revenue claims.
- Copyright and media monetization rights require verification before commercial upload.
