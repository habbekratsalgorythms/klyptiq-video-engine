#!/usr/bin/env python3
"""Klyptiq rights preflight — audit one individual proposed publication.

Fail-closed documentation gate, NOT a legal-opinion engine or permission to publish.
No network, no side effects, no social publishing. Every video requires a new review.
"""
import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path

SOURCE_RULES = {
    "own_original",
    "licensed_commercial",
    "quote_article_15a",
}
PLATFORMS = {"instagram", "tiktok", "youtube", "facebook", "threads", "website"}
MONETIZATION = {"none", "platform_ads", "affiliate", "sponsor", "product_promotion"}

def _nonempty(value, minimum=8):
    return isinstance(value, str) and len(value.strip()) >= minimum

def inspect_release(record, today=None):
    """Return structured blockers. Even a clean record requires human release."""
    today = today or date.today()
    blockers = []
    warnings = []
    if not isinstance(record, dict):
        return {"status": "BLOCK", "blockers": ["Review record must be an object"], "warnings": []}
    if not re.fullmatch(r"[A-Za-z0-9_-]{4,72}", str(record.get("content_id", ""))):
        blockers.append("Missing safe, unique content_id")
    video_hash = record.get("render_sha256", "")
    if not isinstance(video_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", video_hash):
        blockers.append("Missing final rendered file sha256: review cannot apply to an unknown edit")
    try:
        review_date = date.fromisoformat(record["review_date"])
        if review_date > today or review_date < today - timedelta(days=7):
            blockers.append("Rights review is not fresh (must be within seven calendar days)")
    except (KeyError, TypeError, ValueError):
        blockers.append("Missing YYYY-MM-DD rights review date")
    platforms = record.get("platforms")
    if not isinstance(platforms, list) or not platforms or any(p not in PLATFORMS for p in platforms):
        blockers.append("Explicit valid distribution platforms required")
    money = record.get("monetization")
    if not isinstance(money, list) or not money or any(m not in MONETIZATION for m in money):
        blockers.append("Explicit monetization context required")
    elif "none" in money and len(money) != 1:
        blockers.append("Monetization none cannot coexist with commercial methods")
    if not _nonempty(record.get("original_commentary_description"), 25):
        blockers.append("Describe the genuinely original content/commentary (25+ chars)")
    if record.get("facts_verified") is not True:
        blockers.append("Fact-check must be explicitly recorded")
    if record.get("audio_sources_checked") is not True:
        blockers.append("Music/voice/original-audio rights must be checked")
    assets = record.get("assets")
    if not isinstance(assets, list) or not assets:
        blockers.append("Each third-party excerpt and own visual/audio asset must be enumerated")
        assets = []
    quoted = False
    for idx, asset in enumerate(assets, 1):
        name = f"Asset #{idx}"
        if not isinstance(asset, dict):
            blockers.append(f"{name}: must be a record")
            continue
        rights = asset.get("rights_basis")
        if rights not in SOURCE_RULES:
            blockers.append(f"{name}: rights_basis missing/unsupported")
            continue
        if not _nonempty(asset.get("creator"), 2) or not _nonempty(asset.get("source_url"), 10):
            blockers.append(f"{name}: identify creator and source URL/evidence")
        if asset.get("lawfully_disclosed") is not True:
            blockers.append(f"{name}: lawful public release/source not confirmed")
        if rights == "licensed_commercial":
            if not _nonempty(asset.get("license_evidence"), 12):
                blockers.append(f"{name}: actual commercial/platform rights evidence missing")
            if not set(platforms or []).issubset(set(asset.get("licensed_platforms") or [])):
                blockers.append(f"{name}: license does not cover every selected platform")
            if not set(money or []).issubset(set(asset.get("licensed_monetization") or [])):
                blockers.append(f"{name}: license does not cover all selected commercial uses")
        if rights == "own_original":
            if asset.get("own_work_verified") is not True:
                blockers.append(f"{name}: original ownership or right to exploit not evidenced")
        if rights == "quote_article_15a":
            quoted = True
            for field, minimum in (
                ("quote_purpose", 12),
                ("specific_criticism_or_review", 35),
                ("why_this_exact_clip_is_needed", 35),
                ("why_this_length_is_proportionate", 30),
                ("source_credit_as_displayed", 8),
                ("personality_rights_check", 20),
                ("publisher_policy_check", 25),
                ("neighboring_rights_check", 20),
            ):
                if not _nonempty(asset.get(field), minimum):
                    blockers.append(f"{name}: missing detailed Article 15a/neighboring rights assessment: {field}")
            if asset.get("decorative_only") is not False:
                blockers.append(f"{name}: must verify clip is NOT decorative or generic background")
            if asset.get("is_leaked_or_spoiler") is not False:
                blockers.append(f"{name}: unpublished leaks/spoilers not acceptable")
            if not isinstance(asset.get("start_seconds"), (int, float)) or isinstance(asset.get("start_seconds"), bool) or asset.get("start_seconds") < 0:
                blockers.append(f"{name}: explicit excerpt start needed")
            if not isinstance(asset.get("duration_seconds"), (int, float)) or isinstance(asset.get("duration_seconds"), bool) or asset.get("duration_seconds") <= 0:
                blockers.append(f"{name}: explicit excerpt length needed; there is no universal safe seconds number")
            if not _nonempty(asset.get("editorial_assessment_by"), 3):
                blockers.append(f"{name}: identified human quote reviewer is mandatory")
            if any(m != "none" for m in (money or [])) and not _nonempty(asset.get("commercial_context_legal_analysis"), 45):
                blockers.append(f"{name}: separate commercial/contextual legal analysis missing")
            warnings.append(f"{name}: Article 15a applicability is fact- and context-dependent; no automatic legal clearance")
    if blockers:
        status = "BLOCK"
    elif quoted:
        status = "HUMAN_LEGAL_DECISION_REQUIRED"
    else:
        status = "READY_FOR_FINAL_HUMAN_REVIEW"
    if record.get("owner_release_approved") is not True:
        warnings.append("No release authorization recorded; publication not approved")
    if quoted:
        warnings.append("A human legal assessment and explicit owner approval of this exact cut are still mandatory")
    return {"status": status, "content_id": record.get("content_id"),
            "blockers": blockers, "warnings": warnings,
            "quote_assets": sum(a.get("rights_basis")=="quote_article_15a"
                                for a in assets if isinstance(a,dict)),
            "machine_publish_approved": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rights_record", type=Path, help="One video/one planned publication — no generic blanket approval")
    parser.add_argument("--output", type=Path, help="Optional local JSON report path")
    args = parser.parse_args()
    obj = json.loads(args.rights_record.read_text(encoding="utf-8"))
    result = inspect_release(obj)
    report = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    # Exit 0 only for preflight readiness, NEVER actual publication permission.
    raise SystemExit(0 if result["status"]=="READY_FOR_FINAL_HUMAN_REVIEW" else 2)

if __name__ == "__main__":
    main()
