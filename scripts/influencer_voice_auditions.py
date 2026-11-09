#!/usr/bin/env python3
"""Original Klyptiq character voice auditions (no publishing or paid services).

Default mode prints a safe plan; --execute synthesizes short WAV files using
the Kokoro models already verified by scripts/setup_kokoro.sh. This does not
create lip-sync, edit video, send network requests or publish anything.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "models" / "kokoro-v1.0.fp16.onnx"
DEFAULT_VOICES = ROOT / "models" / "voices-v1.0.bin"
DEFAULT_OUTPUT = ROOT / "output" / "influencer-voice-review"

# Separate character voices; none imitates a real individual's voice.
PROFILES = {
    "vexa-volt": {
        "voice": "af_bella",
        "speed": 1.08,
        "line": "Magic email button? Prove it.",
    },
    "pip": {
        "voice": "af_heart",
        "speed": 1.12,
        "line": "Patch, is this prompt any good?",
    },
    "patch": {
        "voice": "am_echo",
        "speed": 1.10,
        "line": "Nope. Try again.",
    },
    "blop": {
        "voice": "am_puck",
        "speed": 1.06,
        "line": "A cable that fits both ways? Fascinating!",
    },
}


def voice_plan() -> dict:
    return {
        "status": "AUDITION_ONLY_NOT_LIPSYNCED",
        "engine": "Local Kokoro ONNX 82M",
        "paid_api_calls": 0,
        "automatic_publication": False,
        "source_video_seconds": 73 / 24,
        "notes": [
            "Audition only: review the character voices before editing or lip-sync.",
            "The short dialogue may not match the video duration exactly.",
            "Do not represent these WAVs as synchronized speech.",
        ],
        "characters": [
            {"id": name, "filename": f"{name}.wav", **settings}
            for name, settings in PROFILES.items()
        ],
    }


def synthesize(model_path: Path, voices_path: Path, output: Path) -> Path:
    # All inferencing occurs locally: no online TTS or payment service.
    if not model_path.is_file() or not voices_path.is_file():
        raise FileNotFoundError(
            "Kokoro model files not found. Use the repository's verified "
            "scripts/setup_kokoro.sh before --execute."
        )
    if output.is_symlink():
        raise ValueError("Output folder cannot be a symlink")
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Refusing to overwrite an existing audition directory")
    import soundfile as sf
    from kokoro_onnx import Kokoro

    tts = Kokoro(str(model_path), str(voices_path))
    output.mkdir(parents=True, exist_ok=True)
    plan = voice_plan()
    for entry in plan["characters"]:
        name = entry["id"]
        samples, rate = tts.create(
            entry["line"], voice=entry["voice"], speed=entry["speed"], lang="en-us"
        )
        if not isinstance(rate, (int, float)) or rate <= 0 or len(samples) == 0:
            raise RuntimeError(f"Invalid audio produced for {name}")
        seconds = round(len(samples) / rate, 3)
        if seconds < 0.5 or seconds > 12:
            raise RuntimeError(f"Implausible audition duration for {name}: {seconds}s")
        wav_path = output / entry["filename"]
        sf.write(str(wav_path), samples, rate, subtype="PCM_16")
        entry["actual_seconds"] = seconds
        entry["sha256"] = hashlib.sha256(wav_path.read_bytes()).hexdigest()
    plan["status"] = "WAV_AUDITIONS_READY_FOR_HUMAN_REVIEW"
    manifest = output / "voice-review-manifest.json"
    manifest.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Actually synthesize local WAVs")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--voices", type=Path, default=DEFAULT_VOICES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    if not args.execute:
        print(json.dumps(voice_plan(), indent=2, ensure_ascii=False))
        print("SAFE DRY-RUN: no files written, model loaded or API requests sent.")
        return 0
    result = synthesize(args.model, args.voices, args.out)
    print(f"Auditions created for review: {result}")
    print("NO LIPSYNC; NO SOCIAL PUBLICATION.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
