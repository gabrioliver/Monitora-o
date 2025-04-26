# ia_monitor_rtmp.py
import os
from datetime import datetime
from recorder import capturar_frame, capturar_audio
from detector_video import verificar_black_screen, verificar_freeze
from detector_audio import verificar_audio_mudo

# Configurações
RTMP_URL = "rtmp://192.168.1.2/live/test"  # ajuste o IP se necessário
FRAME_CAPTURE_PATH = "frames/frame.jpg"
AUDIO_CAPTURE_PATH = "audio/audio.wav"
BLACK_THRESHOLD = 15  # valor para detectar tela preta
AUDIO_MUDO_THRESHOLD = 30  # valor para detectar áudio mudo

# Variável global para guardar último frame (para detectar congelamento)
ultimo_frame = None

def verificar_status_transmissao():
    global ultimo_frame

    mensagens = []
    status = "ok"

    # Garantir pastas
    os.makedirs(os.path.dirname(FRAME_CAPTURE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(AUDIO_CAPTURE_PATH), exist_ok=True)

    # Captura frame
    capturar_frame(RTMP_URL, FRAME_CAPTURE_PATH)
    imagem_existe = os.path.exists(FRAME_CAPTURE_PATH)

    # Captura áudio
    capturar_audio(RTMP_URL, AUDIO_CAPTURE_PATH)
    audio_existe = os.path.exists(AUDIO_CAPTURE_PATH)

    # Verifica frame
    if not imagem_existe:
        mensagens.append("[ALERTA] Imagem não encontrada (possível falha de vídeo).")
        status = "ausente"
    else:
        if verificar_black_screen(FRAME_CAPTURE_PATH):
            mensagens.append("[ALERTA] Tela preta detectada!")
            status = "falha"
        elif verificar_freeze(FRAME_CAPTURE_PATH):
            mensagens.append("[ALERTA] Quadro congelado detectado!")
            status = "falha"

    # Verifica áudio
    if not audio_existe:
        mensagens.append("[ALERTA] Áudio não encontrado (possível falha de áudio).")
        status = "ausente"
    else:
        try:
            if verificar_audio_mudo(AUDIO_CAPTURE_PATH):
                mensagens.append("[ALERTA] Áudio mudo detectado!")
                status = "falha"
        except Exception as e:
            mensagens.append(f"[ERRO] Problema ao analisar o áudio: {e}")
            status = "falha"

    # Se não houve nenhum problema detectado
    if imagem_existe and audio_existe and status == "ok":
        mensagens.append("[OK] Transmissão normal.")

    return status, mensagens

if __name__ == "__main__":
    status, mensagens = verificar_status_transmissao()
    for msg in mensagens:
        print(msg)
