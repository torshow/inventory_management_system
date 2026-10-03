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


def find_item(item_id):

    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def next_id():
    
    return max([item["id"] for item in inventory], default=0) + 1
 
 
@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    
    return jsonify(inventory), 200
 
 
@app.route("/api/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
 
    return jsonify(item), 200
 
 
@app.route("/api/inventory", methods=["POST"])
def create_item():
    data = request.get_json(silent=True) or {}
 
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
 
    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number and stock a whole number"}), 400
 
    new_item = {
        "id": next_id(),
        "name": name,
        "brand": data.get("brand", ""),
        "barcode": data.get("barcode", ""),
        "ingredients": data.get("ingredients", ""),
        "price": price,
        "stock": stock,
    }
 
    inventory.append(new_item)
    return jsonify(new_item), 201
 
 
 