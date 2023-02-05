import pytest
from app import app

client = app.test_client()


def test_item(db_cliente, item_data, teardown):

    create_item_data = item_data
    create_item_data['cliente_id'] = db_cliente.id
    response = client.post("/itens/", json=item_data)

    assert response.status_code == 201
    data = response.json

    assert data["id"]
    assert data["nome"] == cliente_data["nome"]
    assert data["cliente_id"] = create_item_data["id"]

    id_item = data["id"]
    upd_item_data = create_item_data
    upd_item_data["nome"] = "Teste2"
    response = cliente.put(f"/itens/{id_cliente}", json=upd_cliente_data)


    assert response.status_code == 200
    data = response.json

    assert data["id"] = upd_item_data['id']
    assert data["nome"] == upd_item_data["nome"]
    assert data["cliente_id"] == upd_item_data["cliente_id"]

    response = client.delete(f"/itens/{data['id']}")

    assert response.status_code == 204

