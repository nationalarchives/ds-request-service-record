"""Resize service record request fields.

Revision ID: 20260309_resize_service_record
Revises: None
Create Date: 2026-03-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260309_resize_service_record"
down_revision = None
branch_labels = None
depends_on = None


def _ensure_max_length(conn, table_name, column_name, max_length):
    query = sa.text(
        f'SELECT MAX(LENGTH("{column_name}")) FROM "{table_name}"'
    )
    max_seen = conn.execute(query).scalar()
    if max_seen is not None and max_seen > max_length:
        raise ValueError(
            f"{table_name}.{column_name} has values longer than {max_length}"
        )


def upgrade():
    conn = op.get_bind()

    _ensure_max_length(conn, "service_record_requests", "forenames", 100)
    _ensure_max_length(conn, "service_record_requests", "last_name", 100)
    _ensure_max_length(conn, "service_record_requests", "other_last_names", 100)
    _ensure_max_length(conn, "service_record_requests", "regiment", 100)
    _ensure_max_length(conn, "service_record_requests", "requester_address1", 250)
    _ensure_max_length(conn, "service_record_requests", "requester_address2", 250)
    _ensure_max_length(conn, "service_record_requests", "requester_email", 100)
    _ensure_max_length(conn, "service_record_requests", "requester_first_name", 100)
    _ensure_max_length(conn, "service_record_requests", "requester_last_name", 100)
    _ensure_max_length(conn, "service_record_requests", "requester_town_city", 80)

    op.alter_column(
        "service_record_requests",
        "forenames",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "last_name",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "other_last_names",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "regiment",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "requester_address1",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.VARCHAR(length=250),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_address2",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.VARCHAR(length=250),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "requester_email",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_first_name",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "requester_last_name",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_town_city",
        existing_type=sa.VARCHAR(length=128),
        type_=sa.VARCHAR(length=80),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "service_record_requests",
        "requester_town_city",
        existing_type=sa.VARCHAR(length=80),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_last_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_first_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "requester_email",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=256),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "requester_address2",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.VARCHAR(length=256),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "requester_address1",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.VARCHAR(length=256),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "regiment",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "other_last_names",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=True,
    )
    op.alter_column(
        "service_record_requests",
        "last_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
    )
    op.alter_column(
        "service_record_requests",
        "forenames",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=128),
        existing_nullable=False,
    )
