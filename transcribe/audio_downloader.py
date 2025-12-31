import yt_dlp
import uuid
import os

def download_audio(youtube_url):
    # Create temp folder if missing
    os.makedirs("temp", exist_ok=True)

    # Unique filename
    file_id = str(uuid.uuid4())
    output_path = f"temp/{file_id}.wav"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"temp/{file_id}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_path
