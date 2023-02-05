from flask_restx import Api, fields, Resource
from models import db, Cliente

from datetime import datetime
from email.utils import parsedate_to_datetime

api = Api()

ns = api.namespace("clientes", description="API CRUD Clientes")

cliente = api.model(
    "Cliente",
    {
        "id": fields.Integer(readonly=True, description="ID do cliente"),
        "nome": fields.String(required=True, description="Nome do cliente"),
        "cpf": fields.String(required=True, description="CPF do cliente"),
        "data_nasc": fields.DateTime(
            required=True, description="Data de nascimento do cliente"
        ),
        "endereco": fields.String(required=True, description="Endereço do cliente"),
    },
)


@ns.route("/")
class ClienteListResource(Resource):
    @ns.doc("list_clientes")
    @ns.marshal_list_with(cliente)
    def get(self):
        """Lista de clientes"""
        return db.session.query(Cliente).all()

    @ns.doc("create_cliente")
    @ns.expect(cliente)
    @ns.marshal_with(cliente, code=201)
    def post(self):
        """Cadastro de cliente"""
        print(api.payload)
        cliente = Cliente(**api.payload)
        cliente.data_nasc = parsedate_to_datetime(api.payload["data_nasc"])
        db.session.add(cliente)
        db.session.commit()
        return cliente, 201


@ns.route("/<int:id>")
class ClienteResource(Resource):
    @ns.doc("get_cliente")
    @ns.marshal_with(cliente)
    def get(self, id):
        """Busca cliente"""
        return db.get_or_404(Cliente, id)

    @ns.doc("delete_cliente")
    @ns.response(204, "Cliente excluído")
    def delete(self, id):
        """Exclui cliente"""
        cliente = db.get_or_404(Cliente, id)
        db.session.delete(cliente)
        db.session.commit()
        return "", 204

    @ns.expect(cliente)
    @ns.marshal_with(cliente)
    def put(self, id):
        """Atualiza cliente"""
        cliente = db.get_or_404(Cliente, id)
        cliente.nome = api.payload['nome']
        cliente.cpf = api.payload['cpf']
        cliente.data_nasc = parsedate_to_datetime(api.payload['data_nasc'])
        cliente.endereco = api.payload['endereco']
        
        return cliente
