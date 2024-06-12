from flask import render_template, redirect, url_for, request
from flask import flash, jsonify
import os
from werkzeug.utils import secure_filename
from app import app, db
from models import Livro, Membro, Emprestimo, Autor, Genero 
from forms import *
from flask import jsonify


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

@app.route('/livros')
def livros():
    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)

@app.route('/livro/excluir/<int:livro_id>', methods=['POST'])
def excluir_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    
    # Verifique se há empréstimos associados ao livro
    if Emprestimo.query.filter_by(livro_id=livro_id).count() > 0:
        flash('Não é possível excluir o livro, pois há empréstimos associados a ele.', 'danger')
        return redirect(url_for('livros'))
    
    # Excluir o livro
    db.session.delete(livro)
    db.session.commit()
    
    flash('Livro excluído com sucesso!', 'success')
    return redirect(url_for('livros'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    form = LivroForm()

    # Carregar os autores e gêneros do banco de dados
    autores = [(autor.id, autor.nome) for autor in Autor.query.all()]
    form.autor_id.choices = autores

    generos = [(genero.id, genero.nome) for genero in Genero.query.all()]
    form.genero_id.choices = generos

    if form.validate_on_submit():
        # Lógica para salvar o livro no banco de dados
        novo_livro = Livro(
            titulo=form.titulo.data,
            autor_id=form.autor_id.data,
            ano_publicacao=form.ano_publicacao.data,
            genero_id=form.genero_id.data,
            disponivel=form.disponivel.data
        )
        db.session.add(novo_livro)
        db.session.commit()

        # Lógica para salvar a foto do livro
        if form.foto.data:
            filename = secure_filename(f"{novo_livro.titulo.replace(' ', '_')}.png")
            form.foto.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            novo_livro.url_da_capa = filename
            db.session.commit()

        flash('Livro adicionado com sucesso!', 'success')
        return redirect(url_for('adicionar_livro', mensagem='Livro adicionado com sucesso!'))

    return render_template('adicionar_livro.html', form=form)


@app.route('/livro/editar/<int:livro_id>', methods=['GET', 'POST'])
def editar_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    if request.method == 'POST':
        livro.titulo = request.form['titulo']
        livro.autor_id = request.form['autor_id']
        livro.ano_publicacao = request.form['ano_publicacao']
        livro.genero_id = request.form['genero_id']
        livro.disponivel = request.form['disponivel'] == '1'
        
        # Processar o upload da capa do livro
        if 'capa_upload' in request.files:
            file = request.files['capa_upload']
            if file and allowed_file(file.filename):
                # Certificar-se de que o diretório existe
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                livro.url_da_capa = filename
        
        db.session.commit()
        return redirect(url_for('livros'))  # Corrigido para 'livros' em vez de 'listar_livros'
    else:
        autores = Autor.query.all()
        generos = Genero.query.all()  # Adiciona consulta aos gêneros
        return render_template('editar_livro.html', livro=livro, autores=autores, generos=generos)

@app.route('/livros/<int:livro_id>')
def livro_detalhes(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    return render_template('livro_detalhes.html', livro=livro)



@app.route('/autores', methods=['GET'])
def listar_autores():
    autores = Autor.query.all()
    return render_template('autores.html', autores=autores)

@app.route('/adicionar_autor', methods=['GET', 'POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_autor = Autor(nome=nome)
        db.session.add(novo_autor)
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('adicionar_autor.html')

# Rota para editar um autor via interface web
@app.route('/editar_autor/<int:autor_id>', methods=['GET', 'POST'])
def editar_autor(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    if request.method == 'POST':
        autor.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('editar_autor.html', autor=autor)

# Rota para excluir um autor via interface web
@app.route('/excluir_autor/<int:autor_id>', methods=['POST'])
def excluir_autor_web(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    db.session.delete(autor)
    db.session.commit()
    return redirect(url_for('listar_autores'))

# Rota para criar um novo autor via API
@app.route('/api/autores', methods=['POST'])
def criar_autor():
    data = request.json
    novo_autor = Autor(**data)
    db.session.add(novo_autor)
    db.session.commit()
    return jsonify({'message': 'Autor criado com sucesso!', 'id': novo_autor.id}), 201

# Rota para listar todos os autores via API
@app.route('/api/autores', methods=['GET'])
def listar_autores_api():
    autores = Autor.query.all()
    return jsonify([autor.serialize() for autor in autores]), 200

# Rota para obter detalhes de um autor específico via API
@app.route('/api/autores/<int:id>', methods=['GET'])
def detalhes_autor(id):
    autor = Autor.query.get_or_404(id)
    return jsonify(autor.serialize()), 200

# Rota para atualizar informações de um autor via API
@app.route('/api/autores/<int:id>', methods=['PUT'])
def atualizar_autor(id):
    autor = Autor.query.get_or_404(id)
    data = request.json
    autor.nome = data.get('nome', autor.nome)
    db.session.commit()
    return jsonify({'message': 'Autor atualizado com sucesso!'}), 200

# Rota para excluir um autor via API
@app.route('/api/autores/<int:id>', methods=['DELETE'])
def excluir_autor_api(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    return jsonify({'message': 'Autor excluído com sucesso!'}), 200


@app.route('/emprestimos')
def emprestimos():
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/emprestimos/editar/<int:emprestimo_id>', methods=['GET', 'POST'])
def editar_emprestimo(emprestimo_id):
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    livros = Livro.query.all()
    membros = Membro.query.all()
    if request.method == 'POST':
        emprestimo.livro_id = request.form['livro_id']
        emprestimo.membro_id = request.form['membro_id']
        emprestimo.data_emprestimo = request.form['data_emprestimo']
        emprestimo.data_devolucao = request.form['data_devolucao']
        db.session.commit()
        return redirect(url_for('emprestimos'))
    return render_template('editar_emprestimo.html', emprestimo=emprestimo, livros=livros, membros=membros)

@app.route('/emprestimos/excluir/<int:emprestimo_id>', methods=['POST'])
def excluir_emprestimo(emprestimo_id):
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    db.session.delete(emprestimo)
    db.session.commit()
    return redirect(url_for('emprestimos'))

@app.route('/emprestimos/atualizar/<int:emprestimo_id>', methods=['GET', 'POST'])
def atualizar_emprestimo_route(emprestimo_id):  # Renomeando a função para evitar conflito
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    form = EmprestimoForm(obj=emprestimo)
    form.livro_id.choices = [(livro.id, livro.titulo) for livro in Livro.query.all()]
    form.membro_id.choices = [(membro.id, membro.nome) for membro in Membro.query.all()]

    if form.validate_on_submit():
        emprestimo.livro_id = form.livro_id.data
        emprestimo.membro_id = form.membro_id.data
        emprestimo.data_emprestimo = form.data_emprestimo.data
        emprestimo.data_devolucao = form.data_devolucao.data
        db.session.commit()
        flash('Empréstimo atualizado com sucesso!', 'success')
        return redirect(url_for('emprestimos'))

    return render_template('atualizar_emprestimo.html', form=form, emprestimo=emprestimo)

@app.route('/emprestimos/adicionar', methods=['GET', 'POST'])
def adicionar_emprestimo():
    form = EmprestimoForm()
    livros_disponiveis = Livro.query.filter_by(disponivel=True).all()
    form.livro_id.choices = [(livro.id, livro.titulo) for livro in livros_disponiveis]
    membros = Membro.query.all()
    form.membro_id.choices = [(membro.id, membro.nome) for membro in membros]

    if form.validate_on_submit():
        emprestimo = Emprestimo(
            livro_id=form.livro_id.data,
            membro_id=form.membro_id.data,
            data_emprestimo=form.data_emprestimo.data,
            data_devolucao=form.data_devolucao.data
        )
        livro = Livro.query.get(form.livro_id.data)
        livro.disponivel = False
        db.session.add(emprestimo)
        db.session.commit()
        return redirect(url_for('emprestimos'))
    
    return render_template('adicionar_emprestimo.html', form=form)

@app.route('/emprestimos/criar', methods=['POST'])
def criar_emprestimo():
    data = request.json
    novo_emprestimo = Emprestimo(**data)
    db.session.add(novo_emprestimo)
    db.session.commit()
    return jsonify({'message': 'Empréstimo criado com sucesso!', 'id': novo_emprestimo.id}), 201

@app.route('/emprestimos/listar', methods=['GET'])
def listar_emprestimos():
    emprestimos = Emprestimo.query.all()
    return jsonify([emprestimo.serialize() for emprestimo in emprestimos]), 200

@app.route('/emprestimos/detalhes/<int:id>', methods=['GET'])
def detalhes_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    return jsonify(emprestimo.serialize()), 200

@app.route('/emprestimos/atualizar/<int:id>', methods=['PUT'])
def atualizar_emprestimo_put(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    data = request.json
    emprestimo.data_devolucao = data.get('data_devolucao', emprestimo.data_devolucao)
    db.session.commit()
    return jsonify({'message': 'Empréstimo atualizado com sucesso!'}), 200

@app.route('/membros')
def listar_membros():
    membros = Membro.query.all()
    return render_template('membros.html', membros=membros)

@app.route('/adicionar_membro', methods=['GET', 'POST'])
def adicionar_membro_form():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_membro = Membro(nome=nome)
        db.session.add(novo_membro)
        db.session.commit()
        return redirect(url_for('listar_membros'))
    return render_template('adicionar_membro.html')

# Rota para listar todos os membros via API
@app.route('/api/membros', methods=['GET'])
def listar_membros_api():
    membros = Membro.query.all()
    return jsonify([membro.serialize() for membro in membros]), 200

# Rota para criar um novo membro via API
@app.route('/api/membros', methods=['POST'])
def criar_membro_api():
    data = request.json
    novo_membro = Membro(**data)
    db.session.add(novo_membro)
    db.session.commit()
    return jsonify({'message': 'Membro criado com sucesso!', 'id': novo_membro.id}), 201

# Rota para obter detalhes de um membro específico via API
@app.route('/api/membros/<int:id>', methods=['GET'])
def detalhes_membro_api(id):
    membro = Membro.query.get_or_404(id)
    return jsonify(membro.serialize()), 200

@app.route('/membros/atualizar/<int:membro_id>', methods=['GET', 'POST'])
def atualizar_membro(membro_id):
    membro = Membro.query.get_or_404(membro_id)
    form = MembroForm(obj=membro)
    if form.validate_on_submit():
        form.populate_obj(membro)
        db.session.commit()
        return redirect(url_for('listar_membros'))  # Redireciona para a página de listagem de membros
    return render_template('atualizar_membro.html', form=form)


@app.route('/membro/editar/<int:membro_id>', methods=['GET', 'POST'])
def editar_membro(membro_id):
    membro = Membro.query.get_or_404(membro_id)
    if request.method == 'POST':
        membro.nome = request.form['nome']
        membro.email = request.form['email']
        membro.telefone = request.form['telefone']
        db.session.commit()
        return redirect(url_for('listar_membros'))
    return render_template('editar_membro.html', membro=membro)


# Rota para excluir um membro via interface web
@app.route('/excluir_membro/<int:membro_id>', methods=['POST'])
def excluir_membro(membro_id):
    membro = Membro.query.get_or_404(membro_id)
    db.session.delete(membro)
    db.session.commit()
    flash('Membro excluído com sucesso!', 'success')
    return redirect(url_for('listar_membros'))



init_routes(app)
