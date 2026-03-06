import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/admin/feedback')
    print(f"Status: {response.status_code}")
    # Print formatted JSON
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
