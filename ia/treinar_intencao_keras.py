import matplotlib
matplotlib.use('Agg')  # ✅ evita que o gráfico abra na tela

import matplotlib.pyplot as plt
import numpy as np
import pickle
import csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os


def main():
    # === DADOS FIXOS INICIAIS ===
    dados_fixos = [
        ("quero saber sobre iptu", "iptu"),
        ("como pagar iptu atrasado", "iptu"),
        ("onde emitir guia do iptu", "iptu"),
        ("renovar minha cnh", "cnh"),
        ("minha carteira de motorista venceu", "cnh"),
        ("como tirar cnh", "cnh"),
        ("documento do carro vencido", "detran"),
        ("como pagar licenciamento", "detran"),
        ("problemas com o detran go", "detran"),
    ]

    # === ADICIONA DADOS DO CSV (se existirem) ===
    caminho_csv_novos = "ia/dados_novos.csv"
    dados_combinados = dados_fixos.copy()

    if os.path.exists(caminho_csv_novos):
        with open(caminho_csv_novos, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if len(linha) == 2:
                    pergunta, classe = linha
                    dados_combinados.append((pergunta.strip(), classe.strip()))

    # === Preparar dados ===
    frases, intencoes = zip(*dados_combinados)

    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(frases)
    sequencias = tokenizer.texts_to_sequences(frases)
    X = pad_sequences(sequencias, padding='post')

    # === Codificar classes ===
    labels = sorted(list(set(intencoes)))
    label_to_index = {label: i for i, label in enumerate(labels)}
    index_to_label = {i: label for label, i in label_to_index.items()}
    y = np.array([label_to_index[label] for label in intencoes])

    # === Modelo ===
    vocab_size = len(tokenizer.word_index) + 1
    model = Sequential([
        Embedding(vocab_size, 16),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(len(labels), activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # === Treinamento com histórico ===
    history = model.fit(X, y, epochs=500, verbose=0)

    # === Salvar gráfico de desempenho como imagem ===
    plt.plot(history.history['accuracy'], label='Acurácia de Treinamento')
    plt.plot(history.history['loss'], label='Perda de Treinamento')
    plt.title('Desempenho do Modelo de Rede Neural')
    plt.xlabel('Épocas')
    plt.ylabel('Acurácia / Perda')
    plt.legend()
    plt.savefig("ia/grafico_treinamento.png")
    plt.close()

    # === Salvar modelo e mapeamentos ===
    model.save("ia/modelo_intencao.h5")

    with open("ia/tokenizer.pkl", "wb") as f_tok:
        pickle.dump(tokenizer, f_tok)

    with open("ia/index_to_label.pkl", "wb") as f_lbl:
        pickle.dump(index_to_label, f_lbl)

    print("✅ Modelo treinado com dados novos e salvos com sucesso!")

if __name__ == '__main__':
    main()
