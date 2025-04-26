# detector_video.py
import cv2
import numpy as np
from config import BLACK_THRESHOLD

_anterior = None  # frame anterior (para detectar freeze)

def verificar_black_screen(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        return False
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    media = np.mean(cinza)
    return media < BLACK_THRESHOLD

def verificar_freeze(caminho_imagem, limiar_similaridade=0.99):
    global _anterior
    atual = cv2.imread(caminho_imagem)
    if atual is None:
        return False

    if _anterior is None:
        _anterior = atual
        return False

    img1 = cv2.cvtColor(_anterior, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(atual, cv2.COLOR_BGR2GRAY)

    score = np.corrcoef(img1.flatten(), img2.flatten())[0, 1]

    _anterior = atual
    return score >= limiar_similaridade
