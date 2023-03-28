import sqlite3

DB_NAME = "ordermanagement.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        print("The Database connection could not be created")
    return conn

def set_reset_tabel_with_name_and_id(tabelname:str, attributes:str):
    connection_to_db = create_connection()
    curser = connection_to_db.cursor()
    curser.execute(f"DROP TABLE IF EXISTS {tabelname}")
    curser.execute(f"CREATE TABLE {tabelname}({attributes})")
    connection_to_db.commit()
    connection_to_db.close()
    
def set_reset_products():
    set_reset_tabel_with_name_and_id("products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT")
    
def set_reset_categories():
    set_reset_tabel_with_name_and_id("categories", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT")
    
def set_reset_product_to_categorie():
    set_reset_tabel_with_name_and_id("product_to_categorie", "product_id INTEGER, categorie_id INTEGER")

def set_reset_price_per_size():
    set_reset_tabel_with_name_and_id("price_per_size", "product_id INTEGER, size TEXT, prize REAL")


set_reset_products()
set_reset_categories()
set_reset_product_to_categorie()
set_reset_price_per_size()