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
 