from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Optional
from models import Autor, Genero

class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor_id = SelectField('Autor', coerce=int, validators=[DataRequired()])
    ano_publicacao = IntegerField('Ano de Publicação')
    genero_id = SelectField('Gênero', coerce=int)
    disponivel = BooleanField('Disponível', default=True)
    foto = FileField('Foto do Livro')

class EmprestimoForm(FlaskForm):
    livro_id = SelectField('Livro', coerce=int, validators=[DataRequired()])
    membro_id = SelectField('Membro', coerce=int, validators=[DataRequired()])
    data_emprestimo = DateField('Data de Empréstimo', validators=[DataRequired()])
    data_devolucao = DateField('Data de Devolução', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class MembroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    submit = SubmitField('Salvar')
