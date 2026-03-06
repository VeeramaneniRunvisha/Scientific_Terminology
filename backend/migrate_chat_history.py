"""
Database Migration Script
Drops user_id and session_id columns from chat_history table
"""
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("🔄 Starting database migration...")
        print("=" * 50)
        
        # Check if columns exist before dropping
        result = conn.execute(text("DESCRIBE chat_history"))
        columns = [row[0] for row in result.fetchall()]
        print(f"Current columns: {', '.join(columns)}")
        print()
        
        # Drop user_id column if it exists
        if 'user_id' in columns:
            print("Dropping 'user_id' column...")
            conn.execute(text("ALTER TABLE chat_history DROP COLUMN user_id"))
            conn.commit()
            print("✅ 'user_id' column dropped successfully")
        else:
            print("⚠️  'user_id' column does not exist, skipping")
        
        # Drop session_id column if it exists
        if 'session_id' in columns:
            print("Dropping 'session_id' column...")
            conn.execute(text("ALTER TABLE chat_history DROP COLUMN session_id"))
            conn.commit()
            print("✅ 'session_id' column dropped successfully")
        else:
            print("⚠️  'session_id' column does not exist, skipping")
        
        print()
        print("=" * 50)
        print("🎉 Migration completed successfully!")
        print()
        
        # Show updated table structure
        result = conn.execute(text("DESCRIBE chat_history"))
        columns_after = result.fetchall()
        print("📋 Updated table structure:")
        for col in columns_after:
            print(f"  - {col[0]} ({col[1]})")
        
except Exception as e:
    print(f"❌ Migration error: {e}")
    print("\nIf you see 'Can't DROP...check that column/key exists', it means the columns were already removed.")
