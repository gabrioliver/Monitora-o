import os
import pickle
from difflib import get_close_matches
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 1. Mapeamento por palavras-chave
MAPA_INTENCOES = {
    "iptu": ["iptu", "imposto predial", "imóvel", "terreno", "casa"],
    "cnh": ["cnh", "carteira de motorista", "habilitação", "renovar"],
    "detran": ["detran", "licenciamento", "documento do carro", "veículo", "carro"]
}

# 2. Base de conhecimento com respostas
BASE_CONHECIMENTO = {
    "iptu": "O IPTU é um imposto municipal. Em Goiás, consulte no site da prefeitura com seu CPF ou número do imóvel.",
    "cnh": "Para renovar a CNH, acesse o site do Detran GO > Habilitação > Renovação.",
    "detran": "O Detran GO oferece serviços como renovação de CNH, licenciamento, IPVA, e outros relacionados a veículos."
}

# 3. Similaridade textual básica
def por_palavra_chave(pergunta):
    pergunta = pergunta.lower()
    for chave, palavras in MAPA_INTENCOES.items():
        if any(p in pergunta for p in palavras):
            return BASE_CONHECIMENTO.get(chave)
    return None

def por_similaridade(pergunta):
    pergunta = pergunta.lower()
    termos = list(BASE_CONHECIMENTO.keys())
    semelhantes = get_close_matches(pergunta, termos, n=1, cutoff=0.5)
    if semelhantes:
        return BASE_CONHECIMENTO.get(semelhantes[0])
    return None

# 4. Classificação por rede neural refinada (Keras)
def carregar_modelo_keras():
    try:
        modelo = load_model("ia/modelo_intencao.h5")
        with open("ia/tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
        with open("ia/index_to_label.pkl", "rb") as f:
            index_to_label = pickle.load(f)
        return modelo, tokenizer, index_to_label
    except:
        return None, None, None

def por_modelo_keras(pergunta, modelo, tokenizer, index_to_label):
    if not modelo or not tokenizer:
        return None
    sequencia = tokenizer.texts_to_sequences([pergunta.lower()])
    entrada = pad_sequences(sequencia, maxlen=10, padding='post')
    pred = modelo.predict(entrada, verbose=0)[0]
    indice = pred.argmax()
    classe = index_to_label.get(indice)
    return BASE_CONHECIMENTO.get(classe)

# 5. Função final de decisão com fallback
def responder(pergunta):
    resposta = por_palavra_chave(pergunta)
    if resposta:
        return resposta

    resposta = por_similaridade(pergunta)
    if resposta:
        return resposta

    modelo, tokenizer, index_to_label = carregar_modelo_keras()
    resposta = por_modelo_keras(pergunta, modelo, tokenizer, index_to_label)
    if resposta:
        return resposta

    return "Desculpe, ainda não sei como responder isso. Mas estou aprendendo!"

# Caminho do arquivo onde serão salvas perguntas desconhecidas
ARQUIVO_PERGUNTAS_NAO_RECONHECIDAS = "ia/perguntas_nao_reconhecidas.txt"

def salvar_pergunta_nao_reconhecida(pergunta):
    with open(ARQUIVO_PERGUNTAS_NAO_RECONHECIDAS, "a", encoding="utf-8") as f:
        f.write(pergunta.strip() + "\n")

# Alterar função final 'responder' para incluir o salvamento
def responder(pergunta):
    resposta = por_palavra_chave(pergunta)
    if resposta:
        return resposta

    resposta = por_similaridade(pergunta)
    if resposta:
        return resposta

    modelo, tokenizer, index_to_label = carregar_modelo_keras()
    resposta = por_modelo_keras(pergunta, modelo, tokenizer, index_to_label)
    if resposta:
        return resposta

    salvar_pergunta_nao_reconhecida(pergunta)
    return "Desculpe, ainda não sei como responder isso. Mas estou aprendendo!"
