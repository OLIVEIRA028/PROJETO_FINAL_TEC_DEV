import tkinter as tk
import matplotlib.pyplot as plt
from database import sqlite3

class Metricas:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Métricas")
        self.window.geometry("400x300")
        
        tk.Button(self.window, text="Visualizar Animais por Espécie", command=self.grafico_especies).pack(pady=20)
        tk.Button(self.window, text="Visualizar Receita Bilheteria", command=self.grafico_bilheteria).pack(pady=20)

    def grafico_especies(self):
        conn = sqlite3.connect('data/zoologico.db')
        cursor = conn.cursor()
        cursor.execute('SELECT especie, COUNT(*) FROM animais GROUP BY especie')
        dados = cursor.fetchall()
        conn.close()

        especies = [row[0] for row in dados]
        quantidades = [row[1] for row in dados]

        plt.bar(especies, quantidades)
        plt.title("Quantidade de Animais por Espécie")
        plt.show()

    def grafico_bilheteria(self):
        conn = sqlite3.connect('data/zoologico.db')
        cursor = conn.cursor()
        cursor.execute('SELECT data, SUM(valor_total) FROM bilheteria GROUP BY data')
        dados = cursor.fetchall()
        conn.close()

        datas = [row[0] for row in dados]
        valores = [row[1] for row in dados]

        plt.plot(datas, valores)
        plt.title("Receita da Bilheteria por Data")
        plt.show()
