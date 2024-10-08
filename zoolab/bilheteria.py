import tkinter as tk
from tkinter import messagebox
from database import inserir_bilheteria

class Bilheteria:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Controle de Bilheteria")
        self.window.geometry("400x300")
        
        tk.Label(self.window, text="Data:").pack(pady=5)
        self.data_entry = tk.Entry(self.window)
        self.data_entry.pack(pady=5)

        tk.Label(self.window, text="Quantidade de Ingressos:").pack(pady=5)
        self.ingressos_entry = tk.Entry(self.window)
        self.ingressos_entry.pack(pady=5)

        tk.Label(self.window, text="Valor Total:").pack(pady=5)
        self.valor_total_entry = tk.Entry(self.window)
        self.valor_total_entry.pack(pady=5)

        tk.Button(self.window, text="Salvar", command=self.salvar_bilheteria).pack(pady=20)

    def salvar_bilheteria(self):
        data = self.data_entry.get()
        quantidade_ingressos = self.ingressos_entry.get()
        valor_total = self.valor_total_entry.get()

        if data and quantidade_ingressos and valor_total:
            inserir_bilheteria(data, quantidade_ingressos, valor_total)
            messagebox.showinfo("Sucesso", "Bilheteria registrada com sucesso!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
