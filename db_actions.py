from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data_model import Product, Category

def return_engine():
    db_path = Path('ordermanagement.db')
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    return engine

def get_all_categorys(engine):
    session = Session(engine)
    return session.query(Category)

def get_all_products(engine):
    session = Session(engine)
    return session.query(Product)

if __name__ == '__main__':
    engine = return_engine()
    for product in get_all_products(engine):
        print(product)
    
    for category in get_all_categorys(engine):
        print(category)

