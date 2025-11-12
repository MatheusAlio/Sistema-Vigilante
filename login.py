import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importando o Pillow para manipulação de imagens
from utils import pegar_ip_local, aplicar_hover
from telas.principal_portoes import TelaControlePortoes

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E2F")

        # --- Carregar e exibir o logo ---
        try:
            logo_img = Image.open("TA_.png")  # Certifique-se de que o caminho da imagem está correto
            logo_img = logo_img.resize((120, 100))  # Ajuste o tamanho do logo
            self.logo = ImageTk.PhotoImage(logo_img)
            # Exibe o logo na tela
            logo_label = tk.Label(root, image=self.logo, bg="#1E1E2F")
            logo_label.image = self.logo  # Manter uma referência para a imagem
            logo_label.pack(pady=20)  # Ajuste o padding conforme necessário
        except Exception as e:
            # Se houver erro no carregamento, exibe o texto "LOGO" como fallback
            messagebox.showerror("Erro", f"Erro ao carregar o logo: {e}")
            tk.Label(root, text="LOGO", font=("Arial", 20, "bold"), fg="white", bg="#1E1E2F").pack(pady=10)

        # --- Texto de cabeçalho ---
        tk.Label(root, text="Acesso ao Sistema", font=("Arial", 16, "bold"), fg="white", bg="#1E1E2F").pack(pady=15)
        
        # --- Campos de Login ---
        tk.Label(root, text="Usuário:", font=("Arial", 11), fg="white", bg="#1E1E2F").pack()
        self.usuario_entry = tk.Entry(root, font=("Arial", 11))
        self.usuario_entry.pack(pady=5)
        
        tk.Label(root, text="Senha:", font=("Arial", 11), fg="white", bg="#1E1E2F").pack()
        self.senha_entry = tk.Entry(root, show="*", font=("Arial", 11))
        self.senha_entry.pack(pady=5)

        # --- Botão de Entrar ---
        self.btn_entrar = tk.Button(root, text="Entrar", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                                    width=12, command=self.verificar_login)
        self.btn_entrar.pack(pady=15)
        aplicar_hover(self.btn_entrar, "#4CAF50", "#45A049")

        # --- Exibir IP local na parte inferior ---
        ip_local = pegar_ip_local()
        tk.Label(root, text=f"IP do computador: {ip_local}", font=("Arial", 9), fg="white", bg="#1E1E2F").pack(side=tk.BOTTOM, pady=5)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        if usuario == "admin" and senha == "1234":
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.abrir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def abrir_tela_principal(self):
        # Esconde a janela de login antes de abrir a janela principal
        self.root.withdraw()  # Esconde a janela de login
        
        # Agora criamos a nova janela principal
        root_principal = tk.Tk()
        TelaControlePortoes(root_principal)
        root_principal.mainloop()

        # Depois que a janela principal for fechada, destruímos a janela de login
        self.root.destroy()
