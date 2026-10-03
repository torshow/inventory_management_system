import requests
from flask import Flask, request, jsonify
 
from external_api import get_by_barcode, search_by_name
 
app = Flask(__name__)


inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0025293001015",
        "ingredients": "Filtered water, almonds, cane sugar",
        "price": 3.99,
        "stock": 25,
    },
    {
        "id": 2,
        "name": "Peanut Butter",
        "brand": "Jif",
        "barcode": "0051500255162",
        "ingredients": "Roasted peanuts, sugar, molasses",
        "price": 4.49,
        "stock": 40,
    },
    {
        "id": 3,
        "name": "Corn Flakes",
        "brand": "Kellogg's",
        "barcode": "0038000845116",
        "ingredients": "Milled corn, sugar, malt flavoring",
        "price": 5.29,
        "stock": 15,
    },
]
 