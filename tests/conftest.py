import pytest
from app import app
from models import Cliente, Item, db
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm.exc import ObjectDeletedError


@pytest.fixture
def teardown():
    yield None
    with app.app_context():
        db.session.execute(text("DELETE FROM itens;"))
        db.session.execute(text("DELETE FROM clientes;"))
        db.session.commit()


@pytest.fixture
def cliente_data():
    return {
        "nome": "Foo Bar",
        "cpf": "12345678912",
        "data_nasc": "2023-02-07T21:34:53.256Z",
        "endereco": "Rua dos Pinheiros, 123, apto 101, Porto Alegre",
    }


@pytest.fixture
def obj_cliente(cliente_data):
    return Cliente(**cliente_data)


@pytest.fixture
def db_cliente(obj_cliente):
    with app.app_context():
        db.session.add(obj_cliente)
        db.session.commit()
        yield obj_cliente
        try:
            db.session.delete(obj_cliente)
            db.session.commit()
        except ObjectDeletedError as ex:
            pass


@pytest.fixture
def item_data():
    return {
        "nome": "Teste",
    }


@pytest.fixture
def obj_item(item_data, db_cliente):
    return Item(cliente_id=db_cliente.id, **item_data)


@pytest.fixture
def db_item(obj_item):
    with app.app_context():
        db.session.add(obj_item)
        db.session.commit()
        yield obj_item
        try:
            db.session.delete(obj_item)
            db.session.commit()
        except ObjectDeletedError as ex:
            pass
