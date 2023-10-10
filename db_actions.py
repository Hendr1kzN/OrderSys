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

def get_products_with_categories(categories: list):
    print(select(Product).select_from(Category).join(Category in Product.categories))
    pass # TODO: learn how to create a query to not use for loops to find the right products

if __name__ == '__main__':
    get_products_with_categories(['Getraenke'])

