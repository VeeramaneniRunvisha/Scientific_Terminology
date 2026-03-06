from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"

Base = declarative_base()

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), index=True)
    term = Column(String(255))
    score = Column(Integer)
    created_at = Column(String(50))

def test_quiz_storage():
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # 1. Inspect columns
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns('quiz_results')]
        print(f"Quiz Table Columns: {columns}")
        
        if 'score' not in columns:
            print("ERROR: 'score' column missing!")
            return

        # 2. Insert dummy record
        timestamp = datetime.now().isoformat()
        new_result = QuizResult(
            user_email="test_worker@example.com",
            term="Test Term",
            score=100,
            created_at=timestamp
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        print(f"Inserted Quiz Log ID: {new_result.id}")
        
        # 3. Read back
        log = db.query(QuizResult).filter(QuizResult.id == new_result.id).first()
        if log:
            print(f"Retrieved: {log.term}, Score: {log.score}")
            
            # 4. Clean up
            db.delete(log)
            db.commit()
            print("Cleaned up test record.")
        else:
            print("Failed to retrieve record.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_quiz_storage()
