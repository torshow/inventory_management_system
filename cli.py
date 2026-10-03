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
 
 