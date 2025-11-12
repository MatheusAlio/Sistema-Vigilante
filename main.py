import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from telas.principal_portoes import TelaControlePortoes


class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Sistema Vigilante")
        self.master.geometry("500x450")
        self.master.configure(bg="#282A36")
        self.master.resizable(False, False)

        # --- Carregar e exibir o logo ---
        try:
            logo_img = Image.open("TA_.png")
            logo_img = logo_img.resize((100, 125))
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(master, image=self.logo, bg="#282A36")
            logo_label.image = self.logo
            logo_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o logo: {e}")
            tk.Label(master, text="LOGO", font=("Arial", 20, "bold"),
                     fg="white", bg="#282A36").pack(pady=10)

        # --- Texto de cabeçalho ---
        tk.Label(master, text="Sistema de Automação",
                 font=("Arial", 16, "bold"),
                 fg="white", bg="#282A36").pack(pady=20)

        # --- Campos de Login ---
        tk.Label(master, text="Usuário:", font=("Arial", 12),
                 fg="white", bg="#282A36").pack(pady=5)
        self.entry_usuario = tk.Entry(master, font=("Arial", 12))
        self.entry_usuario.pack(pady=5)

        tk.Label(master, text="Senha:", font=("Arial", 12),
                 fg="white", bg="#282A36").pack(pady=5)
        self.entry_senha = tk.Entry(master, show="*", font=("Arial", 12))
        self.entry_senha.pack(pady=5)

        # --- Botão Entrar ---
        tk.Button(master, text="Entrar", bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold"), width=12,
                  command=self.verificar_login).pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "admin" and senha == "1234":
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.abrir_tela_portoes()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_tela_portoes(self):
        # Esconde a janela de login
        self.master.withdraw()

        # Abre a janela principal corretamente
        janela_principal = tk.Toplevel(self.master)
        TelaControlePortoes(janela_principal)

        # Quando fechar a principal → volta para tela de login
        janela_principal.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.voltar_login(janela_principal)
        )

    def voltar_login(self, janela):
        janela.destroy()
        self.master.deiconify()  # Reexibe o login!


# ==============================
# FUNÇÃO PRINCIPAL
# ==============================
def main():
    root = tk.Tk()
    TelaLogin(root)
    root.mainloop()


if __name__ == "__main__":
    main()
