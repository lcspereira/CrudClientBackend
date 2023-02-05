import pytest
from app import app

client = app.test_client()


def test_cliente(cliente_data, teardown):
    response = client.post("/clientes/", json=cliente_data)

    assert response.status_code == 201
    data = response.json

    assert data["id"]
    assert data["nome"] == cliente_data["nome"]
    assert data["cpf"] == cliente_data["cpf"]
    #assert data["data_nasc"] == cliente_data["data_nasc"]
    assert data["endereco"] == cliente_data["endereco"]

    id_cliente = data["id"]
    upd_cliente_data = cliente_data
    upd_cliente_data["nome"] = "Bar Baz"
    upd_client_data = data["data_nasc"]
    response = client.put(f"/clientes/{id_cliente}", json=upd_cliente_data)


    assert response.status_code == 200

    response = client.delete(f"/clientes/{data['id']}")

    assert response.status_code == 204

