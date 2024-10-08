import tkinter as tk
from tkinter import messagebox
from database import inserir_alimentacao

class Alimentacao:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Controle de Alimentação")
        self.window.geometry("400x300")
        
        tk.Label(self.window, text="Nome do Animal:").pack(pady=5)
        self.animal_entry = tk.Entry(self.window)
        self.animal_entry.pack(pady=5)

        tk.Label(self.window, text="Tipo de Alimento:").pack(pady=5)
        self.alimento_entry = tk.Entry(self.window)
        self.alimento_entry.pack(pady=5)

        tk.Label(self.window, text="Quantidade:").pack(pady=5)
        self.quantidade_entry = tk.Entry(self.window)
        self.quantidade_entry.pack(pady=5)

        tk.Label(self.window, text="Data:").pack(pady=5)
        self.data_entry = tk.Entry(self.window)
        self.data_entry.pack(pady=5)

        tk.Button(self.window, text="Salvar", command=self.salvar_alimentacao).pack(pady=20)

    def salvar_alimentacao(self):
        nome_animal = self.animal_entry.get()
        tipo_alimento = self.alimento_entry.get()
        quantidade = self.quantidade_entry.get()
        data = self.data_entry.get()

        if nome_animal and tipo_alimento and quantidade and data:
            inserir_alimentacao(nome_animal, tipo_alimento, quantidade, data)
            messagebox.showinfo("Sucesso", "Alimentação registrada com sucesso!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
