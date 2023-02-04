import pytest
from app import app
from models import Cliente, Item, db
from datetime import datetime
from sqlalchemy import text


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
        "data_nasc": datetime.now(),
        "endereco": "Rua dos Pinheiros, 123, apto 101, Porto Alegre",
    }


@pytest.fixture
def obj_cliente(cliente_data):
    return Cliente(**cliente_data)


@pytest.fixture
def db_cliente(obj_cliente):
    cliente = db.session.add(obj_cliente)
    db.commit()
    db.refresh()
    yield cliente
    db.session.delete(cliente)
    db.session.commit()


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
    item = db.session.add(obj_item)
    db.session.commit()
    yield item
    db.session.delete(item)
    db.session.commit()
