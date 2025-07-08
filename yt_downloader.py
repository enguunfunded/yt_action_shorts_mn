# yt_downloader.py
import yt_dlp
import os

def download_youtube_video(url: str, output_dir: str = "input"):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\n📥 Татаж байна: {url}")
        ydl.download([url])
        print("✅ Таталт дууслаа.")

if __name__ == "__main__":
    video_url = input("YouTube видеоны линк оруулна уу: ")
    download_youtube_video(video_url)
