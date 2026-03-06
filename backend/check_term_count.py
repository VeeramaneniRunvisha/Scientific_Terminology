from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    term = "genetics"
    
    # Exact match
    count = db.execute(text("SELECT COUNT(*) FROM chat_history WHERE term = :term"), {"term": term}).scalar()
    print(f"Exact match count for '{term}': {count}")
    
    # Case-insensitive match check (just to be sure)
    count_lower = db.execute(text("SELECT COUNT(*) FROM chat_history WHERE LOWER(term) = :term"), {"term": term}).scalar()
    print(f"Case-insensitive count for '{term}': {count_lower}")

finally:
    db.close()
