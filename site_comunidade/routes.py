from flask import render_template, url_for, request, flash, redirect, abort
from site_comunidade.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost
from site_comunidade.models import Usuario, Post
from site_comunidade import app, database, bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image





@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/usuarios')
@login_required
def usuarios():
    lista = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():   
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'btn_submit_login' in request.form:
        user = Usuario.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form_login.senha.data):
            login_user(user, remember=form_login.lembrar_login.data)
            flash('Login realizado com sucesso', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login, e-mail ou senha inválidos', 'alert-danger')
    if form_criar_conta.validate_on_submit() and 'btn_submit_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        return redirect(url_for('home'))

    return render_template('cadastro.html', form_criar_conta=form_criar_conta, form_login=form_login)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso', 'alert-success')
    return redirect(url_for('home'))
    

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form=form)


def salvar_imagem(img):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(img.filename)
    nome_arquivo = nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    
    tamanho = (200, 200)
    img_reduzida = Image.open(img)
    img_reduzida.thumbnail(tamanho)
    img_reduzida.save(caminho_completo)
    
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name and campo.data:
            lista_cursos.append(campo.label.text)
    if lista_cursos:
        return ';'.join(lista_cursos)



@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()

    if form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        if form_editar_perfil.foto_perfil.data:
            imgagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = imgagem
        
        current_user.cursos = atualizar_cursos(form_editar_perfil)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
         form_editar_perfil.email.data = current_user.email
         form_editar_perfil.username.data = current_user.username

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso', 'alert-warning')
        return redirect(url_for('home'))
    else:
        abort(403)
