from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ServiceRecordRequest(db.Model):
    __tablename__ = "service_record_requests"

    id = db.Column(db.Integer, primary_key=True)
    additional_information = db.Column(db.Text, nullable=True)
    case_reference_number = db.Column(db.String(64), nullable=True)
    date_of_birth = db.Column(db.String(10))
    date_of_death = db.Column(db.String(10), nullable=True)
    died_in_service = db.Column(db.String(8))
    forenames = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    mod_reference = db.Column(db.String(64), nullable=True)
    other_last_names = db.Column(db.String(128), nullable=True)
    place_of_birth = db.Column(db.String(128), nullable=True)
    regiment = db.Column(db.String(128), nullable=True)
    requester_address1 = db.Column(db.String(256))
    requester_address2 = db.Column(db.String(256), nullable=True)
    requester_contact_preference = db.Column(db.String(32))
    requester_country = db.Column(db.String(64))
    requester_county = db.Column(db.String(64), nullable=True)
    requester_email = db.Column(db.String(256))
    requester_first_name = db.Column(db.String(128), nullable=True)
    requester_last_name = db.Column(db.String(128))
    requester_postcode = db.Column(db.String(32), nullable=True)
    requester_title = db.Column(db.String(32), nullable=True)
    requester_town_city = db.Column(db.String(128))
    service_branch = db.Column(db.String(64))
    service_number = db.Column(db.String(64), nullable=True)
    evidence_of_death = db.Column(
        db.String(64), nullable=True
    )  # TODO: Needs to store UUID generated when saving file to S3
    payment_id = db.Column(db.String(64), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
