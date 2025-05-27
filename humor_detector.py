# filters/humor_detector.py

import openai
import subprocess
import os

openai.api_key = "YOUR_API_KEY"  # Load from environment or config in production

def transcribe_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    
    # Convert video to audio
    subprocess.run(["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1", audio_path, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Use Whisper to transcribe audio
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    os.remove(audio_path)  # Clean up
    return transcript['text']

def is_video_funny(transcript_text):
    prompt = f"Here is a transcript of a short video: '{transcript_text}'. Is this likely to be funny? Respond with 'Yes' or 'No' and give a short reason."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a humor detector AI."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response['choices'][0]['message']['content']
    return "Yes" in answer, answer

if __name__ == "__main__":
    video_file = "downloads/tiktok/example.mp4"
    transcript = transcribe_audio(video_file)
    is_funny, reason = is_video_funny(transcript)
    print(f"Funny: {is_funny} – Reason: {reason}")
