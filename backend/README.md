# Concept Clarity - Backend

FastAPI backend for the Concept Clarity application with AI-powered scientific term explanations and chat history storage.

## Features

- 🔐 User authentication (register/login with JWT)
- 🤖 AI-powered explanations using Hugging Face API
- 📊 Multi-level explanations (Beginner, Intermediate, Advanced)
- 💾 Chat history storage in MySQL database
- 🔍 RESTful API endpoints

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create/update `.env` file:
```
HF_API_TOKEN=your_hugging_face_token
HF_MODEL=meta-llama/Llama-3.2-3B-Instruct
```

### 3. Database Setup

Make sure MySQL is running and create the database:
```sql
CREATE DATABASE concept_clarity;
```

Update database credentials in `main.py` if needed (line 37):
```python
DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost/concept_clarity"
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

Server will be available at `http://127.0.0.1:8000`

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user (returns JWT token)

### Explanations
- `POST /explain` - Get AI explanation for a term
  ```json
  {
    "term": "photosynthesis",
    "level": "beginner",
    "user_email": "user@example.com"  // optional
  }
  ```

### Chat History
- `POST /chat/save` - Manually save chat entry
- `GET /chat/history?user_email=...&limit=50` - Get chat history
- `DELETE /chat/delete/{id}` - Delete chat entry

## Database Schema

### users
- id, name, email, password

### chat_history
- id, user_email, term, explanation, level, timestamp

## Testing

### Test Database Connection
```bash
python test_db_connection.py
```

### Test Chat History
```bash
python test_chat_history.py
```

### Test API Endpoints
```bash
python test_api_endpoints.py
```

### Test User Email Storage
```bash
python test_user_email_storage.py
```

## Files

- `main.py` - Main FastAPI application
- `ml_service.py` - AI service for generating explanations
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys)
- `download_model.py` - Script to download AI models (if using local models)
- `migrate_chat_history.py` - Database migration script
- `CHAT_HISTORY_GUIDE.md` - Detailed chat history usage guide

## Troubleshooting

### User email not saving?
Make sure you're logged in. The app extracts email from `localStorage.getItem('user')`.

### Database connection error?
Check MySQL is running and credentials in `main.py` are correct.

### AI not responding?
Verify your Hugging Face API token in `.env` is valid.

## Documentation

See `CHAT_HISTORY_GUIDE.md` for detailed chat history API usage and SQL queries.
