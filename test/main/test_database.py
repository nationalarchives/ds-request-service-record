# TODO: Investigate a way to have a separate table/database for testing
# as these are currently using + dropping the local DB

import pytest
from app.lib.db.db_handler import (
    add_service_record_request,
    delete_service_record_request,
    get_service_record_request,
)
from app.lib.db.models import db

from app import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app("config.Test")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@db:5432/postgres_test"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def session(test_app):
    with test_app.app_context():
        yield db.session


def test_add_service_record_request(session):
    record = add_service_record_request(
        {
            "id": "testrecordid123",
            "forenames": "John",
            "last_name": "Doe",
            "requester_email": "john.doe@email.com",
            "died_in_service": "yes",
            "requester_address1": "123 Main St",
            "requester_country": "United Kingdom",
            "requester_contact_preference": "email",
            "service_branch": "british_army",
            "record_hash": "dummyhashvalue",
            "gov_uk_payment_id": "testpaymentid123",
        }
    )
    assert record is not None
    assert record.forenames == "John"
    assert record.requester_email == "john.doe@email.com"


def test_get_service_record_request(session):
    id = "testrecordid123"

    result = get_service_record_request(id=id)
    assert result is not None
    assert result.forenames == "John"
    assert result.requester_email == "john.doe@email.com"


def test_delete_service_record_request(session):
    id = "anothertestid"

    add_service_record_request(
        {
            "id": id,
            "forenames": "John",
            "last_name": "Doe",
            "requester_email": "john.doe@email.com",
            "died_in_service": "yes",
            "requester_address1": "123 Main St",
            "requester_country": "United Kingdom",
            "requester_contact_preference": "email",
            "service_branch": "british_army",
            "record_hash": "dummyhash",
            "gov_uk_payment_id": "anothertestpaymentid",
        }
    )
    record = get_service_record_request(id=id)
    assert record is not None

    delete_service_record_request(record)
    deleted = get_service_record_request(id=id)
    assert deleted is None
