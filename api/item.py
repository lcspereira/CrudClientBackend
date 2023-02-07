from flask_restx import fields, Resource
from models import db, Item
from . import api
from datetime import datetime
from utils.message_queue import Publisher


ns = api.namespace("itens", description="API CRUD Itens")
publisher = Publisher("crud", "crud", "crud")

item = api.model(
    "Item",
    {
        "id": fields.Integer(readonly=True, description="ID do item"),
        "nome": fields.String(required=True, description="Nome do item"),
        "cliente_id": fields.Integer(required=True, description="ID do cliente"),
    },
)


@ns.route("/")
class ItemListResource(Resource):
    @ns.doc("list_item")
    @ns.marshal_list_with(item)
    def get(self):
        """Lista de items"""
        return db.session.query(Item).all()

    @ns.doc("create_item")
    @ns.expect(item)
    @ns.marshal_with(item, code=201)
    def post(self):
        """Cadastro de item"""
        item = Item(**api.payload)
        db.session.add(item)
        db.session.commit()
        publisher.publish(f"Item cadastrado: {item.id}")
        return item, 201


@ns.route("/cliente/<int:id>")
class ItemListByClienteResource(Resource):
    @ns.doc("list_item_by_cliente")
    @ns.marshal_list_with(item)
    def get(self, id):
        """Lista de items por cliente"""
        return [item for item in db.session.query(Item).filter(Item.cliente_id == id)]


@ns.route("/<int:id>")
class ItemResource(Resource):
    @ns.doc("get_item")
    @ns.marshal_with(item)
    def get(self, id):
        """Busca item"""
        return db.get_or_404(Item, id)

    @ns.doc("delete_item")
    @ns.response(204, "item excluído")
    def delete(self, id):
        """Exclui item"""
        item = db.get_or_404(Item, id)
        db.session.delete(item)
        db.session.commit()
        publisher.publish(f"Item excluído: {id}")
        return "", 204

    @ns.expect(item)
    @ns.marshal_with(item)
    def put(self, id):
        """Atualiza item"""
        item = db.get_or_404(Item, id)
        item.nome = api.payload["nome"]
        item.cliente_id = api.payload["cliente_id"]
        db.session.commit()
        publisher.publish(f"Item atualizado: {item.id}")
        return item
