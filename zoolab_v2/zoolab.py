from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, connect_db

app = Flask(__name__)
app.secret_key = "zoologico_secret"  # Para o uso do flash messages

@app.route('/')
def index():
    return render_template('index.html')

# Cadastro de Animais
@app.route('/cadastro_animais', methods=['GET', 'POST'])
def cadastro_animais():
    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        idade = request.form['idade']
        habitat = request.form['habitat']
        peso = request.form['peso']

        if all([nome, especie, idade, habitat, peso]):
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO animais (nome, especie, idade, habitat, peso)
                                  VALUES (?, ?, ?, ?, ?)''', (nome, especie, idade, habitat, peso))
                conn.commit()
            flash("Animal cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro_animais'))
        else:
            flash("Preencha todos os campos!", "danger")
    
    return render_template('cadastro_animais.html')

# Visualização de Animais
@app.route('/visualizar_animais')
def visualizar_animais():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM animais')
        animais = cursor.fetchall()
    return render_template('visualizar_animais.html', animais=animais)

# Edição de Animais
@app.route('/editar_animal/<int:id>', methods=['GET', 'POST'])
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
    if request.method == 'POST':
        data = request.form['data']
        quantidade_ingressos = request.form['quantidade_ingressos']
        valor_total = request.form['valor_total']

        if data and quantidade_ingressos.isnumeric() and valor_total.replace('.', '', 1).isdigit():
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO bilheteria (data, quantidade_ingressos, valor_total)
                                  VALUES (?, ?, ?)''', (data, quantidade_ingressos, valor_total))
                conn.commit()
            flash("Venda registrada com sucesso!", "success")
            return redirect(url_for('bilheteria'))
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('bilheteria.html')

# Cadastro de Alimentação
@app.route('/alimentacao', methods=['GET', 'POST'])
def alimentacao():
    if request.method == 'POST':
        nome_animal = request.form['nome_animal']
        tipo_alimento = request.form['tipo_alimento']
        quantidade = request.form['quantidade']
        data = request.form['data']

        if all([nome_animal, tipo_alimento, quantidade.isnumeric(), data]):
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO alimentacao (nome_animal, tipo_alimento, quantidade, data)
                                  VALUES (?, ?, ?, ?)''', (nome_animal, tipo_alimento, quantidade, data))
                conn.commit()
            flash("Alimentação registrada com sucesso!", "success")
            return redirect(url_for('alimentacao'))
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('alimentacao.html')

# Cadastro de Produtos
@app.route('/cadastro_produtos', methods=['GET', 'POST'])
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

# Visualização de Produtos
@app.route('/visualizar_produtos')
def visualizar_produtos():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos_lanchonete')
        produtos = cursor.fetchall()
    return render_template('visualizar_produtos.html', produtos=produtos)

# Controle da Lanchonete
@app.route('/lanchonete', methods=['GET', 'POST'])
def lanchonete():
    produtos = []
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos_lanchonete')
        produtos = cursor.fetchall()

    if request.method == 'POST':
        produto_id = request.form['produto']
        quantidade = request.form['quantidade']

        if produto_id and quantidade.isnumeric():
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT valor_unitario FROM produtos_lanchonete WHERE id = ?', (produto_id,))
                valor_unitario = cursor.fetchone()
                if valor_unitario:
                    valor_total = float(valor_unitario[0]) * int(quantidade)
                    cursor.execute('''INSERT INTO lanchonete (produto, quantidade, valor_unitario, valor_total)
                                      VALUES (?, ?, ?, ?)''', (produto_id, quantidade, valor_unitario[0], valor_total))
                    conn.commit()
                    flash("Venda registrada com sucesso!", "success")
                    return redirect(url_for('lanchonete'))
                else:
                    flash("Produto não encontrado!", "danger")
        else:
            flash("Preencha todos os campos corretamente!", "danger")

    return render_template('lanchonete.html', produtos=produtos)

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
        animais_populares = cursor.fetchall()

    return render_template('metricas.html', total_ingressos=total_ingressos, total_lucro=total_lucro, animais_populares=animais_populares)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
