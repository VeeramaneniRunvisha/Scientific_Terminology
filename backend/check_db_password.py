from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, DATABASE_URL

# Setup DB connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("-" * 30)
print("USER PASSWORD HASH CHECKER")
print("-" * 30)

email = input("Enter the email address to check: ")
user = session.query(User).filter(User.email == email).first()

if user:
    print(f"\nUser Found:")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Current Password Hash: {user.password}")
    print("\n(Note: This is a secure hash. If you change the password, this string will change.)")
else:
    print(f"\nNo user found with email: {email}")

session.close()
