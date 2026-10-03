import requests


BASE_URL = "https://world.openfoodfacts.org"
 
 
def clean_product(product, barcode=""):
    
    return {
        "barcode": product.get("code", barcode),
        "name": product.get("product_name", "Unknown"),
        "brand": product.get("brands", ""),
        "ingredients": product.get("ingredients_text", ""),
    }
 
 