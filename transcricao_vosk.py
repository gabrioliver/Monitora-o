# transcricao_vosk.py
import os
import wave
import json
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-model-small-pt-0.3"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modelo Vosk não encontrado em {MODEL_PATH}")

model = Model(MODEL_PATH)

def transcrever_audio(caminho_audio):
    if not os.path.exists(caminho_audio):
        return "[ERRO] Áudio não encontrado para transcrição."

    wf = wave.open(caminho_audio, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    frases = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            resultado = json.loads(rec.Result())
            if resultado.get("text"):
                frases.append(resultado["text"])

    resultado = json.loads(rec.FinalResult())
    if resultado.get("text"):
        frases.append(resultado["text"])

    with open("historico_transcricao.txt", "a", encoding="utf-8") as f:
        for frase in frases:
            f.write(frase + "\n")

    return frases
