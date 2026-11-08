"""Rights policy tests: disabled revenue cannot be used as a copyright bypass."""
import copy
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from per_post_revenue_preflight import evaluate

TODAY=date(2026,11,8)

class PerPostRevenueTests(unittest.TestCase):
    def own(self):
        return {
            "content_id":"KLYPTIQ-ORIGINAL-001","render_sha256":"a"*64,
            "review_date":TODAY.isoformat(),
            "platforms":["youtube"],"monetization":["platform_ads"],
            "original_commentary_description":"Own studio recording of an unbranded product and thoughtful hands-on testing.",
            "facts_verified":True,"audio_sources_checked":True,
            "owner_release_approved":False,
            "assets":[{"rights_basis":"own_original","creator":"Klyptiq Gaming",
                       "source_url":"internal://original-recording","lawfully_disclosed":True,
                       "own_work_verified":True}],
            "publication_category":"owned_commercial",
            "platform_posts":[{"network":"youtube","format":"long_video",
                 "platform_monetization":"on","control_evidence":"",
                 "affiliate_links":False,"paid_partner":False,
                 "product_or_service_cta":False,"paid_boost":False,"brand_growth_intent":True}]
        }

    def quoted(self):
        out=self.own()
        out["content_id"]="KLYPTIQ-GAME-REVIEW-001"
        out["publication_category"]="unpaid_game_analysis"
        out["monetization"]=["none"]
        out["platform_posts"][0]["platform_monetization"]="off_manually_verified"
        out["platform_posts"][0]["control_evidence"]="Verified YouTube Studio Off on 2026-11-08, internal reviewer"
        out["assets"]=[{
            "rights_basis":"quote_article_15a",
            "creator":"Rockstar Games","source_url":"https://www.rockstargames.com/VI/media/videos",
            "lawfully_disclosed":True,
            "quote_purpose":"Explain and critically assess a specific cinematographic camera movement.",
            "specific_criticism_or_review":"The narration analyzes the precise trailer image composition and explains its storytelling impact.",
            "why_this_exact_clip_is_needed":"The video segment directly illustrates the criticized camera move rather than adding background imagery.",
            "why_this_length_is_proportionate":"Only the exact transition needed to demonstrate the movement is quoted.",
            "source_credit_as_displayed":"Rockstar Games — Grand Theft Auto VI trailer",
            "personality_rights_check":"Check that transformations preserve integrity and attribution.",
            "publisher_policy_check":"Rockstar fan-use policy is narrower than professional/brand promotion.",
            "neighboring_rights_check":"Producer and performer related rights require separate examination.",
            "decorative_only":False,"is_leaked_or_spoiler":False,
            "start_seconds":12.5,"duration_seconds":1.2,
            "editorial_assessment_by":"human editor",
            "commercial_context_legal_analysis":"No direct ad income, but building audience for a branded commercial content channel requires independent context analysis."
        }]
        return out

    def test_original_commercial_ready_but_no_automatic_publish(self):
        result=evaluate(self.own(),today=TODAY)
        self.assertEqual(result["status"],"READY_FOR_OWNER_AND_PLATFORM_REVIEW")
        self.assertIs(result["can_auto_publish"],False)
        self.assertIs(result["platform_monetization_was_changed"],False)

    def test_quoted_game_analysis_requires_human_lawyer_even_when_video_ads_off(self):
        result=evaluate(self.quoted(),today=TODAY)
        self.assertEqual(result["status"],"MANUAL_LEGAL_REVIEW_REQUIRED")
        self.assertTrue(result["manual_actions"])
        self.assertFalse(result["can_auto_publish"])

    def test_youtube_off_must_be_verified_not_just_written(self):
        record=self.quoted()
        record["platform_posts"][0]["control_evidence"]=""
        result=evaluate(record,today=TODAY)
        self.assertEqual(result["status"],"BLOCK")
        self.assertTrue(any("dated evidence" in s for s in result["blockers"]))

    def test_short_platform_revenue_must_not_be_assumed_off(self):
        record=self.quoted()
        record["platform_posts"][0]["format"]="short"
        record["platform_posts"][0]["platform_monetization"]="unknown"
        result=evaluate(record,today=TODAY)
        self.assertEqual(result["status"],"BLOCK")
        self.assertTrue(any("cannot verify" in s for s in result["blockers"]))

    def test_revenue_cta_betrays_unpaid_classification(self):
        record=self.quoted()
        record["platform_posts"][0]["affiliate_links"]=True
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

    def test_commercial_own_category_rejects_third_party_quote(self):
        record=self.quoted()
        record["publication_category"]="owned_commercial"
        record["monetization"]=["affiliate"]
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

    def test_unreviewed_rockstar_footage_stays_blocked_even_with_no_ads(self):
        record=self.quoted()
        record["assets"][0].pop("specific_criticism_or_review")
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

    def test_cross_platform_metadata_required(self):
        record=self.own()
        record["platforms"]=["youtube","instagram"]
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

    def test_unknown_category_cannot_be_assumed_commercial(self):
        record=self.own()
        record.pop("publication_category")
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

    def test_fictional_status_cannot_be_paid_without_declared_monetization(self):
        record=self.own()
        record["monetization"]=["none"]
        self.assertEqual(evaluate(record,today=TODAY)["status"],"BLOCK")

if __name__=="__main__":
    unittest.main()
