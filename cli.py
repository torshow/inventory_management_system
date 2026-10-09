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
        print("Error: the API request failed. ({e})")
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



def find_on_api(args):
    if args.barcode:
        params = {"barcode": args.barcode}
    elif args.name:
        params = {"name": args.name}
    else:
        print("Error: give --barcode or --name")
        return
 
    products = call_api("GET", "/external/search", params=params)
    if products is not None:
        if not products:
            print("No products found.")
        for p in products:
            print(f"{p['barcode']} | {p['name']} | {p['brand']}")
 
 
def build_parser():
    parser = argparse.ArgumentParser(description="Inventory CLI")
    sub = parser.add_subparsers(dest="command", required=True)
 
    p = sub.add_parser("list", help="List all items")
    p.set_defaults(func=list_items)
 
    p = sub.add_parser("view", help="View one item")
    p.add_argument("id", type=int)
    p.set_defaults(func=view_item)
 
    p = sub.add_parser("add", help="Add an item")
    p.add_argument("name")
    p.add_argument("--brand", default="")
    p.add_argument("--price", type=float, default=0)
    p.add_argument("--stock", type=int, default=0)
    p.set_defaults(func=add_item)
 
    p = sub.add_parser("update", help="Update price and/or stock")
    p.add_argument("id", type=int)
    p.add_argument("--price", type=float)
    p.add_argument("--stock", type=int)
    p.set_defaults(func=update_item)
 
    p = sub.add_parser("delete", help="Delete an item")
    p.add_argument("id", type=int)
    p.set_defaults(func=delete_item)
 
    p = sub.add_parser("find", help="Search OpenFoodFacts")
    p.add_argument("--barcode")
    p.add_argument("--name")
    p.set_defaults(func=find_on_api)
 
    return parser
 
 
if __name__ == "__main__":
    args = build_parser().parse_args()   
    args.func(args)
 
 
 

 