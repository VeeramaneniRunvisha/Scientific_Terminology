import requests
import json
from datetime import datetime, timezone, timedelta

# Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Get current IST time
current_ist = datetime.now(IST)
print(f"Current IST time: {current_ist.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"ISO format: {current_ist.isoformat()}")
print()

# Test the /explain endpoint
url = "http://127.0.0.1:8000/explain"

payload = {
    "term": "timezone_test",
    "level": "beginner",
    "user_email": "test@example.com"
}

print("Sending request to backend...")
try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("✅ Request successful")
        
        # Get the latest entry from chat history
        history_url = "http://127.0.0.1:8000/chat/history?limit=1"
        history_response = requests.get(history_url)
        
        if history_response.status_code == 200:
            data = history_response.json()
            if data['count'] > 0:
                latest = data['history'][0]
                stored_time = latest['timestamp']
                
                print(f"\nStored timestamp: {stored_time}")
                print(f"Current IST time: {current_ist.isoformat()}")
                print()
                
                # Parse and compare
                stored_dt = datetime.fromisoformat(stored_time)
                time_diff = abs((stored_dt - current_ist).total_seconds())
                
                if time_diff < 10:  # Within 10 seconds
                    print("✅ SUCCESS! Timestamp is in IST (matches current time)")
                else:
                    print(f"⚠️  Time difference: {time_diff} seconds")
                    print(f"   Stored: {stored_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   Current: {current_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"❌ Error: {e}")
