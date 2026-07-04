"""Add sample customers to test the Billing functionality."""
from src.core.db import engine
from sqlmodel import Session
from src.models.sales import Customer
from decimal import Decimal

def add_sample_customers():
    session = Session(engine)

    # Sample customers for a medical store
    sample_customers = [
        {
            "name": "Walk-in Customer",
            "phone": None,
            "email": None,
            "address": None,
            "balance": Decimal("0.00")
        },
        {
            "name": "Dr. Ahmed Khan",
            "phone": "+92-300-1234567",
            "email": "ahmed.khan@hospital.com",
            "address": "123 Medical Plaza, Karachi",
            "balance": Decimal("0.00")
        },
        {
            "name": "City General Hospital",
            "phone": "+92-21-1111222",
            "email": "procurement@citygeneral.com",
            "address": "456 Hospital Road, Lahore",
            "balance": Decimal("0.00")
        },
        {
            "name": "Ali Pharmacy Chain",
            "phone": "+92-42-3456789",
            "email": "orders@alipharmacy.com",
            "address": "789 Main Boulevard, Islamabad",
            "balance": Decimal("0.00")
        },
        {
            "name": "Mrs. Fatima Malik",
            "phone": "+92-333-9876543",
            "email": "fatima.malik@email.com",
            "address": "321 Garden Town, Karachi",
            "balance": Decimal("0.00")
        },
        {
            "name": "Health Care Clinic",
            "phone": "+92-51-8887777",
            "email": "admin@healthcareclinic.pk",
            "address": "555 Medical Center, Rawalpindi",
            "balance": Decimal("0.00")
        }
    ]

    print("Adding sample customers...")
    for customer_data in sample_customers:
        customer = Customer(**customer_data)
        session.add(customer)
        name = customer_data['name']
        phone = customer_data['phone'] or 'N/A'
        print(f"  [+] Added: {name} ({phone})")

    session.commit()

    print(f"\n[SUCCESS] Added {len(sample_customers)} customers to database")
    print("\nYou can now:")
    print("  1. Go to Billing page")
    print("  2. Search for products to add to cart")
    print("  3. Optionally select a customer")
    print("  4. Choose payment method")
    print("  5. Complete sale and generate invoice")

    session.close()

if __name__ == "__main__":
    add_sample_customers()
