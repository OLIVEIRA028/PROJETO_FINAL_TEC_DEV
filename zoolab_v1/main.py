import tkinter as tk
from tkinter import messagebox
from cadastro_animais import CadastroAnimais
from bilheteria import Bilheteria
from alimentacao import Alimentacao
from metricas import Metricas
from lanchonete import Lanchonete
from database import init_db  

class ZoologicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Zoológico")
        self.root.geometry("600x400")
        
        # Inicializa o banco de dados
        init_db()

        # Criando o menu principal
        menubar = tk.Menu(self.root)

        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Cadastrar Animais", command=self.abrir_cadastro_animais)
        menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

        menu_alimentacao = tk.Menu(menubar, tearoff=0)
        menu_alimentacao.add_command(label="Controle de Alimentação", command=self.abrir_controle_alimentacao)
        menubar.add_cascade(label="Alimentação", menu=menu_alimentacao)

        menu_bilheteria = tk.Menu(menubar, tearoff=0)
        menu_bilheteria.add_command(label="Controle de Bilheteria", command=self.abrir_bilheteria)
        menubar.add_cascade(label="Bilheteria", menu=menu_bilheteria)

        menu_metricas = tk.Menu(menubar, tearoff=0)
        menu_metricas.add_command(label="Ver Métricas", command=self.abrir_metricas)
        menubar.add_cascade(label="Métricas", menu=menu_metricas)

        menu_lanchonete = tk.Menu(menubar, tearoff=0)
        menu_lanchonete.add_command(label="Lanchonete", command=self.abrir_lanchonete)
        menubar.add_cascade(label="Lanchonete", menu=menu_lanchonete)

        self.root.config(menu=menubar)

    def abrir_cadastro_animais(self):
        CadastroAnimais(self.root)

    def abrir_controle_alimentacao(self):
        Alimentacao(self.root)

    def abrir_bilheteria(self):
        Bilheteria(self.root)

    def abrir_metricas(self):
        Metricas(self.root)

    def abrir_lanchonete(self):
        Lanchonete(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = ZoologicoApp(root)
    root.mainloop()
