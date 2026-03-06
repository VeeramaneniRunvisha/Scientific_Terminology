from sqlalchemy import create_engine, text
from main import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    try:
        connection.execute(text("ALTER TABLE users ADD COLUMN created_at VARCHAR(50);"))
        print("Successfully added 'created_at' column to 'users' table.")
    except Exception as e:
        print(f"Error (column might already exist): {e}")
