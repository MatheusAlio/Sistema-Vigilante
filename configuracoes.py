import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

CONFIG_FILE = "config.json"

# -------------------------------
# Configuração padrão
# -------------------------------
CONFIG_PADRAO = {
    "arduinos": {str(i): f"192.168.150.{40+i}" for i in range(1, 9)},
    "portas_arduino": {str(i): [True, True, True, True] for i in range(1, 9)},
    "panicos": {str(i): f"192.168.150.{50+i}" for i in range(1, 9)},
    "panicos_ativos": {str(i): [True] for i in range(1, 9)}
}

# -------------------------------
# Funções de arquivo
# -------------------------------
def carregar_config():
    if not os.path.exists(CONFIG_FILE):
        salvar_config(CONFIG_PADRAO)
        return CONFIG_PADRAO
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                raise ValueError("Arquivo vazio")
            return json.loads(conteudo)
    except Exception as e:
        print(f"[ERRO] Falha ao carregar config.json: {e}")
        salvar_config(CONFIG_PADRAO)
        return CONFIG_PADRAO

def salvar_config(novo_config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(novo_config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERRO] Falha ao salvar config.json: {e}")

CONFIG = carregar_config()

# -------------------------------
# GUI
# -------------------------------
class ConfiguracoesGerais(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configurações Arduino e Pânico")
        self.configure(bg="#2C2F44")
        self.resizable(False, False)

        self.entries_arduino = {}
        self.entries_panico = {}
        self.checks_portas = {}
        self.checks_panico = {}

        # Cabeçalho
        tk.Label(self, text="Arduino", bg="#2C2F44", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(self, text="IP Arduino", bg="#2C2F44", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1)
        tk.Label(self, text="Portas Ativas", bg="#2C2F44", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2)
        tk.Label(self, text="IP Pânico", bg="#2C2F44", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=3)

        for i in range(1, 9):
            # Label Arduino
            tk.Label(self, text=f"Arduino {i}", bg="#2C2F44", fg="white").grid(row=i, column=0, padx=5, pady=5)

            # Entry IP Arduino
            entry_a = tk.Entry(self, width=20)
            entry_a.insert(0, CONFIG["arduinos"].get(str(i), ""))
            entry_a.grid(row=i, column=1, padx=5, pady=5)
            self.entries_arduino[i] = entry_a

            # Checkbuttons das portas
            frame_portas = tk.Frame(self, bg="#2C2F44")
            frame_portas.grid(row=i, column=2)
            self.checks_portas[i] = []
            portas_config = CONFIG.get("portas_arduino", {}).get(str(i), [True, True, True, True])
            for p in range(4):
                var = tk.IntVar(value=1 if portas_config[p] else 0)
                cb = tk.Checkbutton(frame_portas, text=f"P{p+1}", variable=var, bg="#2C2F44", fg="white")
                cb.pack(side="left", padx=2)
                self.checks_portas[i].append(var)

            # Frame do IP Pânico + Checkbutton abaixo
            frame_panico = tk.Frame(self, bg="#2C2F44")
            frame_panico.grid(row=i, column=3, padx=5, pady=5)

            # Entry IP Pânico
            entry_p = tk.Entry(frame_panico, width=20)
            entry_p.pack(pady=(2,5))
            entry_p.insert(0, CONFIG["panicos"].get(str(i), ""))
            self.entries_panico[i] = entry_p

            # Checkbutton Pânico centralizado abaixo do Entry
            self.checks_panico[i] = []
            panico_config = CONFIG.get("panicos_ativos", {}).get(str(i), [True])
            for p in range(len(panico_config)):
                var = tk.IntVar(value=1 if panico_config[p] else 0)
                cb = tk.Checkbutton(frame_panico, text="Ativo", variable=var, bg="#2C2F44", fg="white")
                cb.pack(pady=2, anchor="center")
                self.checks_panico[i].append(var)

        # Botões
        btn_frame = tk.Frame(self, bg="#2C2F44")
        btn_frame.grid(row=20, column=0, columnspan=4, pady=15)

        tk.Button(btn_frame, text="Testar Conexões", bg="#2196F3", fg="white", width=18,
                  command=self.testar_conexoes).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Salvar Configurações", bg="#4CAF50", fg="white", width=22,
                  command=self.salvar_tudo).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Fechar", bg="#F44336", fg="white", width=15,
                  command=self.destroy).pack(side="left", padx=10)

    # -------------------------------
    # Funções internas
    # -------------------------------
    def testar_conexoes(self):
        resultados = []
        for i in range(1, 9):
            ip_a = self.entries_arduino[i].get().strip()
            ip_p = self.entries_panico[i].get().strip()

            # Testa Arduino
            try:
                r = requests.get(f"http://{ip_a}", timeout=1)
                if r.status_code == 200:
                    resultados.append(f"Arduino {i}: ✅ OK")
                else:
                    resultados.append(f"Arduino {i}: ⚠️ Erro {r.status_code}")
            except Exception:
                resultados.append(f"Arduino {i}: ❌ Falha")

            # Testa Pânico
            try:
                r = requests.get(f"http://{ip_p}", timeout=1)
                if r.status_code == 200:
                    resultados.append(f"Pânico {i}: ✅ OK")
                else:
                    resultados.append(f"Pânico {i}: ⚠️ Erro {r.status_code}")
            except Exception:
                resultados.append(f"Pânico {i}: ❌ Falha")

        messagebox.showinfo("Teste de Conexões", "\n".join(resultados))

    def salvar_tudo(self):
        novas_config = {
            "arduinos": {str(i): self.entries_arduino[i].get().strip() for i in range(1, 9)},
            "portas_arduino": {
                str(i): [bool(var.get()) for var in self.checks_portas[i]] for i in range(1, 9)
            },
            "panicos": {str(i): self.entries_panico[i].get().strip() for i in range(1, 9)},
            "panicos_ativos": {
                str(i): [bool(var.get()) for var in self.checks_panico[i]] for i in range(1, 9)
            }
        }
        salvar_config(novas_config)
        messagebox.showinfo("Salvar", "Configurações salvas com sucesso!")

#-----------------------------
# Inicializa GUI
#-----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema Vigilante")
    root.geometry("500x500")
    tk.Button(root, text="Abrir Configurações", width=25,
              command=lambda: ConfiguracoesGerais(root)).pack(pady=20)
    root.mainloop()
