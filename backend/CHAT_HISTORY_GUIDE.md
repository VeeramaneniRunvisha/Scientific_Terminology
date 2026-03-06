# Chat History Storage - Quick Reference

## Database Table: `chat_history`

The chat history is stored in the `concept_clarity` MySQL database with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INT (Primary Key) | Auto-increment ID |
| `user_id` | INT (Nullable) | Foreign key to users table |
| `user_email` | VARCHAR(100) | Email of the user |
| `term` | VARCHAR(255) | Scientific term queried |
| `explanation` | VARCHAR(2000) | AI-generated explanation |
| `level` | VARCHAR(50) | Difficulty level (beginner/intermediate/advanced) |
| `timestamp` | VARCHAR(50) | ISO format timestamp |
| `session_id` | VARCHAR(100) | Optional session identifier |

## API Endpoints

### 1. **Automatic Save** (via `/explain`)
When users request explanations, chat history is automatically saved.

**Request:**
```json
POST /explain
{
  "term": "photosynthesis",
  "level": "beginner",
  "user_email": "user@example.com"  // Optional
}
```

### 2. **Manual Save**
```json
POST /chat/save
{
  "term": "gravity",
  "explanation": "Gravity is a force...",
  "level": "intermediate",
  "user_email": "user@example.com",  // Optional
  "session_id": "abc123"  // Optional
}
```

### 3. **Retrieve History**
```
GET /chat/history?user_email=user@example.com&limit=50
```

**Response:**
```json
{
  "count": 10,
  "history": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "term": "photosynthesis",
      "explanation": "...",
      "level": "beginner",
      "timestamp": "2026-01-26T13:40:25.123456",
      "session_id": null
    }
  ]
}
```

### 4. **Get User Sessions**
```
GET /chat/sessions/user@example.com
```

### 5. **Delete Entry**
```
DELETE /chat/delete/1
```

## Frontend Usage

### Check History in Browser Console
```javascript
// Load all chat history
loadChatHistory().then(history => console.table(history));

// Load history for specific user
loadChatHistory('user@example.com').then(history => console.table(history));
```

## MySQL Workbench Queries

### View all chat history
```sql
USE concept_clarity;
SELECT * FROM chat_history ORDER BY id DESC LIMIT 20;
```

### View history for specific user
```sql
SELECT term, level, timestamp 
FROM chat_history 
WHERE user_email = 'user@example.com' 
ORDER BY timestamp DESC;
```

### Count queries by term
```sql
SELECT term, COUNT(*) as query_count 
FROM chat_history 
GROUP BY term 
ORDER BY query_count DESC;
```

### Count queries by difficulty level
```sql
SELECT level, COUNT(*) as count 
FROM chat_history 
GROUP BY level;
```
