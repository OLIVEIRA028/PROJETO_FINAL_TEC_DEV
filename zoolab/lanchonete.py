import tkinter as tk
from tkinter import messagebox
from database import inserir_lanchonete

class Lanchonete:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Lanchonete")
        self.window.geometry("400x300")
        
        tk.Label(self.window, text="Produto:").pack(pady=5)
        self.produto_entry = tk.Entry(self.window)
        self.produto_entry.pack(pady=5)

        tk.Label(self.window, text="Quantidade:").pack(pady=5)
        self.quantidade_entry = tk.Entry(self.window)
        self.quantidade_entry.pack(pady=5)

        tk.Label(self.window, text="Valor Unitário:").pack(pady=5)
        self.valor_unitario_entry = tk.Entry(self.window)
        self.valor_unitario_entry.pack(pady=5)

        tk.Label(self.window, text="Valor Total:").pack(pady=5)
        self.valor_total_entry = tk.Entry(self.window)
        self.valor_total_entry.pack(pady=5)

        tk.Button(self.window, text="Salvar", command=self.salvar_lanchonete).pack(pady=20)

    def salvar_lanchonete(self):
        produto = self.produto_entry.get()
        quantidade = self.quantidade_entry.get()
        valor_unitario = self.valor_unitario_entry.get()
        valor_total = self.valor_total_entry.get()

        if produto and quantidade and valor_unitario and valor_total:
            inserir_lanchonete(produto, quantidade, valor_unitario, valor_total)
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
