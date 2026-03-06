from sqlalchemy import create_engine
from main import Base, DATABASE_URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("Tracking tables created successfully.")
