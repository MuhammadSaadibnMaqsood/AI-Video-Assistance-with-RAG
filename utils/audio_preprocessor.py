import os
import sys

if sys.platform == "win32":
    import winreg
    try:
        registry_paths = []
        for hive, subkey in [
            (winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Control\Session Manager\Environment"),
            (winreg.HKEY_CURRENT_USER, r"Environment")
        ]:
            try:
                with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                    val, _ = winreg.QueryValueEx(key, "Path")
                    registry_paths.append(val)
            except Exception:
                pass
        if registry_paths:
            os.environ["PATH"] = ";".join(registry_paths) + ";" + os.environ.get("PATH", "")
    except Exception:
        pass

import yt_dlp
from pydub import AudioSegment



DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

data =download_youtube_audio("https://youtu.be/6hV1jnQssj0?si=l0r5vbp_3E9XBNcW")


def convert_to_wav(input_path: str)->str:
    
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path

converted_data = convert_to_wav(data)
print("Converted WAV:", converted_data)


