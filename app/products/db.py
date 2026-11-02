
from pathlib import Path
from tinydb import TinyDB

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

db = TinyDB(DATA_DIR / 'products.json')
products_table = db.table('products')
