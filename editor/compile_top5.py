# editor/compile_top5.py

import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from filters.ranker import rank_videos_by_funny

FUNNY_DIR = "downloads/filtered_funny"
OUTPUT_FILE = "outputs/top5_funny_compilation.mp4"

def add_label_to_clip(clip, label_text):
    txt_clip = TextClip(label_text, fontsize=70, color='white', font="Arial-Bold")
    txt_clip = txt_clip.set_position(('center', 'top')).set_duration(clip.duration)
    return CompositeVideoClip([clip, txt_clip])

def compile_top5_video():
    top5 = rank_videos_by_funny(FUNNY_DIR, top_n=5)
    final_clips = []

    for idx, (filename, _) in enumerate(top5):
        path = os.path.join(FUNNY_DIR, filename)
        video = VideoFileClip(path).subclip(0, min(30, VideoFileClip(path).duration))

        label = f"#{5 - idx}"
        labeled_clip = add_label_to_clip(video, label)
        final_clips.append(labeled_clip)

    final_video = concatenate_videoclips(final_clips, method="compose")
    os.makedirs("outputs", exist_ok=True)
    final_video.write_videofile(OUTPUT_FILE, fps=24)

if __name__ == "__main__":
    compile_top5_video()
