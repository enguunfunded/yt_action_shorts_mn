# main.py
import os
from dotenv import load_dotenv
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import whisper
from utils.subtitle import write_srt_file, burn_subtitle
from utils.translate_chatgpt import translate_to_mongolian  # NEW
from utils.scene_split import detect_action_scenes


def load_config():
    """ .env файл ачаалж тохиргоо буцаана """
    load_dotenv()

    video_url = os.getenv("VIDEO_URL")
    download_path = os.getenv("DOWNLOAD_PATH", "input")
    output_path = os.getenv("OUTPUT_PATH", "output")

    if not video_url:
        raise ValueError("❌ VIDEO_URL .env дотор оруулаагүй байна!")

    return video_url, download_path, output_path
    
    # --- SETTINGS ---
VIDEO_URL, DOWNLOAD_PATH, OUTPUT_PATH = load_config()
CLIP_COUNT = 10
    
# --- 1. Видео татах ---
def download_video(url, path):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    out_path = stream.download(output_path=path)
    print(f"Downloaded to {out_path}")
    return out_path

# --- 2. Сцен хуваах + action хэсгүүд авах ---
def split_video_to_clips(video_path, output_path, count=10):
    scene_times = detect_action_scenes(video_path)
    os.makedirs(output_path, exist_ok=True)
    clips = []
    for i, (start, end) in enumerate(scene_times[:count]):
        out = os.path.join(output_path, f"clip_{i+1}.mp4")
        ffmpeg_extract_subclip(video_path, start, end, targetname=out)
        clips.append(out)
    return clips

# --- 3. Англи яриаг хөрвүүлж, орчуулж, subtitle болгох ---
def process_clip(clip_path, output_path):
    model = whisper.load_model("base")
    result = model.transcribe(clip_path)
    segments = result['segments']

    translated_lines = []
    for seg in segments:
        start = seg['start']
        end = seg['end']
        text = seg['text']
        translated = translate_to_mongolian(text)
        translated_lines.append((start, end, translated))

    srt_path = clip_path.replace(".mp4", ".srt")
    write_srt_file(srt_path, translated_lines)

    final_path = os.path.join(output_path, os.path.basename(clip_path).replace(".mp4", "_mn.mp4"))
    burn_subtitle(clip_path, srt_path, final_path)
    return final_path

# --- Run Full Process ---
def main():
    video_path = download_video(VIDEO_URL, DOWNLOAD_PATH)
    clips = split_video_to_clips(video_path, OUTPUT_PATH, CLIP_COUNT)

    for clip in clips:
        final = process_clip(clip, OUTPUT_PATH)
        print("✅ Гарсан видео:", final)

if __name__ == "__main__":
    main()
