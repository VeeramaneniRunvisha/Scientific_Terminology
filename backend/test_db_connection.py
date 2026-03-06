from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from main import DATABASE_URL

# Test database connection

try:
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        print(f"✅ Connected to database: {result.fetchone()[0]}")
        
        # Check if users table exists
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        if result.fetchone():
            print("✅ 'users' table exists")
            
            # Count users
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            print(f"📊 Number of users in database: {count}")
            
            # Show all users
            result = conn.execute(text("SELECT id, name, email FROM users"))
            users = result.fetchall()
            if users:
                print("\n👥 Users in database:")
                for user in users:
                    print(f"  - ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
            else:
                print("⚠️  No users found in database")
        else:
            print("❌ 'users' table does NOT exist")
            
except Exception as e:
    print(f"❌ Database connection error: {e}")
