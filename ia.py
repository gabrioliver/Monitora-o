# Importando as bibliotecas necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Passo 1: Carregar o Dataset (Iris Dataset)
data = load_iris()
X = data.data  # Dados de entrada (features)
y = data.target  # Rótulos (target)

# Passo 2: Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Passo 3: Criar o modelo de rede neural
model = Sequential()

# Adicionando camadas (rede neural simples com 1 camada oculta)
model.add(Dense(10, input_dim=4, activation='relu'))  # 4 features de entrada (Iris tem 4)
model.add(Dense(3, activation='softmax'))  # 3 classes de saída (Iris tem 3 tipos de flores)

# Passo 4: Compilar o modelo
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Passo 5: Treinar o modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=1)

# Passo 6: Avaliar o modelo
accuracy = model.evaluate(X_test, y_test)
print(f"Acurácia no conjunto de teste: {accuracy[1] * 100:.2f}%")

# Passo 7: Fazer previsões
predictions = model.predict(X_test)

# Converter as previsões para classes
predicted_classes = np.argmax(predictions, axis=1)
print(f"Previsões das classes: {predicted_classes}")

# Passo 8: Visualizar a performance do modelo
plt.plot(history.history['accuracy'], label='Acurácia de Treinamento')
plt.plot(history.history['loss'], label='Perda de Treinamento')
plt.legend()
plt.title("Desempenho do Modelo de Rede Neural")
plt.xlabel("Épocas")
plt.ylabel("Acurácia / Perda")

import speech_recognition as sr
import pyttsx3

# Inicia o motor de voz
voz = pyttsx3.init()
voz.setProperty('rate', 150)  # Velocidade da fala

def falar(texto):
    voz.say(texto)
    voz.runAndWait()

def ouvir():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        reconhecedor.adjust_for_ambient_noise(source)
        audio = reconhecedor.listen(source)

        try:
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print("Você disse:", texto)
            return texto
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return ""
        except sr.RequestError:
            print("Erro ao se conectar com o serviço de voz.")
            return ""

# Loop principal
while True:
    comando = ouvir().lower()

    if "sair" in comando:
        falar("Encerrando a conversa. Até logo!")
        break

    elif comando:
        # Aqui você pode conectar com a sua rede neural ou lógica
        resposta = f"Você disse: {comando}"  # Exemplo simples
        falar(resposta)

# Suponha que seu modelo faz uma previsão de sentimento
from tensorflow.keras.models import load_model
import numpy as np

modelo = load_model("modelo.h5")

def analisar_frase(frase):
    # Aqui você insere seu pré-processamento (como tokenização, vetorização etc.)
    vetor = transformar_para_vetor(frase)
    predicao = modelo.predict(np.array([vetor]))[0]
    
    # Interprete a saída do modelo
    if predicao > 0.5:
        return "Parece uma frase positiva."
    else:
        return "Parece uma frase negativa."
    
