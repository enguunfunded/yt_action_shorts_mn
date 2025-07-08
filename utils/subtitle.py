# utils/subtitle.py
import pysrt
import subprocess

def write_srt_file(srt_path, segments):
    """
    segments: [(start_sec, end_sec, text), ...]
    """
    subs = pysrt.SubRipFile()
    for idx, (start, end, text) in enumerate(segments, 1):
        sub = pysrt.SubRipItem()
        sub.index = idx
        sub.text = text

        sub.start.seconds = int(start)
        sub.start.milliseconds = int((start - int(start)) * 1000)

        sub.end.seconds = int(end)
        sub.end.milliseconds = int((end - int(end)) * 1000)

        subs.append(sub)
    subs.save(srt_path, encoding='utf-8')
    print(f"📄 SRT хадгалагдлаа: {srt_path}")

def burn_subtitle(video_path, srt_path, output_path):
    """
    ffmpeg ашиглан subtitle видеонд шатаана
    """
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles='{srt_path}':force_style='FontName=Arial,FontSize=28'",
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(command, check=True)
    print(f"🎬 Subtitle шатаасан видео: {output_path}")
