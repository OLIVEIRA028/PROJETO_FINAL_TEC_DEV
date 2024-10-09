import tkinter as tk
from tkinter import messagebox

class CadastroAnimais:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Cadastro de Animais")
        self.window.geometry("400x300")
        
        # Campos de cadastro
        tk.Label(self.window, text="Nome do Animal:").pack(pady=5)
        self.nome_entry = tk.Entry(self.window)
        self.nome_entry.pack(pady=5)

        tk.Label(self.window, text="Espécie:").pack(pady=5)
        self.especie_entry = tk.Entry(self.window)
        self.especie_entry.pack(pady=5)

        tk.Label(self.window, text="Idade:").pack(pady=5)
        self.idade_entry = tk.Entry(self.window)
        self.idade_entry.pack(pady=5)

        tk.Label(self.window, text="Habitat:").pack(pady=5)
        self.habitat_entry = tk.Entry(self.window)
        self.habitat_entry.pack(pady=5)
        
        # Botão para salvar os dados
        tk.Button(self.window, text="Salvar", command=self.salvar_animal).pack(pady=20)

    def salvar_animal(self):
        nome = self.nome_entry.get()
        especie = self.especie_entry.get()
        idade = self.idade_entry.get()
        habitat = self.habitat_entry.get()
        
        # Validação simples de preenchimento
        if nome and especie and idade and habitat:
            # Aqui você poderia salvar os dados no banco de dados
            messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
