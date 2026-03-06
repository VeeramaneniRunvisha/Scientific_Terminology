from main import SessionLocal, QuizResult, VideoLog, ConceptTreeLog

def show_data():
    db = SessionLocal()
    
    print("\n--- Recent Quiz Results ---")
    quizzes = db.query(QuizResult).order_by(QuizResult.id.desc()).limit(5).all()
    if not quizzes:
        print("No quiz results found.")
    for q in quizzes:
        print(f"ID: {q.id} | User: {q.user_email} | Term: {q.term} | Score: {q.score}% | Date: {q.created_at}")

    print("\n--- Recent Video Logs ---")
    videos = db.query(VideoLog).order_by(VideoLog.id.desc()).limit(5).all()
    if not videos:
        print("No video logs found.")
    for v in videos:
        print(f"ID: {v.id} | User: {v.user_email} | Term: {v.term} | VideoID: {v.video_id} | Date: {v.created_at}")

    print("\n--- Recent Concept Tree Logs ---")
    trees = db.query(ConceptTreeLog).order_by(ConceptTreeLog.id.desc()).limit(5).all()
    if not trees:
        print("No concept tree logs found.")
    for t in trees:
        print(f"ID: {t.id} | User: {t.user_email} | Term: {t.term} | Date: {t.created_at}")
    
    db.close()

if __name__ == "__main__":
    show_data()
