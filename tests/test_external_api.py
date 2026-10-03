from unittest.mock import patch, Mock
import pytest
import requests
import external_api
 
 
@patch("external_api.requests.get")
def test_get_by_barcode_found(mock_get):
    mock_get.return_value = Mock(json=lambda: {
        "status": 1,
        "product": {"code": "123", "product_name": "Cola", "brands": "Co", "ingredients_text": "water"},
    })
    result = external_api.get_by_barcode("123")
    assert result["name"] == "Cola"
    assert result["brand"] == "Co"
    assert result["ingredients"] == "water"
 
 
@patch("external_api.requests.get")
def test_get_by_barcode_not_found(mock_get):
    mock_get.return_value = Mock(json=lambda: {"status": 0})
    assert external_api.get_by_barcode("000") is None

@patch("external_api.requests.get", side_effect=requests.ConnectionError)
def test_get_by_barcode_website_down(mock_get):
    with pytest.raises(requests.RequestException):
        external_api.get_by_barcode("123")
 
 
@patch("external_api.requests.get")
def test_search_by_name(mock_get):
    mock_get.return_value = Mock(json=lambda: {"products": [
        {"code": "1", "product_name": "A"},
        {"code": "2", "product_name": "B"},
    ]})
    results = external_api.search_by_name("x")
    assert len(results) == 2
    assert results[0]["name"] == "A"

def test_clean_product_uses_barcode_when_code_missing():
    result = external_api.clean_product({}, "999")
    assert result == {"barcode": "999", "name": "Unknown", "brand": "", "ingredients": ""}
 
 
 