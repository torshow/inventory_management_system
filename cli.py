import argparse
import requests


API_URL = "http://127.0.0.1:5000/api"

def call_api(method, path, **kwargs):
    
    try:
        response = requests.request(method, API_URL + path, timeout=10, **kwargs)
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: cannot connect to the API. Is app.py running?")
        return None
    except (requests.exceptions.RequestException, ValueError):
        print("Error: the API request failed.")
        return None
 
    if not response.ok:
        print("Error:", data.get("error", "Something went wrong"))
        return None
    return data

 
def show_item(item):
    print(f"[{item['id']}] {item['name']} ({item['brand']}) "
          f"- ${item['price']:.2f} - stock: {item['stock']}")
 
 

def list_items(args):
    items = call_api("GET", "/inventory")
    if items is not None:
        for item in items:
            show_item(item)


def view_item(args):
    item = call_api("GET", f"/inventory/{args.id}")
    if item:
        for key, value in item.items():
            print(f"{key}: {value}")
 
 
def add_item(args):
    body = {"name": args.name, "brand": args.brand,
            "price": args.price, "stock": args.stock}
    item = call_api("POST", "/inventory", json=body)
    if item:
        print("Added:")
        show_item(item)


def update_item(args):
    body = {}
    if args.price is not None:
        body["price"] = args.price
    if args.stock is not None:
        body["stock"] = args.stock
    if not body:
        print("Error: give --price and/or --stock")
        return
 
    item = call_api("PATCH", f"/inventory/{args.id}", json=body)
    if item:
        print("Updated:")
        show_item(item)
 
 
def delete_item(args):
    result = call_api("DELETE", f"/inventory/{args.id}")
    if result:
        print(result["message"])
 
 

 