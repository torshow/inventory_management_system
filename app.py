import requests
from flask import Flask, request, jsonify
 
from external_api import get_by_barcode, search_by_name
 
app = Flask(__name__)
 
 