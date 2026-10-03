import copy
from unittest.mock import patch
import pytest
import requests
import app as app_module


@pytest.fixture
def client():
    """Test client. Restores the inventory list after each test."""
    backup = copy.deepcopy(app_module.inventory)
    app_module.app.config["TESTING"] = True
    yield app_module.app.test_client()
    app_module.inventory[:] = backup
 
 
FAKE_PRODUCT = {"barcode": "123", "name": "Fake Cola", "brand": "FakeCo", "ingredients": "water"}
 
 
 