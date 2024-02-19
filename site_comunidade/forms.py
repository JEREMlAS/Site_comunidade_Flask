from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site_comunidade.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_login = BooleanField('Lembrar Login')
    btn_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])

    curso_excel = BooleanField('Curso Excel')
    curso_vba = BooleanField('Curso VBA')
    curso_python = BooleanField('Curso Python ')
    curso_powerbi = BooleanField('Curso PowerBI')
    curso_sql = BooleanField('Curso SQL')

    btn_submit_atualizar_conta = SubmitField('Atualizar Conta')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = Usuario.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-mail já cadastrado em outra conta')
            
class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = StringField('Escreva seu post aqui', validators=[DataRequired()])
    btn_submit_post= SubmitField('Criar Post')
