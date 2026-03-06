from sqlalchemy import create_engine, inspect
import sys

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

columns = [col['name'] for col in inspector.get_columns('chat_history')]
print(f"Columns in chat_history: {columns}")

if 'language' in columns:
    print("Language column EXISTS.")
else:
    print("Language column MISSING.")
