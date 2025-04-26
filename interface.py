# interface.py
import tkinter as tk
from threading import Thread
import os
import time
from ia_monitor_rtmp import verificar_status_transmissao

LOG_PATH = "logs/eventos.log"

class MonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoramento de Transmissão")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")

        self.monitorando = False

        self.status_icon = tk.Label(self.root, text="●", font=("Arial", 48), fg="gray", bg="#1e1e1e")
        self.status_icon.pack(pady=(20, 0))

        self.status_label = tk.Label(self.root, text="Aguardando transmissão...", font=("Arial", 16), fg="white", bg="#1e1e1e")
        self.status_label.pack(pady=(0, 10))

        self.btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.btn_frame.pack(pady=10)

        self.monitorar_btn = tk.Button(self.btn_frame, text="Iniciar Monitoramento", command=self.iniciar_monitoramento_thread,
                                       font=("Arial", 14), bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10)
        self.monitorar_btn.pack(side=tk.LEFT, padx=10)

        self.parar_btn = tk.Button(self.btn_frame, text="Parar", command=self.parar_monitoramento,
                                   font=("Arial", 14), bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10)
        self.parar_btn.pack(side=tk.LEFT, padx=10)
        self.parar_btn.config(state="disabled")

        self.log_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, bg="#121212", fg="white", font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        self.root.after(3000, self.loop_monitoramento)

    def iniciar_monitoramento_thread(self):
        if not self.monitorando:
            self.monitorando = True
            self.monitorar_btn.config(text="Monitorando...", state="disabled", bg="#999999")
            self.parar_btn.config(state="normal")
            self.adicionar_log("[INFO] Monitoramento iniciado.")

    def parar_monitoramento(self):
        self.monitorando = False
        self.adicionar_log("[INFO] Monitoramento interrompido pelo usuário.")
        self.monitorar_btn.config(state="normal", text="Iniciar Monitoramento", bg="#4CAF50")
        self.parar_btn.config(state="disabled")

    def loop_monitoramento(self):
        if self.monitorando:
            status, mensagens = verificar_status_transmissao()
            for msg in mensagens:
                self.adicionar_log(msg)
            self.atualizar_status_visual(mensagens)
        self.root.after(3000, self.loop_monitoramento)

    def atualizar_status_visual(self, mensagens):
        texto = mensagens[-1].lower() if mensagens else ""
        if any(p in texto for p in ["preta", "ausente", "congelada", "mudo", "não encontrado", "falha"]):
            cor = "red"
            status = "Falha na transmissão detectada."
        elif "normal" in texto:
            cor = "green"
            status = "Transmissão normal."
        else:
            cor = "yellow"
            status = "Aguardando transmissão..."

        self.status_icon.config(fg=cor)
        self.status_label.config(text=status)

    def adicionar_log(self, mensagem):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        linha = f"{timestamp} {mensagem}\n"

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(linha)

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, linha)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")

    root = tk.Tk()
    app = MonitorGUI(root)
    root.mainloop()
