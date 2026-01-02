from datetime import datetime

import pytest
from app.lib.dynamics_handler import subject_status

from app import create_app


class DummyRecord:
    def __init__(self, date_of_birth, proof_of_death, processing_option):
        self.date_of_birth = date_of_birth
        self.proof_of_death = proof_of_death
        self.processing_option = processing_option


@pytest.fixture(scope="module")
def app():
    return create_app("config.Test")


@pytest.fixture()
def context(app):
    with app.app_context():
        yield


def test_age_over_115_sets_FOIOP(context):
    dob = "01 January 1900"
    r = DummyRecord(dob, None, "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOIOP1"


def test_proof_of_death_sets_FOICD(context):
    recent_year = datetime.now().year - 40
    dob = f"15 June {recent_year}"
    r = DummyRecord(dob, "file.png", "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICD1"


def test_no_evidence_sets_FOICDN_standard(context):
    recent_year = datetime.now().year - 30
    dob = f"10 March {recent_year}"
    r = DummyRecord(dob, None, "standard")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN1"


def test_no_evidence_sets_FOICDN_full(context):
    recent_year = datetime.now().year - 25
    dob = f"20 August {recent_year}"
    r = DummyRecord(dob, None, "full")
    assert subject_status(r) == "? FOI DIRECT MOD FOICDN2"
