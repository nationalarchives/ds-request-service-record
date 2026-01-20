"""
Standalone script to create a test payment entry in the service_record_requests table.
This is useful for testing the /request-submitted/<id> page (and any others that rely on DB interaction) in Playwright tests.

Usage:
    poetry run python create_test_payment.py
"""

import argparse
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.lib.db.models import ServiceRecordRequest, db
from app.lib.db.constants import PAID_STATUS, SENT_STATUS, NEW_STATUS

# Database connection - matches docker-compose.yml
# Inside Docker, use 'db' as hostname (the service name)
# Outside Docker, use 'localhost' (requires port mapping)
DATABASE_URI = "postgresql://postgres:postgres@db:5432/postgres"


def create_test_payment(custom_id=None, status=PAID_STATUS):
    """
    Create a test payment entry in the database.
    
    Args:
        custom_id: Optional custom ID for the record. If not provided, uses default test ID.
        status: Status of the record (default: PAID_STATUS)
                - PAID_STATUS: Creates a successful paid record with payment details
                - NEW_STATUS: Creates a failed payment with only gov_uk_payment_id
    
    Returns:
        dict with 'id', 'payment_reference', and 'status' of the created record
    """
    # Create database engine and session
    engine = create_engine(DATABASE_URI)
    
    # Ensure tables exist
    db.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Use consistent test IDs based on status
        if status == NEW_STATUS:
            record_id = custom_id or "playwright-test-payment-failed-001"
            payment_ref = None
            is_failed = True
        else:
            record_id = custom_id or "playwright-test-payment-001"
            payment_ref = "TEST-REF-2024-001"
            is_failed = False
        
        # Create a hash based on the record ID for uniqueness
        record_hash = hashlib.sha256(record_id.encode()).hexdigest()
        
        # Delete existing record with same ID if it exists (for re-running tests)
        existing = session.get(ServiceRecordRequest, record_id)
        if existing:
            session.delete(existing)
            session.commit()
        
        # Base record data (always required)
        record_data = {
            "id": record_id,
            "forenames": "Robert",
            "last_name": "Playwright",
            "date_of_birth": "15 June 1914",
            "date_of_death": "01 January 1998",
            "died_in_service": "no",
            "service_branch": "british_army",
            "service_number": "12345678",
            "place_of_birth": "London",
            "regiment": "Royal Engineers",
            "requester_first_name": "Francis",
            "requester_last_name": "Palgrave",
            "requester_email": "test@example.com",
            "requester_address1": "123 Test Street",
            "requester_town_city": "London",
            "requester_postcode": "SW1A 1AA",
            "requester_country": "United Kingdom",
            "requester_contact_preference": "email",
            "processing_option": "standard",
            "delivery_type": "email",
            "gov_uk_payment_id": "gov-uk-pay-test-failed-001" if is_failed else "gov-uk-pay-test-001",
            "record_hash": record_hash,
            "status": status,
            "additional_information": "Test record created for Playwright testing"
        }
        
        # Add payment details only for successful payments
        if not is_failed:
            record_data.update({
                "payment_reference": payment_ref,
                "amount_received": "42.25",
                "provider_id": "provider-test-001",
                "payment_date": "15 January 2024",
            })
        
        record = ServiceRecordRequest(**record_data)

        session.add(record)
        session.commit()

        result = {
            "id": record_id,
            "payment_reference": payment_ref,
            "status": status
        }
        return result

    except Exception as e:
        session.rollback()
        print(f"Error creating test payment: {e}")
        raise
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(
        description="Create test payment entries for Playwright testing"
    )
    parser.add_argument(
        "--id",
        type=str,
        help="Custom ID for the test record (optional, uses defaults if not provided)"
    )
    parser.add_argument(
        "--status",
        type=str,
        choices=["P", "S", "N"],
        help="Status of the record: P=Paid, S=Sent, N=New/Failed (creates both by default)"
    )
    parser.add_argument(
        "--only-failed",
        action="store_true",
        help="Create only the failed payment record"
    )
    parser.add_argument(
        "--only-paid",
        action="store_true",
        help="Create only the successful paid record"
    )

    args = parser.parse_args()

    print(f"Database: {DATABASE_URI}")
    print("=" * 70)

    records = []
    
    # Determine which records to create
    if args.status:
        # Create single record with specified status
        result = create_test_payment(custom_id=args.id, status=args.status)
        records.append(result)
        print(f"\n✅ Created 1 test record")
        print(f"   ID: {result['id']}")
        print(f"   Payment Reference: {result['payment_reference'] or 'N/A (failed payment)'}")
        print(f"   Status: {result['status']}")
    elif args.only_failed:
        # Create only failed payment
        result = create_test_payment(custom_id=args.id, status=NEW_STATUS)
        records.append(result)
        print(f"\n✅ Created failed payment record")
        print(f"   ID: {result['id']}")
        print(f"   Status: {result['status']} (NEW/Failed)")
    elif args.only_paid:
        # Create only paid payment
        result = create_test_payment(custom_id=args.id, status=PAID_STATUS)
        records.append(result)
        print(f"\n✅ Created paid payment record")
        print(f"   ID: {result['id']}")
        print(f"   Payment Reference: {result['payment_reference']}")
        print(f"   Status: {result['status']} (PAID)")
    else:
        # Default: Create both paid and failed records
        print("Creating both successful and failed payment records...\n")
        
        # Create successful payment
        paid_result = create_test_payment(status=PAID_STATUS)
        records.append(paid_result)
        print(f"✅ Paid payment record:")
        print(f"   ID: {paid_result['id']}")
        print(f"   Payment Reference: {paid_result['payment_reference']}")
        print(f"   Status: {paid_result['status']}")
        print(f"   Test URL: http://localhost:65517/request-a-military-service-record/request-submitted/{paid_result['id']}")
        
        print()
        
        # Create failed payment
        failed_result = create_test_payment(status=NEW_STATUS)
        records.append(failed_result)
        print(f"✅ Failed payment record:")
        print(f"   ID: {failed_result['id']}")
        print(f"   Payment Reference: N/A (failed payment)")
        print(f"   Status: {failed_result['status']}")
        print(f"   Note: Should redirect to start (no payment completed)")
    
    print("\n" + "=" * 70)
    print(f"✅ Created {len(records)} test record(s) total")


if __name__ == "__main__":
    main()
