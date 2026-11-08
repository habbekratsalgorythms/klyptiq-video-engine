"""The quote-law audit never equates a checkbox with legal permission."""
import copy
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from publication_rights_preflight import inspect_release

class QuoteGateTests(unittest.TestCase):
    def setUp(self):
        self.base={
            "content_id":"KLYPTIQ-SELF-001",
            "render_sha256":"a"*64,
            "review_date":date.today().isoformat(),
            "platforms":["instagram","tiktok","youtube"],
            "monetization":["affiliate"],
            "original_commentary_description":"An original, informative hardware review using original home-studio camera footage.",
            "facts_verified":True,
            "audio_sources_checked":True,
            "owner_release_approved":True,
            "assets":[{"rights_basis":"own_original","creator":"Klyptiq Gaming",
                       "source_url":"internal://owned/hardware-demo",
                       "lawfully_disclosed":True,"own_work_verified":True}]
        }

    def test_original_can_be_prepared_but_never_machine_approved(self):
        verdict=inspect_release(self.base)
        self.assertEqual(verdict["status"],"READY_FOR_FINAL_HUMAN_REVIEW")
        self.assertFalse(verdict["machine_publish_approved"])

    def test_missing_or_expired_review_blocks(self):
        record=copy.deepcopy(self.base);record["review_date"]="2025-01-01"
        self.assertEqual(inspect_release(record)["status"],"BLOCK")
        record=copy.deepcopy(self.base);record["render_sha256"]=""
        self.assertEqual(inspect_release(record)["status"],"BLOCK")

    def test_rockstar_trailer_with_only_credit_is_blocked(self):
        record=copy.deepcopy(self.base)
        record["assets"]=[{"creator":"Rockstar Games",
             "source_url":"https://www.rockstargames.com/VI/media/videos",
             "rights_basis":"quote_article_15a", "lawfully_disclosed":True,
             "source_credit_as_displayed":"Rockstar Games"}]
        result=inspect_release(record)
        self.assertEqual(result["status"],"BLOCK")
        self.assertTrue(any("specific_criticism_or_review" in x for x in result["blockers"]))

    def test_fully_documented_quote_still_requires_human_legal_decision(self):
        record=copy.deepcopy(self.base)
        record["assets"]=[{"creator":"Rockstar Games",
             "source_url":"https://www.rockstargames.com/VI/media/videos",
             "rights_basis":"quote_article_15a","lawfully_disclosed":True,
             "quote_purpose":"Specifieke kritiek op de cameramontage van de trailer",
             "specific_criticism_or_review":"We bespreken precies de framing van het in beeld gebrachte shot en het verband met de dialoog.",
             "why_this_exact_clip_is_needed":"Het commentaar bespreekt de concrete camerabeweging die alleen met dit shot goed uit te leggen is.",
             "why_this_length_is_proportionate":"Een zeer kort fragment toont de besproken overgang en niets anders.",
             "source_credit_as_displayed":"Rockstar Games — officiële GTA VI trailer",
             "personality_rights_check":"Persoonlijkheidsrechten en context beoordeeld.",
             "publisher_policy_check":"Rockstar noncommercial fanbeleid is geen commerciële toestemming.",
             "neighboring_rights_check":"Naburige rechten van audiovisuele opname afzonderlijk bekeken.",
             "decorative_only":False,"is_leaked_or_spoiler":False,
             "start_seconds":12.5,"duration_seconds":1.5,
             "editorial_assessment_by":"redacteur",
             "commercial_context_legal_analysis":"Voor affiliate monetisatie is een afzonderlijke gedocumenteerde juridische toets nodig; die is hier hypothetisch."}]
        result=inspect_release(record)
        self.assertEqual(result["status"],"HUMAN_LEGAL_DECISION_REQUIRED")
        self.assertFalse(result["machine_publish_approved"])

    def test_generic_visual_decoration_must_not_qualify(self):
        record=copy.deepcopy(self.base)
        record["assets"]=[{"creator":"Rockstar Games","source_url":"https://www.rockstargames.com/VI/media/videos",
             "rights_basis":"quote_article_15a","lawfully_disclosed":True,"decorative_only":True}]
        result=inspect_release(record)
        self.assertTrue(any("decorative" in x for x in result["blockers"]))

    def test_licensed_asset_must_cover_platform_and_use(self):
        record=copy.deepcopy(self.base)
        record["assets"]=[{"creator":"Rights Holder","source_url":"https://example.com/licensed-clip",
            "rights_basis":"licensed_commercial","lawfully_disclosed":True,
            "license_evidence":"License agreement stored as record XYZ",
            "licensed_platforms":["youtube"],"licensed_monetization":["none"]}]
        result=inspect_release(record)
        self.assertEqual(result["status"],"BLOCK")
        self.assertTrue(any("license" in x for x in result["blockers"]))

if __name__=="__main__":
    unittest.main()
