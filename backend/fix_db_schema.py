from sqlalchemy import create_engine, text
from main import DATABASE_URL

def fix_schema():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            # Add created_at to feedback table
            print("Attempting to add created_at to feedback table...")
            conn.execute(text("ALTER TABLE feedback ADD COLUMN created_at VARCHAR(50)"))
            print("Successfully added created_at to feedback.")
        except Exception as e:
            print(f"Feedback table update skipped/failed (might already exist): {e}")

        try:
            # Add created_at to users table (double check)
            print("Attempting to add created_at to users table...")
            conn.execute(text("ALTER TABLE users ADD COLUMN created_at VARCHAR(50)"))
            print("Successfully added created_at to users.")
        except Exception as e:
             # This is expected if it was done in the previous task
            print(f"User table update skipped/failed: {e}")

        # check if new tables exist
        try:
            result = conn.execute(text("SHOW TABLES LIKE 'quiz_results'"))
            if result.fetchone():
                print("quiz_results table exists.")
            else:
                print("WARNING: quiz_results table MISSING. Run create_tables.py")
        except Exception as e:
             print(f"Error checking tables: {e}")

    print("Schema fix verification complete.")

if __name__ == "__main__":
    fix_schema()
