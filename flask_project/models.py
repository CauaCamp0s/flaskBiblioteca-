from app import db
from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, String, Date
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
    disponivel = db.Column(db.Integer, default=1)
    url_da_capa = db.Column(db.String(255))

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
    __tablename__ = 'emprestimo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey('livro.id'), nullable=False)
    membro_id = Column(Integer, ForeignKey('membro.id'), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=False)

    livro = relationship("Livro")
    membro = relationship("Membro")

