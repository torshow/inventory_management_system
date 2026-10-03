# Inventory Management System - Flask Project

A Flask REST API and a command line interface (CLI) for managing store
inventory. It can search the OpenFoodFacts API for product details.

Data is stored in a Python list instead of a database, so it resets when the
app restarts.

## 1. Project structure

```text
inventory_management_system/
|-- app.py            Flask routes and the inventory list
|-- external_api.py   OpenFoodFacts functions
|-- cli.py            Command line interface
|-- requirements.txt
|-- README.md
`-- tests/
    |-- test_api.py
    |-- test_external_api.py
    `-- test_cli.py
```

## 2. Setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API runs at http://127.0.0.1:5000

## 3. API routes

| Purpose | Method | Route | Success code |
|---|---|---|---:|
| Read all items | GET | `/api/inventory` | 200 |
| Read one item | GET | `/api/inventory/<id>` | 200 |
| Create item | POST | `/api/inventory` | 201 |
| Update item | PATCH | `/api/inventory/<id>` | 200 |
| Delete item | DELETE | `/api/inventory/<id>` | 200 |
| Search OpenFoodFacts | GET | `/api/external/search?barcode=...` or `?name=...` | 200 |

Errors return JSON like `{"error": "Item not found"}` with status 400 (bad
input), 404 (not found) or 502 (external API unavailable).

Example item:

```json
{
  "id": 1,
  "name": "Organic Almond Milk",
  "brand": "Silk",
  "barcode": "0025293001015",
  "ingredients": "Filtered water, almonds, cane sugar",
  "price": 3.99,
  "stock": 25
}
```

## 4. CLI usage

Keep `python app.py` running in one terminal, then use a second terminal:

```bash
python cli.py list
python cli.py view 1
python cli.py add "Orange Juice" --brand Tropicana --price 3.5 --stock 10
python cli.py update 1 --price 4.25 --stock 30
python cli.py delete 2
python cli.py find --name "nutella"
python cli.py find --barcode 3017620422003
```

## 5. Big O

`find_item()` uses a linear search: it checks each item until the ID matches.
With n items the worst case is O(n).

## 6. Tests

```bash
python -m pytest -v
```

OpenFoodFacts calls are mocked with `unittest.mock`, so the tests run offline.