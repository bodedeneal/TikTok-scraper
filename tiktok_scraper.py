# scrapers/tiktok_scraper.py

from TikTokApi import TikTokApi
import os
import requests

HASHTAGS = ["funny", "comedy", "meme"]
MAX_DURATION = 30  # in seconds
DOWNLOAD_DIR = "downloads/tiktok"

def download_video(video_url, file_path):
    try:
        response = requests.get(video_url, stream=True)
        with open(file_path, 'wb') as out_file:
            out_file.write(response.content)
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {video_url}: {e}")

def fetch_funny_tiktoks(max_videos=10):
    api = TikTokApi()
    saved = 0
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for tag in HASHTAGS:
        print(f"Searching #{tag}")
        videos = api.hashtag(name=tag).videos(count=max_videos)

        for video in videos:
            try:
                if video.as_dict['video']['duration'] <= MAX_DURATION:
                    url = video.video_url
                    video_id = video.id
                    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
                    download_video(url, file_path)
                    saved += 1

                if saved >= max_videos:
                    break
            except Exception as e:
                print(f"Error processing video: {e}")
    print(f"Total videos downloaded: {saved}")

if __name__ == "__main__":
    fetch_funny_tiktoks(max_videos=5)
