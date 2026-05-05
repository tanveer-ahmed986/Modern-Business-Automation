"""
Migration script to update Settings table schema.
Adds created_at, updated_at fields and renames currency_symbol to currency.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add backend/src to path
backend_src = Path(__file__).parent.parent
if str(backend_src) not in sys.path:
    sys.path.insert(0, str(backend_src))

import sqlite3
from src.core.db import engine


def migrate_settings_table():
    """Migrate Settings table to new schema."""

    print("[*] Starting Settings table migration...")

    # Get database path from engine
    db_path = str(engine.url).replace("sqlite:///", "")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if settings table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='settings'
        """)
        if not cursor.fetchone():
            print("[!] Settings table not found - skipping migration")
            conn.close()
            return

        # Get current columns
        cursor.execute("PRAGMA table_info(settings)")
        columns = {row[1]: row for row in cursor.fetchall()}
        column_names = set(columns.keys())

        print(f"[*] Current columns: {column_names}")

        # Track what needs to be done
        needs_migration = False

        # Check if currency_symbol exists (old schema)
        if "currency_symbol" in column_names:
            print("[!] Found old 'currency_symbol' column - needs rename to 'currency'")
            needs_migration = True

        # Check if created_at exists
        if "created_at" not in column_names:
            print("[!] Missing 'created_at' column - needs to be added")
            needs_migration = True

        # Check if updated_at exists
        if "updated_at" not in column_names:
            print("[!] Missing 'updated_at' column - needs to be added")
            needs_migration = True

        if not needs_migration:
            print("[+] Settings table schema is up to date!")
            conn.close()
            return

        # Perform migration using SQLite ALTER TABLE
        print("[*] Performing schema migration...")

        # Step 1: Add new columns if they don't exist
        if "created_at" not in column_names:
            print("    [*] Adding 'created_at' column...")
            cursor.execute(f"""
                ALTER TABLE settings
                ADD COLUMN created_at TIMESTAMP DEFAULT '{datetime.utcnow().isoformat()}'
            """)

        if "updated_at" not in column_names:
            print("    [*] Adding 'updated_at' column...")
            cursor.execute(f"""
                ALTER TABLE settings
                ADD COLUMN updated_at TIMESTAMP DEFAULT '{datetime.utcnow().isoformat()}'
            """)

        # Step 2: Handle currency_symbol -> currency rename
        if "currency_symbol" in column_names and "currency" not in column_names:
            print("    [*] Renaming 'currency_symbol' to 'currency'...")

            # SQLite doesn't support RENAME COLUMN directly in old versions
            # So we use ALTER TABLE ... RENAME COLUMN syntax (supported in SQLite 3.25+)
            try:
                cursor.execute("""
                    ALTER TABLE settings
                    RENAME COLUMN currency_symbol TO currency
                """)
            except sqlite3.OperationalError:
                # Fallback for older SQLite versions - recreate table
                print("    [!] Direct rename not supported, using table recreation...")

                # Get all data
                cursor.execute("SELECT * FROM settings")
                rows = cursor.fetchall()

                # Get column info
                cursor.execute("PRAGMA table_info(settings)")
                old_columns = cursor.fetchall()

                # Create new table with correct schema
                cursor.execute("""
                    CREATE TABLE settings_new (
                        id INTEGER PRIMARY KEY DEFAULT 1,
                        business_name VARCHAR NOT NULL DEFAULT 'My Business',
                        address VARCHAR,
                        phone VARCHAR,
                        email VARCHAR,
                        tax_rate FLOAT NOT NULL DEFAULT 0.0,
                        currency VARCHAR NOT NULL DEFAULT 'PKR',
                        feature_flags JSON NOT NULL DEFAULT '{}',
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL
                    )
                """)

                # Copy data with column mapping
                now = datetime.utcnow().isoformat()
                for row in rows:
                    # Map old columns to new
                    # Assuming order: id, business_name, address, phone, email, tax_rate, currency_symbol, feature_flags
                    cursor.execute("""
                        INSERT INTO settings_new
                        (id, business_name, address, phone, email, tax_rate, currency, feature_flags, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row[0],  # id
                        row[1],  # business_name
                        row[2] if len(row) > 2 else None,  # address
                        row[3] if len(row) > 3 else None,  # phone
                        row[4] if len(row) > 4 else None,  # email
                        row[5] if len(row) > 5 else 0.0,   # tax_rate
                        row[6] if len(row) > 6 else 'PKR', # currency (was currency_symbol)
                        row[7] if len(row) > 7 else '{}',  # feature_flags
                        now,  # created_at
                        now   # updated_at
                    ))

                # Drop old table and rename new one
                cursor.execute("DROP TABLE settings")
                cursor.execute("ALTER TABLE settings_new RENAME TO settings")

        # Commit changes
        conn.commit()
        print("[+] Migration completed successfully!")

        # Verify new schema
        cursor.execute("PRAGMA table_info(settings)")
        new_columns = {row[1]: row for row in cursor.fetchall()}
        print(f"[+] New columns: {set(new_columns.keys())}")

        conn.close()

    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    migrate_settings_table()
