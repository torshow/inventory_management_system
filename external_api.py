import requests


BASE_URL = "https://world.openfoodfacts.org"
 
 
def clean_product(product, barcode=""):
    
    return {
        "barcode": product.get("code", barcode),
        "name": product.get("product_name", "Unknown"),
        "brand": product.get("brands", ""),
        "ingredients": product.get("ingredients_text", ""),
    }



 
def get_by_barcode(barcode):

    response = requests.get(f"{BASE_URL}/api/v0/product/{barcode}.json", timeout=10)
    response.raise_for_status()   
    data = response.json()
 
    if data.get("status") != 1:   
        return None
    return clean_product(data["product"], barcode)


 
def search_by_name(name):

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }
    response = requests.get(f"{BASE_URL}/cgi/search.pl", params=params, timeout=10)
    response.raise_for_status()
 
    results = response.json().get("products", [])
    return [clean_product(item) for item in results]
 
 
 
 