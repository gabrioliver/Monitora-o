import subprocess
import os
from datetime import datetime

LOG_PATH = "logs/eventos.log"

def registrar_erro(msg):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} [ERRO] {msg}\n")

def capturar_frame(rtmp_url, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    comando = [
        "ffmpeg", "-y",
        "-i", rtmp_url,
        "-frames:v", "1",
        "-q:v", "2",
        output_path
    ]
    try:
        resultado = subprocess.run(comando, timeout=10, capture_output=True, text=True)
        print("⚠️ FFmpeg FRAME stderr:\n", resultado.stderr)
    except subprocess.TimeoutExpired:
        registrar_erro("Timeout ao tentar capturar frame de vídeo.")
        return
    if not os.path.exists(output_path):
        registrar_erro("Falha ao capturar frame de vídeo.")

def capturar_audio(rtmp_url, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    comando = [
        "ffmpeg", "-y",
        "-i", rtmp_url,
        "-t", "10",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_path
    ]
    try:
        resultado = subprocess.run(comando, timeout=10, capture_output=True, text=True)
        print("⚠️ FFmpeg AUDIO stderr:\n", resultado.stderr)
    except subprocess.TimeoutExpired:
        registrar_erro("Timeout ao tentar capturar áudio.")
        return
    if not os.path.exists(output_path):
        registrar_erro("Falha ao capturar áudio.")
