import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import serial


# ==============================
# Comunicação via Ethernet (sem porta serial)
# ==============================
arduino = None  # Nenhum Arduino conectado via USB

print("Modo Ethernet ativado — conexão serial desativada.")








# ==============================
# CONFIGURAÇÕES (substitua pelos seus IPs e URLs)
# ==============================
ARDUINO_IPS = {
    1: "192.168.150.45",
    2: "192.168.150.45",
    3: "192.168.150.45",
    4: "192.168.150.45",
    5: "192.168.150.45",
    6: "192.168.150.45",
    7: "192.168.150.45",
    8: "192.168.150.45",
}

URLS_CAMERAS = {
    1: "rtsp://admin:senha@192.168.150.177:554/",
    2: "rtsp://admin:senha@192.168.150.139:554/",
    # adicione URLs para os outros portões
}

# ==============================
# FUNÇÕES DE UTILITÁRIO
# ==============================
def aplicar_hover(botao, cor_normal, cor_hover):
    def on_enter(e):
        botao['bg'] = cor_hover
    def on_leave(e):
        botao['bg'] = cor_normal
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

def pegar_ip_local():
    return "192.168.0.100"

# ==============================
# CLASSE PRINCIPAL DE PORTÕES
# ==============================
class TelaControlePortoes:
    def __init__(self, master):
        self.master = master
        self.janela = tk.Toplevel(master)
        self.janela.title("Controle de Portões")
        self.janela.geometry("700x500")
        self.janela.configure(bg="#282A36")
        self.janela.resizable(False, False)

        self.status_portoes = {i: "Fechado" for i in range(1, 9)}

        # --- Título ---
        tk.Label(self.janela, text="Controle de 8 Portões",
                 font=("Arial", 16, "bold"), fg="white", bg="#282A36").pack(pady=10)

        # --- Frame dos botões de portão ---
        frame_botoes = tk.Frame(self.janela, bg="#282A36")
        frame_botoes.pack(pady=20)

        self.btns_portoes = {}
        for i in range(1, 9):
            btn = tk.Button(frame_botoes, text=f"Portão {i}", width=14, height=2,
                            bg="#6272A4", fg="white", font=("Arial", 11, "bold"),
                            command=lambda n=i: self.abrir_status_portao(n))
            btn.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
            aplicar_hover(btn, "#6272A4", "#50A6FF")
            self.btns_portoes[i] = btn

        # --- Barra inferior com IP ---
        barra_inferior = tk.Frame(self.janela, bg="#282A36")
        barra_inferior.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar = tk.Label(barra_inferior, text=f"IP do computador: {pegar_ip_local()}",
                                   font=("Arial", 10), fg="white", bg="#282A36")
        self.status_bar.pack(side=tk.RIGHT, padx=10, pady=5)

    # ==============================
    # ABRIR PORTÃO INDIVIDUAL
    # ==============================
    def abrir_status_portao(self, numero_portao):
        status_atual = self.status_portoes[numero_portao]
        ip_portao = ARDUINO_IPS.get(numero_portao, "IP não configurado")

        janela = tk.Toplevel(self.janela)
        janela.title(f"Portão {numero_portao}")
        janela.geometry("450x200")
        janela.configure(bg="#282A36")
        janela.resizable(False, False)

        tk.Label(janela, text=f"Portão {numero_portao} - Status: {status_atual}",
                 font=("Arial", 14, "bold"), fg="white", bg="#282A36").pack(pady=15)

        frame_botoes = tk.Frame(janela, bg="#282A36")
        frame_botoes.pack(pady=20)

        # --- Botão Abrir/Fechar ---
        btn_abrir = tk.Button(frame_botoes, text="Abrir/Fechar", bg="#FF9800", fg="white",
                              font=("Arial", 12, "bold"), width=12,
                              command=lambda: self.toggle_portao(numero_portao, janela))
        btn_abrir.grid(row=0, column=0, padx=10)
        aplicar_hover(btn_abrir, "#FF9800", "#FFA733")

        # --- Botão Ver Câmera ---
        btn_camera = tk.Button(frame_botoes, text="Ver Câmera", bg="#2196F3", fg="white",
                               font=("Arial", 12, "bold"), width=12,
                               command=lambda: self.abrir_camera(numero_portao))
        btn_camera.grid(row=0, column=1, padx=10)
        aplicar_hover(btn_camera, "#2196F3", "#4DA6FF")

        # --- Botão OK ---
        btn_ok = tk.Button(frame_botoes, text="OK", bg="#4CAF50", fg="white",
                           font=("Arial", 12, "bold"), width=12, command=janela.destroy)
        btn_ok.grid(row=0, column=2, padx=10)
        aplicar_hover(btn_ok, "#4CAF50", "#45A049")

        # --- Barra inferior ---
        barra_inferior = tk.Frame(janela, bg="#C0C0C0")
        barra_inferior.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(barra_inferior, text=f"IP do Portão: {ip_portao}", font=("Arial", 10), bg="#C0C0C0").pack(side=tk.RIGHT, padx=10)

    # ==============================
    # FUNÇÕES AUXILIARES
    # ==============================
    def toggle_portao(self, numero_portao, janela):
        self.status_portoes[numero_portao] = "Aberto" if self.status_portoes[numero_portao] == "Fechado" else "Fechado"
        messagebox.showinfo("Portão", f"O Portão {numero_portao} agora está {self.status_portoes[numero_portao]}.")

    def abrir_camera(self, numero_portao):
        url = URLS_CAMERAS.get(numero_portao)
        if not url:
            messagebox.showerror("Erro", f"Nenhuma câmera configurada para o Portão {numero_portao}.")
            return

        janela_camera = tk.Toplevel(self.janela)
        janela_camera.title(f"Câmera Portão {numero_portao}")
        janela_camera.geometry("640x480")
        janela_camera.configure(bg="#282A36")

        lbl_video = tk.Label(janela_camera)
        lbl_video.pack()

        cap = cv2.VideoCapture(url)

        def atualizar_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                lbl_video.imgtk = imgtk
                lbl_video.configure(image=imgtk)
            if janela_camera.winfo_exists():
                lbl_video.after(30, atualizar_frame)
            else:
                cap.release()

        atualizar_frame()

        btn_fechar = tk.Button(janela_camera, text="Fechar", bg="#F44336", fg="white",
                               font=("Arial", 12, "bold"), width=12, command=janela_camera.destroy)
        btn_fechar.pack(pady=10)
