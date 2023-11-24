from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from data_model import Product, Category

def return_engine():
    db_path = Path('ordermanagement.db')
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    return engine

def get_all_categorys():
    session = Session(return_engine())
    return session.query(Category)

def get_all_products():
    session = Session(return_engine())
    return session.query(Product)

def get_products_with_categories(categorie_ids: list):
    session = Session(return_engine())
    products = None
    for categorie_id in categorie_ids:
        current_category = session.execute(select(Category).where(Category.id == categorie_id)).first()# maybe it works in some kind of simular way
        print(current_category)
        if products == None:
            pass#products == set(current_category)
    pass # TODO: learn how to create a query to not use for loops to find the right products

if __name__ == '__main__':
    get_products_with_categories([1, 2])

