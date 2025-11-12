# utils.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import os

# ==============================
# Função para aplicar hover nos botões
# ==============================
def aplicar_hover(botao, cor_normal, cor_hover):
    def on_enter(e):
        botao['bg'] = cor_hover
    def on_leave(e):
        botao['bg'] = cor_normal
    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

# ==============================
# Função para centralizar janela
# ==============================
def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# ==============================
# Função para criar ícones
# ==============================
def criar_icone(nome, tamanho=24):
    """
    Cria um ícone a partir de um arquivo .png na pasta 'icones'
    """
    caminho = os.path.join("icones", f"{nome}.png")
    try:
        img = Image.open(caminho)
        img = img.resize((tamanho, tamanho), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erro ao criar ícone '{nome}': {e}")
        return None

# ==============================
# Função para pegar IP local
# ==============================
def pegar_ip_local():
    """
    Retorna o IP local da máquina
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # conecta para descobrir IP
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"
