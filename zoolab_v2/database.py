# database.py
import sqlite3
import os

DATABASE = os.path.join('data', 'database.db')

def connect_db():
    return sqlite3.connect(DATABASE)

# Inicializa o banco de dados
def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Tabela de Animais
        cursor.execute('''CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, especie TEXT, idade INTEGER, habitat TEXT, peso REAL)''')
        
        # Tabela de Bilheteria
        cursor.execute('''CREATE TABLE IF NOT EXISTS bilheteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT, quantidade_ingressos INTEGER, valor_total REAL)''')
        
        # Tabela de Alimentação
        cursor.execute('''CREATE TABLE IF NOT EXISTS alimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_animal TEXT, tipo_alimento TEXT, quantidade INTEGER, data TEXT)''')
        
        # Tabela de Lanchonete
        cursor.execute('''CREATE TABLE IF NOT EXISTS lanchonete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT, quantidade INTEGER, valor_unitario REAL, valor_total REAL)''')
        
        # Tabela de Produtos da Lanchonete
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos_lanchonete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, valor_unitario REAL)''')
        
        conn.commit()
