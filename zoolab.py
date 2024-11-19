from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, connect_db
from datetime import datetime

# Inicializa o aplicativo Flask
app = Flask(__name__)
app.secret_key = "zoologico_secret"  # Chave secreta para mensagens de flash

# Rota principal que renderiza a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Cadastro de Animais
@app.route('/animais/cadastro', methods=['GET', 'POST'])
def cadastro_animais():
    if request.method == 'POST':
        nome = request.form['nome'].upper()
        especie = request.form['especie'].upper()
        idade = request.form['idade']
        habitat_id = request.form['habitat']  # Alterado para habitat_id
        peso = request.form['peso'].replace(',', '.')
        tipos_alimento = request.form['tipos_alimento'].upper().split(',')

        try:
            peso = float(peso)
        except ValueError:
            flash("Peso inválido. Por favor, insira um número válido.", "danger")
            return redirect(url_for('cadastro_animais'))

        # Verifica se todos os campos estão preenchidos corretamente
        if all([nome, especie, idade, habitat_id, peso is not None, tipos_alimento]):
            with connect_db() as conn:
                cursor = conn.cursor()

                # Verifica se o animal já existe
                cursor.execute('''SELECT * FROM animais WHERE nome = ? AND especie = ?''', (nome, especie))
                if cursor.fetchone() is None:  # Se não houver duplicata
                    # Inserir o animal
                    cursor.execute('''INSERT INTO animais (nome, especie, idade, habitat_id, peso)
                                      VALUES (?, ?, ?, ?, ?)''', (nome, especie, idade, habitat_id, peso))
                    animal_id = cursor.lastrowid  # Pega o ID do animal cadastrado

                    # Cadastra os tipos de alimento
                    tipos_cadastrados = set()
                    for tipo in tipos_alimento:
                        tipo = tipo.strip()
                        if tipo not in tipos_cadastrados: 
                            # Verifica se o tipo de alimento já está associado a algum animal
                            cursor.execute('''SELECT * FROM tipos_alimento WHERE tipo = ?''', (tipo,))
                            if not cursor.fetchone():  # Se o tipo de alimento não existir em nenhum animal, insere
                                cursor.execute('''INSERT INTO tipos_alimento (animal_id, tipo) VALUES (?, ?)''', (animal_id, tipo))
                                tipos_cadastrados.add(tipo)
                    conn.commit()
                    flash("Animal cadastrado com sucesso!", "success")
                else:
                    flash("Este animal já está cadastrado!", "danger")

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitat')
        habitats = cursor.fetchall()

    return render_template('cadastro_animais.html', habitats=habitats)

# Remover Animal
@app.route('/animais/remover/<int:id>', methods=['POST'])
def remover_animal(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        # Primeiro, removemos os tipos de alimento associados ao animal
        cursor.execute('DELETE FROM tipos_alimento WHERE animal_id = ?', (id,))
        # Depois, removemos o animal
        cursor.execute('DELETE FROM animais WHERE id = ?', (id,))
        conn.commit()
    flash("Animal removido com sucesso!", "success")
    return redirect(url_for('visualizar_animais'))

# Cadastro de Habitat
@app.route('/habitat/cadastro', methods=['GET', 'POST'])
def cadastro_habitat():
    if request.method == 'POST':
        nome_habitat = request.form['nome_habitat'].upper()
        if nome_habitat:
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Verifica se o habitat já existe
                cursor.execute('''SELECT * FROM habitat WHERE nome = ?''', (nome_habitat,))
                if cursor.fetchone() is None:  # Se não houver duplicata
                    cursor.execute('''INSERT INTO habitat (nome) VALUES (?)''', (nome_habitat,))
                    conn.commit()
                    flash("Habitat cadastrado com sucesso!", "success")
                else:
                    flash("Habitat já cadastrado!", "danger")
                return redirect(url_for('cadastro_habitat'))
        else:
            flash("Preencha todos os campos!", "danger")

    return render_template('cadastro_habitat.html')

# Remover Habitat
@app.route('/habitat/remover/<int:id>', methods=['POST'])
def remover_habitat(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Verifica se o habitat está associado a algum animal
        cursor.execute('SELECT nome FROM animais WHERE habitat_id = ?', (id,))
        animais_associados = cursor.fetchall()
        
        if animais_associados:
            # Cria uma lista com os nomes dos animais associados
            nomes_animais = ', '.join([animal[0] for animal in animais_associados])
            flash(f"Não é possível remover o habitat, pois está associado aos seguintes animais: {nomes_animais}.", "danger")
        else:
            # Se não houver animais associados, remove o habitat
            cursor.execute('DELETE FROM habitat WHERE id = ?', (id,))
            conn.commit()
            flash("Habitat removido com sucesso!", "success")
    
    return redirect(url_for('visualizar_habitats'))

# Editar Habitat
@app.route('/habitat/editar/<int:id>', methods=['GET', 'POST'])
def editar_habitat(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        
        if request.method == 'POST':
            novo_nome = request.form['nome_habitat'].upper()
            cursor.execute('UPDATE habitat SET nome = ? WHERE id = ?', (novo_nome, id))
            conn.commit()
            flash("Habitat atualizado com sucesso!", "success")
            return redirect(url_for('visualizar_habitats'))

        # Obter dados do habitat para preencher o formulário
        cursor.execute('SELECT * FROM habitat WHERE id = ?', (id,))
        habitat = cursor.fetchone()

    return render_template('editar_habitat.html', habitat=habitat)

# Visualização dos habitats
@app.route('/habitat/visualizar', methods=['GET'])
def visualizar_habitats():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitat')
        habitats = cursor.fetchall()
    
    return render_template('visualizar_habitats.html', habitats=habitats)

# Visualização de Animais
@app.route('/animais/visualizar')
def visualizar_animais():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animais')
        animais = cursor.fetchall()

        # Busca registros de alimentação
        alimentacoes = {}
        for animal in animais:
            cursor.execute('SELECT tipo_alimento, quantidade, data, hora FROM alimentacao WHERE nome_animal = ?', (animal[1],))
            alimentacoes[animal[1]] = cursor.fetchall()

    return render_template('visualizar_animais.html', animais=animais, alimentacoes=alimentacoes)

# Remover Animal
@app.route('/animais/remover/<int:id>', methods=['POST'])
def remover_animal_por_id(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tipos_alimento WHERE animal_id = ?', (id,))
        cursor.execute('DELETE FROM animais WHERE id = ?', (id,))
        conn.commit()
    flash("Animal removido com sucesso!", "success")
    return redirect(url_for('visualizar_animais'))

# Edição de Animais
@app.route('/animais/editar/<int:id>', methods=['GET', 'POST'])
def editar_animal(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animais WHERE id = ?', (id,))
        animal = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome'].upper()  
        especie = request.form['especie'].upper()  
        idade = request.form['idade']
        habitat_id = request.form['habitat']  # Alterado para habitat_id
        peso = request.form['peso'].strip()  # Mantém o valor original e remove espaços

        try:
            peso = float(peso.replace(',', '.')) 
        except ValueError:
            peso = 0.0  # Define um valor padrão caso a conversão falhe

        if all([nome, especie, idade, habitat_id, peso >= 0]):  # Verifica se o peso é não-negativo
            with connect_db() as conn:
                cursor = conn.cursor()

                # Verifica se já existe outro animal com o mesmo nome e espécie
                cursor.execute('''SELECT * FROM animais WHERE nome = ? AND especie = ? AND id != ?''', (nome, especie, id))
                if cursor.fetchone() is None:  # Se não houver duplicata
                    cursor.execute('''UPDATE animais SET nome = ?, especie = ?, idade = ?, habitat_id = ?, peso = ?
                                      WHERE id = ?''', (nome, especie, idade, habitat_id, peso, id))
                    conn.commit()
                    flash("Animal atualizado com sucesso!", "success")
                    return redirect(url_for('visualizar_animais'))
                else:
                    flash("Já existe um animal cadastrado com este nome e espécie!", "danger")
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('editar_animal.html', animal=animal)

# Cadastro de Alimentação
@app.route('/animais/alimentacao', methods=['GET', 'POST'])
def alimentacao():
    today = datetime.today().strftime('%d-%m-%Y')
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM animais')
        animais = cursor.fetchall()

        # Busca os tipos de alimento cadastrados
        cursor.execute('SELECT tipo FROM tipos_alimento')
        tipos_alimento = cursor.fetchall()

    if request.method == 'POST':
        nome_animal = request.form['nome_animal']
        tipo_alimento = request.form['tipo_alimento']
        quantidade = request.form['quantidade']  # Mantido para alimentação
        hora = request.form['hora']  # Hora da alimentação

        if all([nome_animal, tipo_alimento, quantidade.replace('.', '', 1).isdigit(), hora]):
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO alimentacao (nome_animal, tipo_alimento, quantidade, data, hora)
                                  VALUES (?, ?, ?, ?, ?)''', (nome_animal, tipo_alimento, quantidade, today, hora))
                conn.commit()
            flash("Alimentação registrada com sucesso!", "success")
            return redirect(url_for('alimentacao'))
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('alimentacao.html', animais=animais, tipos_alimento=tipos_alimento)

# Cadastro de Bilheteria
@app.route('/bilheteria', methods=['GET', 'POST'])
def bilheteria():
    today = datetime.today().strftime('%d-%m-%Y')

    # Conectar ao banco de dados e buscar os valores
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT valor_unitario_inteira, valor_unitario_meia FROM configuracoes WHERE id = 1")
        valores = cursor.fetchone()
        
        if valores:
            valor_unitario_inteira, valor_unitario_meia = valores
        else:
            valor_unitario_inteira = 19.99
            valor_unitario_meia = valor_unitario_inteira / 2

    if request.method == 'POST':
        quantidade_ingressos = int(request.form['quantidade_ingressos'])
        tipo_ingresso = request.form['tipo_ingresso']

        valor_unitario = valor_unitario_inteira if tipo_ingresso == 'inteira' else valor_unitario_meia
        valor_total = quantidade_ingressos * valor_unitario

        # Adiciona o ingresso ao carrinho
        if 'carrinho_bilheteria' not in session:
            session['carrinho_bilheteria'] = []

        # Verifica se o ingresso já está no carrinho
        for item in session['carrinho_bilheteria']:
            if item['tipo_ingresso'] == tipo_ingresso:
                item['quantidade_ingressos'] += quantidade_ingressos
                item['valor_total'] += valor_total
                break
        else:
            # Adiciona novo ingresso ao carrinho
            session['carrinho_bilheteria'].append({
                'tipo_ingresso': tipo_ingresso,
                'quantidade_ingressos': quantidade_ingressos,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total
            })

        session.modified = True  # Marca a sessão como modificada
        flash("Ingresso adicionado ao carrinho!", "success")
        return redirect(url_for('bilheteria'))

    # Calcular o total geral do carrinho
    total_geral = sum(item['valor_total'] for item in session.get('carrinho_bilheteria', []))

    return render_template('bilheteria.html', today=today, carrinho_bilheteria=session.get('carrinho_bilheteria', []), total_geral=total_geral)

# Rota para remover ingresso do carrinho
@app.route('/remover_ingresso/<int:index>', methods=['POST'])
def remover_ingresso(index):
    if 'carrinho_bilheteria' in session:
        session['carrinho_bilheteria'].pop(index)  # Remove o ingresso do carrinho
        session.modified = True
        flash("Ingresso removido do carrinho!", "success")
    return redirect(url_for('bilheteria'))

# Rota para registrar a venda da bilheteria
@app.route('/registrar_venda_bilheteria', methods=['POST'])
def registrar_venda_bilheteria():
    carrinho_bilheteria = session.get('carrinho_bilheteria', [])
    total_geral = sum(item['valor_total'] for item in carrinho_bilheteria) or 0
    data_atual = datetime.today().strftime('%d-%m-%Y')  # Obtém a data atual

    with connect_db() as conn:
        cursor = conn.cursor()
        for item in carrinho_bilheteria:
            cursor.execute('''INSERT INTO bilheteria (tipo_ingresso, quantidade_ingressos, valor_total, data)
                              VALUES (?, ?, ?, ?)''', (item['tipo_ingresso'], item['quantidade_ingressos'], item['valor_total'], data_atual))
        conn.commit()

    session.pop('carrinho_bilheteria', None)  # Limpa o carrinho da bilheteria
    flash(f"Venda da bilheteria registrada com sucesso! Total: R$ {total_geral:.2f}", "success")
    return redirect(url_for('bilheteria'))  # Redireciona de volta para a página de bilheteria

# Alteração de Valores Bilheteria
@app.route('/gerenciar_valores', methods=['GET', 'POST'])
def gerenciar_valores():
    # Conectar ao banco de dados
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Buscar os valores atuais do banco de dados
        cursor.execute("SELECT valor_unitario_inteira, valor_unitario_meia FROM configuracoes WHERE id = 1")
        valores = cursor.fetchone()
        
        if valores:
            valor_unitario_inteira, valor_unitario_meia = valores
        else:
            # Se não existir, use valores padrão
            valor_unitario_inteira = 19.99
            valor_unitario_meia = valor_unitario_inteira / 2

        if request.method == 'POST':
            novo_valor_inteira = float(request.form['valor_inteira'])
            novo_valor_meia = novo_valor_inteira / 2

            # Atualizar valores no banco de dados
            cursor.execute("UPDATE configuracoes SET valor_unitario_inteira = ?, valor_unitario_meia = ? WHERE id = 1",
                           (novo_valor_inteira, novo_valor_meia))
            conn.commit()

            flash("Valores atualizados com sucesso!", "success")
            return redirect(url_for('bilheteria'))

    return render_template('bilheteria_valores.html', valor_inteira=valor_unitario_inteira)


# Cadastro de Produtos
@app.route('/lanchonete/produtos/cadastro', methods=['GET', 'POST'])
def cadastro_produtos():
    if request.method == 'POST':
        nome = request.form.get('nome').upper()  # Converte para maiúsculas
        valor_unitario = request.form.get('valor_unitario')
        quantidade = request.form.get('quantidade', '0')  # Mantém como string

        if nome and valor_unitario and valor_unitario.replace('.', '', 1).isdigit() and quantidade.isdigit():
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Verifica se o produto já existe
                cursor.execute('SELECT * FROM produtos_lanchonete WHERE nome = ?', (nome,))
                if cursor.fetchone() is not None:
                    flash("Produto já cadastrado!", "danger")
                else:
                    data_atual = datetime.today().strftime('%Y-%m-%d')  # Obtém a data atual
                    cursor.execute('''INSERT INTO produtos_lanchonete (nome, valor_unitario, quantidade, data)
                                      VALUES (?, ?, ?, ?)''', (nome, valor_unitario, quantidade, data_atual))
                    conn.commit()
                    flash("Produto cadastrado com sucesso!", "success")
                    return redirect(url_for('cadastro_produtos'))
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('cadastro_produtos.html')

# Edição de Produtos
@app.route('/lanchonete/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos_lanchonete WHERE id = ?', (id,))
        produto = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome'].upper()  # Converte para maiúsculas
        valor_unitario = request.form['valor_unitario']

        if nome and valor_unitario.replace('.', '', 1).isdigit():
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE produtos_lanchonete SET nome = ?, valor_unitario = ?
                                  WHERE id = ?''', (nome, valor_unitario, id))
                conn.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for('visualizar_produtos'))
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('editar_produto.html', produto=produto)

# Visualização de Produtos
@app.route('/lanchonete/produtos/visualizar', methods=['GET', 'POST'])
def visualizar_produtos():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos_lanchonete')
        produtos = cursor.fetchall()

    return render_template('visualizar_produtos.html', produtos=produtos)

# Rota para remover produtos
@app.route('/lanchonete/produtos/remover/<int:id>', methods=['POST'])
def remover_produto(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produtos_lanchonete WHERE id = ?', (id,))
        conn.commit()
    flash("Produto removido com sucesso!", "success")
    return redirect(url_for('visualizar_produtos'))

# Controle da Lanchonete
@app.route('/lanchonete', methods=['GET', 'POST'])
def lanchonete():
    if 'carrinho' not in session:
        session['carrinho'] = []

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos_lanchonete')
        produtos = cursor.fetchall()

    if request.method == 'POST':
        produto_id = int(request.form['produto']) 
        quantidade = int(request.form['quantidade'])

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome, valor_unitario FROM produtos_lanchonete WHERE id = ?', (produto_id,))
            produto = cursor.fetchone()

            if produto:
                # Verifica se o produto já está no carrinho
                for item in session['carrinho']:
                    if item['id'] == produto_id:
                        item['quantidade'] += quantidade
                        item['valor_total'] += produto[1] * quantidade
                        break
                else:
                    # Adiciona novo produto ao carrinho
                    valor_total = produto[1] * quantidade
                    session['carrinho'].append({
                        'id': produto_id,
                        'nome': produto[0],
                        'quantidade': quantidade,
                        'valor_unitario': produto[1],
                        'valor_total': valor_total
                    })

                session.modified = True  # Marca a sessão como modificada
                flash("Produto adicionado ao carrinho!", "success")
                return redirect(url_for('lanchonete'))

    total_geral = sum(item['valor_total'] for item in session['carrinho'])
    return render_template('lanchonete.html', produtos=produtos, carrinho=session['carrinho'], total_geral=total_geral)

# Rota para remover do carrinho
@app.route('/remover/<int:index>', methods=['POST'])
def remover_do_carrinho(index):
    if 'carrinho' in session:
        session['carrinho'].pop(index)  # Remove o produto do carrinho
        session.modified = True
        flash("Produto removido do carrinho!", "success")
    return redirect(url_for('lanchonete'))

# Rota para registrar a venda da lanchonete
@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    total_geral = sum(item['valor_total'] for item in session['carrinho'])  # Calcula o total

    with connect_db() as conn:
        cursor = conn.cursor()
        for item in session['carrinho']:
            if 'id' not in item:
                continue  # Pula itens sem ID

            cursor.execute('''INSERT INTO lanchonete (produto, quantidade, valor_unitario, valor_total, data)
                              VALUES (?, ?, ?, ?, ?)''', (item['id'], item['quantidade'], item['valor_unitario'], item['valor_total'], datetime.today().strftime('%Y-%m-%d')))
        conn.commit()

    session.pop('carrinho', None)  # Limpa o carrinho após registrar a venda
    flash(f"Venda registrada com sucesso! Total: R$ {total_geral:.2f}", "success")  # Exibe o total na mensagem
    return redirect(url_for('lanchonete'))

#Metricas
@app.route('/metricas', methods=['GET', 'POST'])
def metricas():
    data_inicial = request.form.get('data_inicial')
    data_final = request.form.get('data_final')

    with connect_db() as conn:
        cursor = conn.cursor()

        # Detalhes dos ingressos vendidos
        if data_inicial and data_final:
            cursor.execute('''
                SELECT tipo_ingresso, SUM(quantidade_ingressos) AS quantidade_total, 
                       SUM(valor_total) AS valor_total
                FROM bilheteria
                WHERE data BETWEEN ? AND ?
                GROUP BY tipo_ingresso
            ''', (data_inicial, data_final))
        else:
            cursor.execute('''
                SELECT tipo_ingresso, SUM(quantidade_ingressos) AS quantidade_total, 
                       SUM(valor_total) AS valor_total
                FROM bilheteria
                GROUP BY tipo_ingresso
            ''')

        ingressos_detalhados = cursor.fetchall()

        # Calcular o lucro total de bilheteria
        total_ingressos = sum(row[1] for row in ingressos_detalhados)
        total_lucro = sum(row[2] for row in ingressos_detalhados)

        # Produtos mais populares
        if data_inicial and data_final:
            cursor.execute('''
                SELECT p.nome, SUM(l.quantidade), SUM(l.quantidade * p.valor_unitario) AS valor_total
                FROM lanchonete l
                JOIN produtos_lanchonete p ON l.produto = p.id
                WHERE l.data BETWEEN ? AND ?
                GROUP BY p.nome
                ORDER BY SUM(l.quantidade) DESC
                LIMIT 5
            ''', (data_inicial, data_final))
        else:
            cursor.execute('''
                SELECT p.nome, SUM(l.quantidade), SUM(l.quantidade * p.valor_unitario) AS valor_total
                FROM lanchonete l
                JOIN produtos_lanchonete p ON l.produto = p.id
                GROUP BY p.nome
                ORDER BY SUM(l.quantidade) DESC
                LIMIT 5
            ''')

        produtos_populares = cursor.fetchall()

        # Calcular o valor total de produtos vendidos
        valor_total_produtos = sum(produto[2] for produto in produtos_populares)

        # Calcular o lucro total do zoológico
        lucro_total_zoo = total_lucro + valor_total_produtos

    return render_template('metricas.html',
                           ingressos_detalhados=ingressos_detalhados,
                           total_ingressos=total_ingressos,
                           total_lucro=total_lucro,
                           produtos_populares=produtos_populares,
                           valor_total_produtos=valor_total_produtos,
                           lucro_total_zoo=lucro_total_zoo)

# Inicializa o banco de dados e inicia o aplicativo
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
