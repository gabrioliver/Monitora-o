# detector_audio.py
import wave
import numpy as np
from config import AUDIO_MUDO_THRESHOLD

def verificar_audio_mudo(caminho_audio):
    with wave.open(caminho_audio, 'rb') as f:
        frames = f.readframes(-1)
        audio_np = np.frombuffer(frames, dtype=np.int16)
        rms = np.sqrt(np.mean(audio_np ** 2))
        return rms < AUDIO_MUDO_THRESHOLD
