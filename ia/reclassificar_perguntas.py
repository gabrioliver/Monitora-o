import os
import csv

ARQUIVO_ENTRADA = "ia/perguntas_nao_reconhecidas.txt"
ARQUIVO_SAIDA = "ia/dados_novos.csv"

# Confirma se o arquivo de entrada existe
if not os.path.exists(ARQUIVO_ENTRADA):
    print("❌ Nenhuma pergunta nova foi registrada ainda.")
    exit()

# Carrega perguntas não reconhecidas
with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
    perguntas = [linha.strip() for linha in f.readlines() if linha.strip()]

# Remove duplicadas
perguntas = list(set(perguntas))

if not perguntas:
    print("📭 Nenhuma nova pergunta a classificar.")
    exit()

# Cria ou abre o CSV de saída
with open(ARQUIVO_SAIDA, "a", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    
    print("💡 Classifique cada pergunta com uma das intenções: iptu, cnh, detran, etc.")
    print("📌 Digite 's' para pular ou 'q' para sair.\n")

    for pergunta in perguntas:
        print(f"🤔 Pergunta: {pergunta}")
        classe = input("➡️ Intenção: ").strip().lower()

        if classe == "q":
            print("🔚 Saindo...")
            break
        elif classe == "s":
            continue
        elif classe == "":
            print("⚠️ Intenção vazia ignorada.")
            continue

        writer.writerow([pergunta, classe])
        print("✅ Classificado!\n")

# Apaga as perguntas não reconhecidas após classificação
os.remove(ARQUIVO_ENTRADA)
print(f"\n📁 Perguntas salvas em '{ARQUIVO_SAIDA}' e arquivo de não reconhecidas foi limpo.")
