import speech_recognition as sr
import pyttsx3
import numpy as np
import json
import os
import pickle
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.text import text_to_word_sequence

# 🚀 Inicializar voz
voz = pyttsx3.init()
voz.setProperty('rate', 150)

def falar(texto):
    print("IA:", texto)
    voz.say(texto)
    voz.runAndWait()

def ouvir():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Fale algo...")
        reconhecedor.adjust_for_ambient_noise(source)
        audio = reconhecedor.listen(source)

        try:
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print("Você disse:", texto)
            return texto
        except sr.UnknownValueError:
            falar("Desculpe, não entendi.")
            return ""
        except sr.RequestError:
            falar("Erro de conexão com o serviço de voz.")
            return ""

# 🚨 Histórico salvo
ARQUIVO_HISTORICO = "historico_interacoes.json"

# 🔁 Carregar histórico salvo (ou iniciar novo)
if os.path.exists(ARQUIVO_HISTORICO):
    try:    
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            historico = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️  Histórico inválido ou ausente. Iniciando lista vazia.")
        historico = []
else:
    historico = []

# 🔁 Carregar tokenizer
try:
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
except FileNotFoundError:
    print("⚠️  Tokenizer não encontrado. Criando um novo...")
    from tensorflow.keras.preprocessing.text import Tokenizer
    tokenizer = Tokenizer(num_words=1000)


def salvar_historico(frase, classe):
    historico.append({"frase": frase, "classe": int(round(classe))})
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

def treinar_novamente():
    frases = [item["frase"] for item in historico]
    classes = [item["classe"] for item in historico]

    tokenizer.fit_on_texts(frases)
    sequencias = tokenizer.texts_to_sequences(frases)
    X = pad_sequences(sequencias, maxlen=10)
    y = np.array(classes)

    # 🧠 Modelo mais profundo e eficaz
    modelo = Sequential()
    modelo.add(Dense(64, input_shape=(10,), activation='relu'))
    modelo.add(Dense(32, activation='relu'))
    modelo.add(Dense(1, activation='sigmoid'))

    modelo.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # ⏱️ Mais tempo de treino
    modelo.fit(X, y, epochs=30, verbose=0)

    modelo.save("modelo_sentimentos.h5")

    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)



# 🔁 Carregar modelo (o mais recente)
try:
    modelo = load_model("modelo_sentimentos.h5")
except (OSError, IOError):
    print("⚠️  Modelo não encontrado. Treinando um novo com o histórico...")
    treinar_novamente()
    modelo = load_model("modelo_sentimentos.h5")


import random  # no início do seu script

respostas_positivas = [
    "Você parece ótimo hoje, senhor.",
    "Excelentes sinais de humor. Impressionante.",
    "Mais positivo que isso só um pôr do sol com café.",
    "Claramente um dia de conquistas para você.",
    "Isso sim é energia boa, mantenha assim."
]

respostas_neutras = [
    "Você parece... ok. Meio termo é aceitável.",
    "Nada empolga, nada irrita. Um dia normal.",
    "Humor estável. Siga em frente com cautela.",
    "Sem grandes emoções detectadas.",
    "Neutro como um robô com café morno."
]

respostas_negativas = [
    "Detectei traços de tormento interior. Recomendo chocolate.",
    "Sinal de alerta: energia emocional em baixa.",
    "Humor sombrio. Hora de reavaliar sua playlist.",
    "Parece que o dia não colaborou muito, né?",
    "Sinto uma sombra de tristeza aí. Deseja conversar?"
]

def analisar_sentimento(frase):
    sequencia = tokenizer.texts_to_sequences([frase])
    entrada = pad_sequences(sequencia, maxlen=10)
    predicao = modelo.predict(entrada)[0][0]

    print(f"🎯 Predição bruta: {predicao:.2f}")  # mostra no terminal

    # Salvar no histórico
    salvar_historico(frase, predicao)
    treinar_novamente()

    # Escolher resposta com base na faixa
    if predicao > 0.7:
        return random.choice(respostas_positivas)
    elif predicao > 0.4:
        return random.choice(respostas_neutras)
    else:
        return random.choice(respostas_negativas)


# 🎤 Loop de interação
while True:
    comando = ouvir().lower()

    if "sair" in comando or "encerrar" in comando:
        falar("Encerrando. Espero que seu humor melhore... ou não.")
        break

    elif comando:
        resposta = analisar_sentimento(comando)
        falar(resposta)
