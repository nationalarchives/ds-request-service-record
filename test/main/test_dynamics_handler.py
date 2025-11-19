import unittest
from datetime import datetime

from app.lib.dynamics_handler import subject_status

from app import create_app


class DummyRecord:
    def __init__(self, date_of_birth, proof_of_death, processing_option):
        self.date_of_birth = date_of_birth
        self.proof_of_death = proof_of_death
        self.processing_option = processing_option


class SubjectStatusTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_age_over_115_sets_FOIOP(self):
        dob = "01 January 1900"
        r = DummyRecord(dob, None, "standard")
        self.assertEqual(subject_status(r), "? FOI DIRECT MOD FOIOP1")

    def test_proof_of_death_sets_FOICD(self):
        recent_year = datetime.now().year - 40
        dob = f"15 June {recent_year}"
        r = DummyRecord(dob, "file.png", "standard")
        self.assertEqual(subject_status(r), "? FOI DIRECT MOD FOICD1")

    def test_no_evidence_sets_FOICDN_standard(self):
        recent_year = datetime.now().year - 30
        dob = f"10 March {recent_year}"
        r = DummyRecord(dob, None, "standard")
        self.assertEqual(subject_status(r), "? FOI DIRECT MOD FOICDN1")

    def test_no_evidence_sets_FOICDN_full(self):
        recent_year = datetime.now().year - 25
        dob = f"20 August {recent_year}"
        r = DummyRecord(dob, None, "full")
        self.assertEqual(subject_status(r), "? FOI DIRECT MOD FOICDN2")


if __name__ == "__main__":
    unittest.main()
