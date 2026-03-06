from sqlalchemy import create_engine, inspect
import os

DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    columns = inspector.get_columns('feedback')
    print("Feedback Table Columns:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    print("\nCheck for created_at in other tables:")
    for table in ['users', 'quiz_results', 'video_logs', 'tree_logs']:
        try:
            cols = inspector.get_columns(table)
            col_names = [c['name'] for c in cols]
            print(f"{table}: {col_names}")
        except Exception as e:
            print(f"Error checking {table}: {e}")

except Exception as e:
    print(f"Connection/Inspection Error: {e}")
