import sqlite3

# Função para inicializar o banco de dados
def init_db():
    # Garantir que a pasta 'data' exista
    import os
    if not os.path.exists('data'):
        os.makedirs('data')

    # Conectar ao banco de dados
    with sqlite3.connect('data/zoologico.db') as conn:
        cursor = conn.cursor()

        # Criar tabela para Animais
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            idade INTEGER NOT NULL,
            habitat TEXT NOT NULL
        )
        ''')

        # Criar tabela para Bilheteria
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bilheteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            quantidade_ingressos INTEGER NOT NULL,
            valor_total REAL NOT NULL
        )
        ''')

        # Criar tabela para Alimentação
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_animal TEXT NOT NULL,
            tipo_alimento TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL
        )
        ''')

        # Criar tabela para a Lanchonete
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lanchonete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total REAL NOT NULL
        )
        ''')

        # Salvar mudanças no banco
        conn.commit()

# Função para inserir um novo animal
def inserir_animal(nome, especie, idade, habitat):
    try:
        with sqlite3.connect('data/zoologico.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO animais (nome, especie, idade, habitat) 
            VALUES (?, ?, ?, ?)
            ''', (nome, especie, idade, habitat))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir animal: {e}")

# Função para inserir dados de bilheteria
def inserir_bilheteria(data, quantidade_ingressos, valor_total):
    try:
        with sqlite3.connect('data/zoologico.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO bilheteria (data, quantidade_ingressos, valor_total) 
            VALUES (?, ?, ?)
            ''', (data, quantidade_ingressos, valor_total))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir bilheteria: {e}")

# Função para inserir dados de alimentação
def inserir_alimentacao(nome_animal, tipo_alimento, quantidade, data):
    try:
        with sqlite3.connect('data/zoologico.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO alimentacao (nome_animal, tipo_alimento, quantidade, data)
            VALUES (?, ?, ?, ?)
            ''', (nome_animal, tipo_alimento, quantidade, data))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir alimentação: {e}")

# Função para inserir dados de venda da lanchonete
def inserir_lanchonete(produto, quantidade, valor_unitario, valor_total):
    try:
        with sqlite3.connect('data/zoologico.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO lanchonete (produto, quantidade, valor_unitario, valor_total)
            VALUES (?, ?, ?, ?)
            ''', (produto, quantidade, valor_unitario, valor_total))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir venda da lanchonete: {e}")
