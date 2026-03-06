from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Test database connection and chat_history table
DATABASE_URL = "mysql+pymysql://root:Runvisha%402005@localhost/concept_clarity"

try:
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        print(f"✅ Connected to database: {result.fetchone()[0]}")
        
        # Check if chat_history table exists
        result = conn.execute(text("SHOW TABLES LIKE 'chat_history'"))
        if result.fetchone():
            print("✅ 'chat_history' table exists")
            
            # Show table structure
            result = conn.execute(text("DESCRIBE chat_history"))
            columns = result.fetchall()
            print("\n📋 Table structure:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
            
            # Count entries
            result = conn.execute(text("SELECT COUNT(*) FROM chat_history"))
            count = result.fetchone()[0]
            print(f"\n📊 Number of chat entries in database: {count}")
            
            # Show recent entries
            if count > 0:
                result = conn.execute(text("""
                    SELECT id, user_email, term, level, timestamp 
                    FROM chat_history 
                    ORDER BY id DESC 
                    LIMIT 5
                """))
                entries = result.fetchall()
                print("\n💬 Recent chat entries:")
                for entry in entries:
                    print(f"  - ID: {entry[0]}, Email: {entry[1]}, Term: {entry[2]}, Level: {entry[3]}, Time: {entry[4]}")
            else:
                print("\n⚠️  No chat entries found in database yet")
        else:
            print("❌ 'chat_history' table does NOT exist")
            print("💡 Run the backend server to create the table automatically")
            
except Exception as e:
    print(f"❌ Database connection error: {e}")
