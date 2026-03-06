import requests
import json

# Test the /explain endpoint to verify user_email is being stored
url = "http://127.0.0.1:8000/explain"

print("Testing user_email storage...")
print("=" * 50)

# Test with user_email
payload = {
    "term": "atom",
    "level": "beginner",
    "user_email": "testuser@example.com"
}

print(f"Sending request with user_email: {payload['user_email']}")
print(f"Term: {payload['term']}")
print()

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Explanation generated successfully")
        print(f"Term: {data['term']}")
        print(f"Explanation preview: {data['explanation'][:100]}...")
        print()
        
        # Now check if it was saved with user_email
        print("Checking database for saved entry...")
        history_url = "http://127.0.0.1:8000/chat/history?limit=1"
        history_response = requests.get(history_url)
        
        if history_response.status_code == 200:
            history_data = history_response.json()
            if history_data['count'] > 0:
                latest_entry = history_data['history'][0]
                print(f"Latest entry in database:")
                print(f"  - ID: {latest_entry['id']}")
                print(f"  - Term: {latest_entry['term']}")
                print(f"  - User Email: {latest_entry['user_email']}")
                print(f"  - Level: {latest_entry['level']}")
                print(f"  - Timestamp: {latest_entry['timestamp']}")
                
                if latest_entry['user_email'] == payload['user_email']:
                    print()
                    print("✅ SUCCESS: user_email is being stored correctly!")
                else:
                    print()
                    print(f"⚠️  WARNING: Expected email '{payload['user_email']}' but got '{latest_entry['user_email']}'")
            else:
                print("⚠️  No entries found in database")
    else:
        print(f"❌ Error: {response.json()}")
        
except Exception as e:
    print(f"❌ Error: {e}")
