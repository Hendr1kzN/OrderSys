from pathlib import Path
from typing import Set
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data_model import Product, Category
from sqlalchemy import func

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

def get_products_with_given_categories(categorie_ids: set):
    session = Session(return_engine())
    return session.query(Product).select_from(Product, Category)\
        .join(Product.categories)\
            .where(Category.id.in_(categorie_ids))\
                .group_by(Product.id)\
                    .having(func.count(Product.id) == len(categorie_ids))

if __name__ == '__main__':
    print(get_all_products())
    products_with_given_categories = get_products_with_given_categories([1, 2])
    for product in products_with_given_categories:
        print(product)

