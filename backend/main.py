from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from dotenv import load_dotenv
import ml_service

load_dotenv()

# Define IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

app = FastAPI()

# --- JWT Configuration ---
SECRET_KEY = "your-secret-key-change-this-in-production-make-it-long-and-random"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
# Accept legacy hashes and use pbkdf2 as default to avoid bcrypt 4.0+ crashes.
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for easier deployment, restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")

# Render uses 'postgres://', but SQLAlchemy requires 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    # Use MySQL for local development if nothing is set
    DATABASE_URL = "mysql+pymysql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost/concept_clarity"

print(f"[DB] Initializing database...")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))  # Changed to 255 to accommodate bcrypt hashes
    created_at = Column(String(50)) # ISO format timestamp

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), nullable=True)
    term = Column(String(255))
    explanation = Column(String(2000))  # Store longer explanations
    level = Column(String(50))  # beginner, intermediate, advanced
    timestamp = Column(String(50))  # ISO format timestamp

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), index=True)
    rating = Column(Integer)  # 1-5 stars
    comment = Column(String(500), nullable=True)  # Optional comment
    created_at = Column(String(50))  # ISO format timestamp

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), index=True)
    term = Column(String(255))
    score = Column(Integer)
    created_at = Column(String(50))

class VideoLog(Base):
    __tablename__ = "video_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), index=True)
    term = Column(String(255))
    video_id = Column(String(100))
    created_at = Column(String(50))

class ConceptTreeLog(Base):
    __tablename__ = "tree_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), index=True)
    term = Column(String(255))
    created_at = Column(String(50))

# Create tables - This will only create if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Password & JWT Utility Functions ---
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Static explanations (migrated from frontend)
EXPLANATIONS = {
    "photosynthesis": "Photosynthesis is the process by which green plants make their own food using sunlight, water, and carbon dioxide.",
    "gravity": "Gravity is a force that pulls objects toward each other, especially toward the Earth.",
    "atom": "An atom is the smallest unit of matter that makes up everything around us."
}

import re
import requests

def get_related_video(term: str) -> list:
    """Search for related videos on YouTube using requests and regex."""
    try:
        search_query = f"{term} explanation"
        url = f"https://www.youtube.com/results?search_query={search_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        # Regex to find video IDs
        # Look for "videoId":"(videoId)" pattern
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        
        # Return top 3 unique IDs
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)
                if len(unique_ids) >= 3:
                    break
        
        return unique_ids
            
    except Exception as e:
        print(f"Error searching for video: {e}")
    return []

# --- Pydantic Models ---
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str

class TermRequest(BaseModel):
    term: str
    level: str = "beginner"  # Default to beginner if not specified
    user_email: Optional[str] = None  # Optional user email for logged-in users
    language: str = "en"  # Default to English

class ChatSaveRequest(BaseModel):
    term: str
    explanation: str
    level: str = "beginner"
    user_email: Optional[str] = None

class FeedbackRequest(BaseModel):
    user_email: str
    rating: int  # 1-5
    comment: Optional[str] = None

class QuizRequest(BaseModel):
    term: str
    language: str = "en"

class TrackQuizRequest(BaseModel):
    user_email: str
    term: str
    score: int

class TrackVideoRequest(BaseModel):
    user_email: str
    term: str
    video_id: str

class TrackTreeRequest(BaseModel):
    user_email: str
    term: str

class ChatHistoryResponse(BaseModel):
    id: int
    user_email: Optional[str] = None
    term: str
    explanation: str
    level: str
    timestamp: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Scientific Terms Backend - AI Enabled (API)"}

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before storing
    hashed_password = get_password_hash(user.password)
    
    # Save current timestamp
    timestamp = datetime.now(IST).isoformat()
    
    new_user = User(name=user.name, email=user.email, password=hashed_password, created_at=timestamp)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Registration successful", "user": {"name": new_user.name, "email": new_user.email}}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # --- Admin Login Check ---
    if user.email == "admin@gmail.com" and user.password == "Admin@123":
        access_token = create_access_token(data={"sub": user.email, "role": "admin"})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"name": "Admin", "email": user.email, "role": "admin"}
        }

    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify hashed password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": db_user.email, "role": "user"})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"name": db_user.name, "email": db_user.email, "role": "user"}
    }

@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    # In a real app, send email with reset link. For now, we just return success.
    return {"message": "User verified. Please reset your password."}

@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    user.password = get_password_hash(request.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# --- Tracking Endpoints ---

@app.post("/track/quiz")
def track_quiz(request: TrackQuizRequest, db: Session = Depends(get_db)):
    timestamp = datetime.now(IST).isoformat()
    new_result = QuizResult(
        user_email=request.user_email,
        term=request.term,
        score=request.score,
        created_at=timestamp
    )
    db.add(new_result)
    db.commit()
    return {"message": "Quiz result tracked"}

@app.post("/track/video")
def track_video(request: TrackVideoRequest, db: Session = Depends(get_db)):
    timestamp = datetime.now(IST).isoformat()
    new_log = VideoLog(
        user_email=request.user_email,
        term=request.term,
        video_id=request.video_id,
        created_at=timestamp
    )
    db.add(new_log)
    db.commit()
    return {"message": "Video view tracked"}

@app.post("/track/tree")
def track_tree(request: TrackTreeRequest, db: Session = Depends(get_db)):
    timestamp = datetime.now(IST).isoformat()
    new_log = ConceptTreeLog(
        user_email=request.user_email,
        term=request.term,
        created_at=timestamp
    )
    db.add(new_log)
    db.commit()
    return {"message": "Concept tree view tracked"}

# --- Admin Endpoints ---

@app.get("/admin/stats")
@app.get("/admin/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    # 1. Basic Counts
    total_users = db.query(User).count()
    total_explanations = db.query(ChatHistory).count()
    total_feedback = db.query(Feedback).count()
    
    # 2. Avg Rating
    feedbacks = db.query(Feedback).all()
    avg_rating = 0
    if feedbacks:
        total_stars = sum(f.rating for f in feedbacks)
        avg_rating = round(total_stars / len(feedbacks), 1)

    # 3. Pie Chart Data (Registered vs Guest)
    # Assuming guest searches have user_email as None or "guest" (Check your save logic)
    # For now, we count specific emails vs None/Null
    registered_searches = db.query(ChatHistory).filter(ChatHistory.user_email.isnot(None)).count()
    guest_searches = total_explanations - registered_searches

    # 4. Bar Chart Data (Top 5 Terms)
    from sqlalchemy import func, desc
    top_terms_query = db.query(
        ChatHistory.term, func.count(ChatHistory.term).label('count')
    ).group_by(ChatHistory.term).order_by(desc('count')).limit(5).all()
    
    top_terms = [{"term": t[0], "count": t[1]} for t in top_terms_query]

    level_counts = db.query(
        ChatHistory.level, func.count(ChatHistory.level).label('count')
    ).group_by(ChatHistory.level).all()
    
    levels = {l[0]: l[1] for l in level_counts} # e.g., {'beginner': 10, 'advanced': 5}

    # 6. Language Distribution (Inferred from explanation text)
    # We fetch only the explanation text to minimize load, though for large DBs this should be a DB column
    all_explanations = db.query(ChatHistory.explanation).all()
    hindi_count = 0
    english_count = 0
    
    for row in all_explanations:
        text_content = row[0]
        if text_content:
            # Check for Devanagari unicode range (0x0900 - 0x097F)
            if any('\u0900' <= char <= '\u097f' for char in text_content):
                hindi_count += 1
            else:
                english_count += 1
                
    languages = {"English": english_count, "Hindi": hindi_count}

    # 7. Feedback Sentiment
    # Positive: 4-5, Neutral: 3, Negative: 1-2
    sentiment = {"Positive": 0, "Medium": 0, "Negative": 0}
    if feedbacks:
        for f in feedbacks:
            if f.rating >= 4:
                sentiment["Positive"] += 1
            elif f.rating == 3:
                sentiment["Medium"] += 1
            else:
                sentiment["Negative"] += 1

    # 8. Recent Activity (Last 5)
    recent_activity_query = db.query(ChatHistory).order_by(ChatHistory.id.desc()).limit(5).all()
    recent_activity = [
        {"term": r.term, "user": r.user_email or "Guest", "time": r.timestamp} 
        for r in recent_activity_query
    ]
        
    return {
        "total_users": total_users,
        "total_explanations": total_explanations,
        "total_feedback": total_feedback,
        "average_rating": avg_rating,
        "chart_data": {
            "registered": registered_searches,
            "guest": guest_searches,
            "top_terms": top_terms,
            "levels": levels,
            "languages": languages,
            "sentiment": sentiment
        },
        "recent_activity": recent_activity
    }

@app.get("/admin/users")
def get_admin_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    # Handle case where created_at might be None for old users
    return [
        {
            "id": u.id, 
            "name": u.name, 
            "email": u.email,
            "created_at": u.created_at
        } for u in users
    ]

@app.get("/admin/feedback")
def get_admin_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).order_by(Feedback.id.desc()).all()
    return feedbacks

@app.get("/admin/quiz")
def get_admin_quiz(db: Session = Depends(get_db)):
    results = db.query(QuizResult).order_by(QuizResult.id.desc()).all()
    
    # Stats: Avg Score by Term
    from sqlalchemy import func
    stats_query = db.query(
        QuizResult.term, 
        func.avg(QuizResult.score).label('avg_score'),
        func.count(QuizResult.id).label('count')
    ).group_by(QuizResult.term).all()
    
    stats = [{"term": s.term, "avg_score": round(s.avg_score, 1), "count": s.count} for s in stats_query]
    
    # Logs
    logs = [
        {"id": r.id, "user_email": r.user_email, "term": r.term, "score": r.score, "created_at": r.created_at}
        for r in results[:50]  # Limit to 50
    ]
    
    return {"stats": stats, "logs": logs}

@app.get("/admin/comparison")
def get_admin_comparison(days: int = 30, db: Session = Depends(get_db)):
    """
    Get aggregated daily counts for Quiz, YouTube, and Concept Tree usage
    over the last N days.
    """
    end_date = datetime.now(IST)
    start_date = end_date - timedelta(days=days)
    
    # Helper to process query into {date_str: count}
    def get_daily_counts(model):
        results = db.query(model).filter(
            model.created_at >= start_date.isoformat()
        ).all()
        
        counts = {}
        for r in results:
            try:
                # Extract date part YYYY-MM-DD
                date_str = r.created_at.split('T')[0]
                counts[date_str] = counts.get(date_str, 0) + 1
            except:
                pass
        return counts

    quiz_counts = get_daily_counts(QuizResult)
    video_counts = get_daily_counts(VideoLog)
    tree_counts = get_daily_counts(ConceptTreeLog)
    
    # Generate list of all dates in range
    all_dates = []
    current_date = start_date
    while current_date <= end_date:
        all_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
        
    # Align data
    data = {
        "dates": all_dates,
        "quiz": [quiz_counts.get(d, 0) for d in all_dates],
        "video": [video_counts.get(d, 0) for d in all_dates],
        "tree": [tree_counts.get(d, 0) for d in all_dates]
    }
    
    return data

@app.get("/admin/youtube")
def get_admin_youtube(db: Session = Depends(get_db)):
    logs = db.query(VideoLog).order_by(VideoLog.id.desc()).all()
    
    # Stats: Most Watched Terms
    from sqlalchemy import func, desc
    stats_query = db.query(
        VideoLog.term,
        func.count(VideoLog.term).label('count')
    ).group_by(VideoLog.term).order_by(desc('count')).limit(5).all()
    
    stats = [{"term": s[0], "count": s[1]} for s in stats_query]
    
    return {"logs": logs, "stats": stats}

@app.get("/admin/tree")
def get_admin_tree(db: Session = Depends(get_db)):
    logs = db.query(ConceptTreeLog).order_by(ConceptTreeLog.id.desc()).all()
    
    # Stats: Most Generated Trees
    from sqlalchemy import func, desc
    stats_query = db.query(
        ConceptTreeLog.term,
        func.count(ConceptTreeLog.term).label('count')
    ).group_by(ConceptTreeLog.term).order_by(desc('count')).limit(5).all()
    
    stats = [{"term": s[0], "count": s[1]} for s in stats_query]
    
    return {"logs": logs, "stats": stats}

@app.get("/admin/history")
def get_admin_history(db: Session = Depends(get_db)):
    """Fetch all chat history for admin dashboard"""
    # Fetch latest 100 entries to avoid overload, can add pagination later
    history = db.query(ChatHistory).order_by(ChatHistory.id.desc()).limit(100).all()
    
    return [
        {
            "id": h.id,
            "user_email": h.user_email,
            "term": h.term,
            "explanation": h.explanation,
            "level": h.level,
            "timestamp": h.timestamp
        }
        for h in history
    ]

@app.post("/change-password")
def change_password(request: ChangePasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not verify_password(request.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
        
    db_user.password = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@app.post("/explain")
def explain_term(request: TermRequest, db: Session = Depends(get_db)):
    term_key = request.term.lower().strip()
    
    # Try static first (instant) - optional, or remove if user wants pure AI. 
    # User said "Generate ... using simple language" -> Implies AI generation.
    # However, kept static as fallback/cache or just override?
    # Requirement: "Accept a scientific term... Generate a beginner-friendly explanation"
    # I will prioritize AI, but if models fails or is loading, handle gracefully.
    
    explanation = ml_service.generate_explanation(request.term, request.level, request.language)
    
    if explanation:
        # Save to chat history
        try:
            chat_entry = ChatHistory(
                user_email=request.user_email,  # Use email from request
                term=request.term,
                explanation=explanation,
                level=request.level,
                timestamp=datetime.now(IST).isoformat()
            )
            db.add(chat_entry)
            db.commit()
            db.refresh(chat_entry)
        except Exception as e:
            print(f"Error saving chat history: {e}")
            # Don't fail the request if history save fails
        
            # Don't fail the request if history save fails
        
        video_ids = get_related_video(request.term)
        return {"term": request.term, "explanation": explanation, "found": True, "video_ids": video_ids}
    else:
        # Fallback to static or default
        explanation = EXPLANATIONS.get(term_key)
        if explanation:
             return {"term": request.term, "explanation": explanation, "found": True, "source": "static"}
             
        return {
            "term": request.term, 
            "explanation": f"{request.term} is a scientific concept. (Model not available)", 
            "found": False
        }

class QuizRequest(BaseModel):
    term: str
    language: str = "en"
    explanation: Optional[str] = ""

@app.post("/quiz")
def generate_quiz_endpoint(request: QuizRequest, db: Session = Depends(get_db)):
    """Generate 3 MCQs for a term"""
    try:
        quiz_json = ml_service.generate_quiz(request.term, request.language, request.explanation)
        return {"term": request.term, "quiz": quiz_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@app.post("/concept_tree")
def generate_concept_tree_endpoint(request: QuizRequest, db: Session = Depends(get_db)):
    """Generate a concept hierarchy tree"""
    try:
        tree_text = ml_service.generate_concept_tree(request.term, request.language)
        return {"term": request.term, "tree": tree_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tree: {str(e)}")

# --- Chat History Endpoints ---

@app.post("/chat/save")
def save_chat(request: ChatSaveRequest, db: Session = Depends(get_db)):
    """Manually save a chat entry to history"""
    try:
        chat_entry = ChatHistory(
            user_email=request.user_email,
            term=request.term,
            explanation=request.explanation,
            level=request.level,
            timestamp=datetime.now(IST).isoformat()
        )
        db.add(chat_entry)
        db.commit()
        db.refresh(chat_entry)
        
        return {
            "message": "Chat saved successfully",
            "id": chat_entry.id,
            "timestamp": chat_entry.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving chat: {str(e)}")

@app.get("/chat/history")
def get_chat_history(user_email: str = None, limit: int = 50, db: Session = Depends(get_db)):
    """Retrieve chat history, optionally filtered by user email"""
    try:
        query = db.query(ChatHistory)
        
        if user_email:
            query = query.filter(ChatHistory.user_email == user_email)
        
        # Order by most recent first
        history = query.order_by(ChatHistory.id.desc()).limit(limit).all()
        
        return {
            "count": len(history),
            "history": [
                {
                    "id": chat.id,
                    "user_email": chat.user_email,
                    "term": chat.term,
                    "explanation": chat.explanation,
                    "level": chat.level,
                    "timestamp": chat.timestamp
                }
                for chat in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.delete("/chat/delete/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    """Delete a specific chat history entry"""
    try:
        chat_entry = db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
        
        if not chat_entry:
            raise HTTPException(status_code=404, detail="Chat entry not found")
        
        db.delete(chat_entry)
        db.commit()
        
        return {"message": f"Chat entry {chat_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    """Submit user feedback with rating and optional comment"""
    try:
        # Validate rating
        if feedback.rating < 1 or feedback.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Create timestamp in IST
        timestamp = datetime.now(IST).isoformat()
        
        # Create feedback entry
        new_feedback = Feedback(
            user_email=feedback.user_email,
            rating=feedback.rating,
            comment=feedback.comment,
            created_at=timestamp
        )
        
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": new_feedback.id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

