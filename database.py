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

def add_element_to_table(tabelname:str, table_attributes:str, *atributes_of_element):
    connection = create_connection()
    curser = connection.cursor()
    curser.execute(f"""INSERT INTO {tabelname}({table_attributes})
                   VALUES({", ".join(["?" for _ in atributes_of_element])})""", atributes_of_element)
    connection.commit()
    connection.close()


def set_reset_products():
    set_reset_tabel_with_name_and_id("products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT")
    
def set_reset_categories():
    set_reset_tabel_with_name_and_id("categories", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT")
    
def set_reset_product_to_categorie():
    set_reset_tabel_with_name_and_id("product_to_categorie", "product_id INTEGER, categorie_id INTEGER")

def set_reset_price_and_size():
    set_reset_tabel_with_name_and_id("price_per_size", "product_id INTEGER, size TEXT, price REAL")


def add_product(product_name:str):
    if not name_in_table(product_name):
        add_element_to_table("products", "name", product_name)

def add_categorie(castegorie_name:str):
    if not name_in_table(castegorie_name):
        add_element_to_table("categories", "name", castegorie_name)
    
def add_product_to_categorie(product_id:int, categorie_id:int):
    add_element_to_table("product_to_categorie", "product_id, categorie_id", product_id, categorie_id)

def add_price_and_size(product_id:int, size:str, price:float):
    add_element_to_table("price_per_size", "product_id, size , price", product_id, size, price)


def find_product_by_categories(*categorie_ids):
    connection = create_connection()
    curser = connection.cursor()
    curser.execute(f"""SELECT product_id
            FROM product_to_categorie
            WHERE categorie_id IN ({", ".join(["?" for _ in categorie_ids])})
            GROUP BY product_id
            HAVING COUNT(DISTINCT categorie_id) = {len(categorie_ids)};""", categorie_ids)
    result = curser.fetchall()
    connection.close()
    return result

def name_in_table(tablename, name):
    connection = create_connection()
    curser = connection.cursor()
    curser.execute(f"""SELECT id
            FROM {tablename}
            WHERE name = ?""", (name,))
    result = curser.fetchall()
    connection.close()
    return not (result == [])


print(name_in_table("products", "Tee"))