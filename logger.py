# logger.py
import os
from datetime import datetime

LOG_PATH = "logs/eventos.log"

# Cria pasta de logs se não existir
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def registrar_alerta(mensagem):
    agora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log = f"{agora} {mensagem}"
    print(log)  # também exibe no terminal
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log + "\n")
