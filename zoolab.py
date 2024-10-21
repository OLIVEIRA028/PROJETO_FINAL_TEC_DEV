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
        nome = request.form['nome']
        especie = request.form['especie']
        idade = request.form['idade']
        habitat = request.form['habitat']
        peso = request.form['peso']
        tipos_alimento = request.form['tipos_alimento'].split(',')

        if all([nome, especie, idade, habitat, peso, tipos_alimento]):
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO animais (nome, especie, idade, habitat, peso)
                                  VALUES (?, ?, ?, ?, ?)''', (nome, especie, idade, habitat, peso))
                animal_id = cursor.lastrowid  # Pega o ID do animal cadastrado

                # Cadastra os tipos de alimento
                for tipo in tipos_alimento:
                    cursor.execute('''INSERT INTO tipos_alimento (animal_id, tipo) VALUES (?, ?)''', (animal_id, tipo.strip()))

                conn.commit()
            flash("Animal cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro_animais'))
        else:
            flash("Preencha todos os campos!", "danger")

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habitat')
        habitats = cursor.fetchall()

    return render_template('cadastro_animais.html', habitats=habitats)

# Cadastro de Habitat
@app.route('/habitat/cadastro', methods=['GET', 'POST'])
def cadastro_habitat():
    if request.method == 'POST':
        nome_habitat = request.form['nome_habitat']
        if nome_habitat:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO habitat (nome) VALUES (?)''', (nome_habitat,))
                conn.commit()
            flash("Habitat cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro_habitat'))
        else:
            flash("Preencha todos os campos!", "danger")

    return render_template('cadastro_habitat.html')

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

# Edição de Animais
@app.route('/animais/editar/<int:id>', methods=['GET', 'POST'])
def editar_animal(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animais WHERE id = ?', (id,))
        animal = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        idade = request.form['idade']
        habitat = request.form['habitat']
        peso = request.form['peso']

        if all([nome, especie, idade, habitat, peso]):
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE animais SET nome = ?, especie = ?, idade = ?, habitat = ?, peso = ?
                                  WHERE id = ?''', (nome, especie, idade, habitat, peso, id))
                conn.commit()
            flash("Animal atualizado com sucesso!", "success")
            return redirect(url_for('visualizar_animais'))
        else:
            flash("Preencha todos os campos!", "danger")

    return render_template('editar_animal.html', animal=animal)

# Cadastro de Bilheteria
@app.route('/bilheteria', methods=['GET', 'POST'])
def bilheteria():
    today = datetime.today().strftime('%Y-%m-%d')
    valor_unitario_inteira = 19.99
    valor_unitario_meia = valor_unitario_inteira / 2  # 50% do valor

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
    data_atual = datetime.today().strftime('%Y-%m-%d')  # Obtém a data atual

    with connect_db() as conn:
        cursor = conn.cursor()
        for item in carrinho_bilheteria:
            cursor.execute('''INSERT INTO bilheteria (tipo_ingresso, quantidade_ingressos, valor_total, data)
                              VALUES (?, ?, ?, ?)''', (item['tipo_ingresso'], item['quantidade_ingressos'], item['valor_total'], data_atual))
        conn.commit()

    session.pop('carrinho_bilheteria', None)  # Limpa o carrinho da bilheteria
    flash(f"Venda da bilheteria registrada com sucesso! Total: R$ {total_geral:.2f}", "success")
    return redirect(url_for('bilheteria'))  # Redireciona de volta para a página de bilheteria

# Cadastro de Alimentação
@app.route('/animais/alimentacao', methods=['GET', 'POST'])
def alimentacao():
    today = datetime.today().strftime('%Y-%m-%d')
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
        quantidade = request.form['quantidade']
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

# Cadastro de Produtos
@app.route('/lanchonete/produtos/cadastro', methods=['GET', 'POST'])
def cadastro_produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        valor_unitario = request.form['valor_unitario']

        if nome and valor_unitario.replace('.', '', 1).isdigit():
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO produtos_lanchonete (nome, valor_unitario)
                                  VALUES (?, ?)''', (nome, valor_unitario))
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
        nome = request.form['nome']
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
        produto_id = int(request.form['produto'])  # Certifique-se de que seja um inteiro
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

            cursor.execute('''INSERT INTO lanchonete (produto, quantidade, valor_unitario, valor_total)
                              VALUES (?, ?, ?, ?)''', (item['id'], item['quantidade'], item['valor_unitario'], item['valor_total']))
        conn.commit()

    session.pop('carrinho', None)  # Limpa o carrinho após registrar a venda
    flash(f"Venda registrada com sucesso! Total: R$ {total_geral:.2f}", "success")  # Exibe o total na mensagem
    return redirect(url_for('lanchonete'))

# Métricas
@app.route('/metricas')
def metricas():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(quantidade_ingressos) FROM bilheteria')
        total_ingressos = cursor.fetchone()[0] or 0

        cursor.execute('SELECT SUM(valor_total) FROM bilheteria')
        total_lucro = cursor.fetchone()[0] or 0

        cursor.execute('SELECT produto, SUM(quantidade) FROM lanchonete GROUP BY produto ORDER BY SUM(quantidade) DESC LIMIT 5')
        produtos_populares = cursor.fetchall()

    return render_template('metricas.html', total_ingressos=total_ingressos, total_lucro=total_lucro, produtos_populares=produtos_populares)

# Inicializa o banco de dados e inicia o aplicativo
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
