import re
import requests

def get_related_video(term: str) -> str:
    print(f"Searching for: {term} explanation")
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
        
        if video_ids:
            print(f"Found {len(video_ids)} videos. Top result: {video_ids[0]}")
            return video_ids[0]
        else:
            print("No videos found.")
            
    except Exception as e:
        print(f"Error searching for video: {e}")
    return None

if __name__ == "__main__":
    get_related_video("gravity")
