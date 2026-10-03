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
 