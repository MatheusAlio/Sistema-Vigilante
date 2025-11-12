import tkinter as tk

root = tk.Tk()
root.title("Teste Tkinter")
root.geometry("400x200")
tk.Label(root, text="Se você vê isto, o Tkinter está funcionando!").pack(pady=50)
root.mainloop()
