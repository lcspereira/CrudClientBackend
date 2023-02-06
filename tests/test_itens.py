import pytest
from app import app

client = app.test_client()


def test_item(db_cliente, item_data, teardown):
    create_item_data = item_data
    create_item_data["cliente_id"] = db_cliente.id
    response = client.post("/itens/", json=create_item_data)

    assert response.status_code == 201
    data = response.json

    assert data["id"]
    assert data["nome"] == create_item_data["nome"]
    assert data["cliente_id"] == create_item_data["cliente_id"]

    response = client.get(f"/itens/{data['id']}")
    assert response.status_code == 200
    data = response.json

    assert data["id"]
    assert data["nome"] == create_item_data["nome"]
    assert data["cliente_id"] == create_item_data["cliente_id"]

    id_item = data["id"]
    upd_item_data = create_item_data
    upd_item_data["nome"] = "Teste2"
    response = client.put(f"/itens/{id_item}", json=upd_item_data)
    assert response.status_code == 200

    response = client.get(f"/itens/{id_item}")
    assert response.status_code == 200

    data = response.json

    assert data["id"] == id_item
    assert data["nome"] == upd_item_data["nome"]
    assert data["cliente_id"] == upd_item_data["cliente_id"]

    response = client.get(f"/itens/cliente/{db_cliente.id}")
    assert response.status_code == 200
    print(response.json)
    assert len(response.json) == 1
    data = response.json[0]

    assert data["id"] == id_item
    assert data["nome"] == upd_item_data["nome"]
    assert data["cliente_id"] == upd_item_data["cliente_id"]

    response = client.delete(f"/itens/{id_item}")
    assert response.status_code == 204
