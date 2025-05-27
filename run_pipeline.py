# pipeline/run_pipeline.py

import os
from scrapers.tiktok_scraper import scrape_tiktok_videos
from filters.humor_detector import transcribe_audio, is_video_funny
import shutil

RAW_DIR = "downloads/tiktok"
FUNNY_DIR = "downloads/filtered_funny"

def pipeline():
    os.makedirs(FUNNY_DIR, exist_ok=True)

    print("Step 1: Scraping TikTok...")
    scrape_tiktok_videos()  # downloads videos to RAW_DIR

    print("Step 2: Filtering funny videos...")
    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".mp4"):
            file_path = os.path.join(RAW_DIR, filename)

            try:
                transcript = transcribe_audio(file_path)
                funny, reason = is_video_funny(transcript)
                print(f"Video: {filename} | Funny: {funny} | Reason: {reason}")

                if funny:
                    shutil.copy(file_path, os.path.join(FUNNY_DIR, filename))
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    pipeline()
