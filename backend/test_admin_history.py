import requests
import json

API_URL = "http://127.0.0.1:8000"

if __name__ == "__main__":
    print(f"Testing GET {API_URL}/admin/history...")
    try:
        response = requests.get(f"{API_URL}/admin/history")
        
        if response.status_code == 200:
            history = response.json()
            print(f"Success! Retrieved {len(history)} chat history entries.")
            if len(history) > 0:
                print("First entry ID:", history[0]['id'])
                print("First entry Term:", history[0]['term'])
            else:
                print("History is empty.")
        else:
            print(f"Failed. Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
