import requests
import json

# Test the /explain endpoint with user_email
url = "http://127.0.0.1:8000/explain"

# Test 1: With user_email
print("Test 1: Sending request with user_email...")
payload1 = {
    "term": "photosynthesis",
    "level": "beginner",
    "user_email": "test@example.com"
}

try:
    response1 = requests.post(url, json=payload1)
    print(f"Status Code: {response1.status_code}")
    print(f"Response: {json.dumps(response1.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Without user_email (should still work)
print("Test 2: Sending request without user_email...")
payload2 = {
    "term": "gravity",
    "level": "intermediate"
}

try:
    response2 = requests.post(url, json=payload2)
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 3: Check chat history
print("Test 3: Retrieving chat history...")
history_url = "http://127.0.0.1:8000/chat/history?limit=5"

try:
    response3 = requests.get(history_url)
    print(f"Status Code: {response3.status_code}")
    data = response3.json()
    print(f"Total entries: {data['count']}")
    print(f"History entries:")
    for entry in data['history']:
        print(f"  - ID: {entry['id']}, Term: {entry['term']}, Level: {entry['level']}, Email: {entry['user_email']}")
except Exception as e:
    print(f"Error: {e}")
