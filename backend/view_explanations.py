from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Fetch last 10 explanations
    results = db.execute(text("SELECT id, term, explanation FROM chat_history ORDER BY id DESC LIMIT 10")).fetchall()
    
    print("Sample Explanations:")
    for r in results:
        print(f"ID: {r[0]}, Term: {r[1]}")
        # Print first 50 chars of explanation
        print(f"Explanation Sample: {r[2][:100]}...")
        
        # Check for Devanagari (range 0x0900–0x097F)
        has_hindi = any('\u0900' <= c <= '\u097f' for c in r[2])
        print(f"Detected Hindi: {has_hindi}")
        print("-" * 20)

finally:
    db.close()
