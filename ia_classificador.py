# ia_classificador.py
import json
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import tokenizer_from_json

# Carrega tokenizer salvo
with open("tokenizer.json", "r", encoding="utf-8") as f:
    tokenizer_data = json.load(f)
    tokenizer = tokenizer_from_json(tokenizer_data)

# Carrega modelo treinado
modelo = load_model("modelo_classificador.h5")

# Mapeamento de intenções (precisa ser igual ao que usou no treinamento)
rotulos = ['ipva', 'iptu', 'cnh', 'detran']

# Função para prever intenção
def prever_intencao(frase):
    sequencia = tokenizer.texts_to_sequences([frase])
    sequencia_padded = pad_sequences(sequencia, maxlen=20)
    predicao = modelo.predict(sequencia_padded)
    indice_previsto = np.argmax(predicao)
    return rotulos[indice_previsto]
