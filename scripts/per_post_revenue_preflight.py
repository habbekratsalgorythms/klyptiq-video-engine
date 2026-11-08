#!/usr/bin/env python3
"""Classify ONE Klyptiq publication's revenue intent, per-platform limitations and rights.

Offline POLICY preflight, NOT a toggle for YouTube/TikTok/Instagram and NEVER an
authorization to publish. Link this assessment to the exact rendered file hash.
Always use publication_rights_preflight.inspect_release for the underlying IP.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from publication_rights_preflight import inspect_release

CATEGORIES={"owned_commercial","unpaid_game_analysis","owned_unpaid"}
PUBLISH_FORMS={
    "youtube":{"long_video","short"},
    "instagram":{"post","reel","story"},
    "tiktok":{"video","photo"},
    "facebook":{"post","reel"},
    "threads":{"post"},
    "website":{"article"},
}
MONEY_SIGNALS=("affiliate_links","paid_partner","product_or_service_cta","paid_boost")
SUPPORT={
  ("youtube","long_video"):"Creator can choose monetization Off for an individual long-form video (if controls are available in Studio). This does NOT stop all third-party/platform advertisements.",
  ("youtube","short"):"Shorts Feed ad sharing runs through the Shorts Monetization Module; a guaranteed per-Short off switch was NOT verified.",
  ("instagram","reel"):"No universal verified per-Reel off switch for all Meta monetization programs.",
  ("instagram","post"):"No universal verified per-post off switch for all Meta monetization programs.",
  ("tiktok","video"):"Monetization depends on program and account; no universal Creator Rewards per-video off control was verified.",
}

def evaluate(record, today=None):
    basic=inspect_release(record,today=today)
    blockers=list(basic.get("blockers",[]))
    manual=[]
    warnings=list(basic.get("warnings",[]))
    category=record.get("publication_category") if isinstance(record,dict) else None
    if category not in CATEGORIES:
        blockers.append("Choose exactly one publication_category: owned_commercial, owned_unpaid or unpaid_game_analysis")
    platforms=record.get("platforms",[]) if isinstance(record,dict) else []
    money=record.get("monetization",[]) if isinstance(record,dict) else []
    if category in {"owned_unpaid","unpaid_game_analysis"} and money != ["none"]:
        blockers.append("Unpaid category may not request ads, affiliate, sponsorship or sales revenue")
    if category=="owned_commercial" and (not money or money==["none"]):
        blockers.append("Commercial category must declare the actual intended money streams")
    controls=record.get("platform_posts",[]) if isinstance(record,dict) else []
    if not isinstance(controls,list):
        controls=[]
    if isinstance(platforms,list) and set(platforms)!={x.get("network") for x in controls if isinstance(x,dict)}:
        blockers.append("Exactly one platform_posts entry for every selected platform is required")
    if len(controls)!=len(platforms):
        blockers.append("Duplicated or incomplete per-platform plan")
    any_growth=False
    for p in controls:
        if not isinstance(p,dict):
            blockers.append("Invalid platform post plan")
            continue
        platform=p.get("network")
        fmt=p.get("format")
        if fmt not in PUBLISH_FORMS.get(platform,set()):
            blockers.append(f"{platform}: unsupported post format")
            continue
        evidence=p.get("control_evidence","")
        if p.get("platform_monetization") not in {"off_manually_verified","not_enrolled","unknown","on"}:
            blockers.append(f"{platform}: specify platform_monetization without assuming software switched it")
        if p.get("platform_monetization")=="off_manually_verified" and (not isinstance(evidence,str) or len(evidence.strip())<15):
            blockers.append(f"{platform}: manual off requires actual dated evidence from account settings")
        if any(p.get(field) is True for field in MONEY_SIGNALS):
            if category!="owned_commercial":
                blockers.append(f"{platform}: unpaid classification conflicts with affiliate, sponsor, advertising or product CTA")
        if category in {"unpaid_game_analysis","owned_unpaid"} and p.get("platform_monetization")=="on":
            blockers.append(f"{platform}: monetization enabled on a post classified unpaid")
        if p.get("brand_growth_intent") is True:
            any_growth=True
        if category=="unpaid_game_analysis":
            manual.append(f"{platform}: confirm non-earning account/settings; 'off' does not guarantee ad-free or lawful use")
            if p.get("platform_monetization") in {"unknown","on"}:
                blockers.append(f"{platform}: cannot verify the post is non-earning")
            if (platform,fmt) in SUPPORT:
                warnings.append(f"{platform}/{fmt}: {SUPPORT[(platform,fmt)]}")
            # Even if Off verified, it cannot erase the professional/promotional purpose.
            if p.get("brand_growth_intent") is True:
                manual.append(f"{platform}: lawyer/editor must assess commercial brand-growth intention and publisher policy")
    assets=record.get("assets",[]) if isinstance(record,dict) else []
    third_party=any(isinstance(a,dict) and a.get("rights_basis")!="own_original" for a in assets)
    quotes=any(isinstance(a,dict) and a.get("rights_basis")=="quote_article_15a" for a in assets)
    if category=="owned_commercial" and quotes:
        manual.append("Commercial quote of third-party media requires independent legal review of each precise excerpt")
    if category=="unpaid_game_analysis" and not third_party:
        warnings.append("Unpaid game analysis may be based on owned/original graphics; this is preferable to uncleared footage")
    if category=="unpaid_game_analysis" and third_party:
        manual.append("No blanket publisher permission: business-channel fan policy, quotation exception and audience acquisition must be separately assessed")
    if category in {"owned_commercial","owned_unpaid"} and third_party:
        blockers.append("Owned category cannot include third-party clip: reclassify and fully document rights and purpose")
    if category=="owned_commercial" and any_growth:
        warnings.append("Audience growth is not a rights license and is distinct from platform ad revenue")
    if basic.get("status")=="HUMAN_LEGAL_DECISION_REQUIRED":
        manual.append("The Article 15a preflight explicitly requires a qualified human legal/editorial decision")
    if any(p.get("network")=="youtube" for p in controls if isinstance(p,dict)):
        warnings.append("Even with monetization disabled, YouTube or a claimant may show ads without paying Klyptiq")
    if blockers:
        status="BLOCK"
    elif quotes or (category=="unpaid_game_analysis" and third_party):
        status="MANUAL_LEGAL_REVIEW_REQUIRED"
    else:
        status="READY_FOR_OWNER_AND_PLATFORM_REVIEW"
    return {
       "status":status,
       "publication_category":category,
       "asset_gate":basic.get("status"),
       "blockers":blockers,
       "manual_actions":list(dict.fromkeys(manual)),
       "warnings":list(dict.fromkeys(warnings)),
       "can_auto_publish":False,
       "platform_monetization_was_changed":False,
       "final_owner_approval_still_required":True
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record",type=Path)
    parser.add_argument("--report",type=Path)
    args=parser.parse_args()
    data=json.loads(args.record.read_text(encoding="utf-8"))
    result=evaluate(data)
    out=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    print(out)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(out,encoding="utf-8")
    raise SystemExit(2 if result["status"]!="READY_FOR_OWNER_AND_PLATFORM_REVIEW" else 0)

if __name__=="__main__":
    main()
