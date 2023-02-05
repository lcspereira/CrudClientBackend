from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    cpf = db.Column(db.String(11))
    data_nasc = db.Column(db.DateTime())
    endereco = db.Column(db.String(1024))
    itens = db.relationship("Item", back_populates="cliente")


class Item(db.Model):
    __tablename__ = "itens"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    cliente = db.relationship("Cliente", back_populates="itens")
