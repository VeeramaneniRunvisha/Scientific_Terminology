from youtubesearchpython import VideosSearch
import json

try:
    print("Searching for 'gravity explanation'...")
    videosSearch = VideosSearch('gravity explanation', limit = 1)
    result = videosSearch.result()
    print("Result obtained.")
    print(json.dumps(result, indent=2))
    
    if result['result']:
        print(f"Video ID: {result['result'][0]['id']}")
    else:
        print("No results found.")
except Exception as e:
    print(f"Error: {e}")
