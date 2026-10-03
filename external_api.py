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
 
 
 