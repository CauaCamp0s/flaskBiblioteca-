from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, String, Date, DateTime
from sqlalchemy.orm import relationship

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)

class Livro(db.Model):
    __tablename__ = 'livro'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    ano_publicacao = db.Column(db.Integer)
    genero_id = db.Column(db.Integer, db.ForeignKey('genero.id'))
    disponivel = db.Column(db.Boolean, default=True)
    url_da_capa = db.Column(db.String(255))
    autor = db.relationship('Autor', backref=db.backref('livros', lazy=True))
    genero = db.relationship('Genero', backref=db.backref('livros', lazy=True))

class Genero(db.Model):
    __tablename__ = 'genero'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Genero {self.nome}>'
    
class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(15))

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    membro_id = db.Column(db.Integer, db.ForeignKey('membro.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    livro = db.relationship('Livro', backref=db.backref('emprestimos', lazy=True))
    membro = db.relationship('Membro', backref=db.backref('emprestimos', lazy=True))
