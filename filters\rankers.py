# filters/ranker.py

import os
from filters.humor_detector import transcribe_audio
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_humor_score(transcript_text):
    prompt = (
        f"Rate the humor level of this transcript from 1 (not funny) to 10 (extremely funny):\n\n"
        f"{transcript_text}\n\n"
        f"Respond ONLY with a number."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    score = response['choices'][0]['message']['content'].strip()
    try:
        return int(score)
    except ValueError:
        return 5  # fallback score

def rank_videos_by_funny(folder_path="downloads/filtered_funny", top_n=5):
    scores = []

    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            file_path = os.path.join(folder_path, file)
            print(f"Scoring: {file}")
            transcript = transcribe_audio(file_path)
            score = get_humor_score(transcript)
            scores.append((file, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

if __name__ == "__main__":
    top5 = rank_videos_by_funny()
    print("\nTop 5 Funniest Videos:")
    for name, score in top5:
        print(f"{name} — Humor Score: {score}")
