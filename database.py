# database.py
import sqlite3
import os

DATABASE = os.path.join('data', 'database.db')

def connect_db():
    """Conecta ao banco de dados SQLite."""
    return sqlite3.connect(DATABASE)

def init_db():
    """Inicializa o banco de dados, criando as tabelas necessárias."""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Tabela de Animais
        cursor.execute('''CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            idade INTEGER,
            habitat TEXT,
            peso REAL)''')
        
        # Tabela de Bilheteria
        cursor.execute('''CREATE TABLE IF NOT EXISTS bilheteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            quantidade_ingressos INTEGER NOT NULL,
            valor_total REAL NOT NULL)''')
        
        # Tabela de Alimentação
        cursor.execute('''CREATE TABLE IF NOT EXISTS alimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_animal TEXT NOT NULL,
            tipo_alimento TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL)''')
        
        # Tabela de Lanchonete
        cursor.execute('''CREATE TABLE IF NOT EXISTS lanchonete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL)''')
        
        # Tabela de Produtos da Lanchonete
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos_lanchonete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_unitario REAL NOT NULL)''')
        
        conn.commit()

if __name__ == "__main__":
    init_db()
