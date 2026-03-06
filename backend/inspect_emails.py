from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Check distinct user_emails in ChatHistory
    print("Distinct user_emails in ChatHistory:")
    results = db.execute(text("SELECT DISTINCT user_email FROM chat_history")).fetchall()
    for r in results:
        print(f"'{r[0]}'")

    # Count NULLs
    null_count = db.execute(text("SELECT COUNT(*) FROM chat_history WHERE user_email IS NULL")).scalar()
    print(f"\nNULL count: {null_count}")

    # Count 'guest' string
    guest_str_count = db.execute(text("SELECT COUNT(*) FROM chat_history WHERE user_email = 'guest'")).scalar()
    print(f"'guest' string count: {guest_str_count}")

    # Count total
    total = db.execute(text("SELECT COUNT(*) FROM chat_history")).scalar()
    print(f"Total: {total}")

finally:
    db.close()
