import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ServiceRecordRequest(db.Model):
    """
    Table to store requests for service records (for the initial payment/form)
    """

    __tablename__ = "service_record_requests"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    additional_information = db.Column(db.Text, nullable=True)
    case_reference_number = db.Column(db.String(64), nullable=True)
    date_of_birth = db.Column(db.String(10))
    date_of_death = db.Column(db.String(10), nullable=True)
    died_in_service = db.Column(db.String(8))
    forenames = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    mod_reference = db.Column(db.String(64), nullable=True)
    catalogue_reference = db.Column(db.String(64), nullable=True)
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
    requester_town_city = db.Column(db.String(128))
    service_branch = db.Column(db.String(64))
    service_number = db.Column(db.String(64), nullable=True)
    evidence_of_death = db.Column(db.String(64), nullable=True)
    payment_id = db.Column(db.String(64), nullable=True, unique=True)
    provider_id = db.Column(db.String(64), nullable=True)
    payment_date = db.Column(db.DateTime, nullable=True)
    delivery_type = db.Column(db.String(32), nullable=True)
    processing_option = db.Column(db.String(32), nullable=True)
    payment_reference = db.Column(db.String(64), nullable=True)
    amount_received = db.Column(db.Integer, nullable=True)  # amount in pence
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class DynamicsPayment(db.Model):
    """
    Table to store payment requests sent by Dynamics for payees to pay for record copying
    """

    __tablename__ = "dynamics_payments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_number = db.Column(db.String(64), nullable=False)
    reference = db.Column(db.String(64), nullable=False)
    net_amount = db.Column(db.Integer, nullable=False)  # amount in pence
    delivery_amount = db.Column(
        db.Integer, nullable=True
    )  # postage/delivery amount in pence
    total_amount = db.Column(db.Integer, nullable=False)  # total amount in pence
    payee_email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    details = db.Column(db.String(256), nullable=True)
    status = db.Column(
        db.String(1), nullable=False, default="N"
    )  # N=New, S=Sent, P=Paid
    provider_id = db.Column(
        db.String(64), nullable=True
    )  # GOV.UK Pay payment ID if paid
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class GOVUKDynamicsPayment(db.Model):
    """
    Table to store GOV.UK Pay payment attempts for Dynamics payment requests
    """

    __tablename__ = "gov_uk_dynamics_payments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dynamics_payment_id = db.Column(
        db.String(36), db.ForeignKey("dynamics_payments.id"), nullable=False
    )
    gov_uk_payment_id = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
