import copy
from unittest.mock import patch
import pytest
import requests
import app as app_module


@pytest.fixture
def client():

    backup = copy.deepcopy(app_module.inventory)
    app_module.app.config["TESTING"] = True
    yield app_module.app.test_client()
    app_module.inventory[:] = backup
 
 
FAKE_PRODUCT = {"barcode": "123", "name": "Fake Cola", "brand": "FakeCo", "ingredients": "water"}


def test_get_all(client):
    response = client.get("/api/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 3
 
 
def test_get_one(client):
    response = client.get("/api/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"
 
 
def test_get_one_not_found(client):
    assert client.get("/api/inventory/999").status_code == 404

    def test_create_item(client):
    response = client.post("/api/inventory", json={"name": "Tea", "price": 2.5, "stock": 8})
    assert response.status_code == 201
    assert response.get_json()["id"] == 4
    assert len(client.get("/api/inventory").get_json()) == 4
 
 
def test_create_item_missing_name(client):
    assert client.post("/api/inventory", json={"price": 1}).status_code == 400
 
 
def test_create_item_bad_price(client):
    assert client.post("/api/inventory", json={"name": "X", "price": "abc"}).status_code == 400

def test_update_item(client):
    response = client.patch("/api/inventory/1", json={"price": 9.99, "stock": 5})
    data = response.get_json()
    assert response.status_code == 200
    assert data["price"] == 9.99
    assert data["stock"] == 5
 
 
def test_update_bad_value(client):
    assert client.patch("/api/inventory/1", json={"stock": "many"}).status_code == 400
 
 
def test_update_not_found(client):
    assert client.patch("/api/inventory/999", json={"price": 1}).status_code == 404


def test_delete_item(client):
    assert client.delete("/api/inventory/1").status_code == 200
    assert client.get("/api/inventory/1").status_code == 404
 
 
def test_delete_not_found(client):
    assert client.delete("/api/inventory/999").status_code == 404


@patch("app.get_by_barcode", return_value=FAKE_PRODUCT)
def test_search_by_barcode(mock_fetch, client):
    response = client.get("/api/external/search?barcode=123")
    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "Fake Cola"
 
 
@patch("app.search_by_name", return_value=[FAKE_PRODUCT])
def test_search_by_name(mock_search, client):
    response = client.get("/api/external/search?name=cola")
    assert response.status_code == 200
    assert len(response.get_json()) == 1
 
 
@patch("app.get_by_barcode", return_value=None)
def test_search_not_found(mock_fetch, client):
    assert client.get("/api/external/search?barcode=000").status_code == 404
 
 
def test_search_no_params(client):
    assert client.get("/api/external/search").status_code == 400
 
 
@patch("app.get_by_barcode", side_effect=requests.RequestException)
def test_search_api_down(mock_fetch, client):
    assert client.get("/api/external/search?barcode=123").status_code == 502
 
 

 
 
 
 
 
 
 