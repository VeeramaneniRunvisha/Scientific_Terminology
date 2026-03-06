from main import SessionLocal, Feedback

def check_feedback():
    db = SessionLocal()
    try:
        print("Querying Feedback table...")
        feedbacks = db.query(Feedback).limit(5).all()
        print(f"Success! Found {len(feedbacks)} feedback entries.")
        for f in feedbacks:
            print(f"ID: {f.id}, Created At: {getattr(f, 'created_at', 'MISSING')}")
    except Exception as e:
        print(f"Error querying Feedback: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_feedback()
