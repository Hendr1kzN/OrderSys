from pathlib import Path
from typing import Set
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, aliased
from data_model import Product, Category, product_to_category_table
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

def get_categorys_valid_with_current(categorie_ids: set):
    product2 = aliased(Product)
    category1 = aliased(Category)
    category2 = aliased(Category)
    session = Session(return_engine())
    product_to_category_table1 = aliased(product_to_category_table)
    product_to_category_table2 = aliased(product_to_category_table)
    
    return session.query(category2)\
        .join(product_to_category_table1, category2.id == product_to_category_table1.c.category_id)\
        .join(product2, product2.id == product_to_category_table1.c.product_id)\
        .join(product_to_category_table2, product2.id == product_to_category_table2.c.product_id)\
        .join(category1, category1.id == product_to_category_table2.c.category_id)\
        .filter(category1.id.in_(categorie_ids))\
        .distinct()\
        .order_by(category2.name)

if __name__ == '__main__':
    products_with_given_categories = get_categorys_valid_with_current({1})
    for product in products_with_given_categories:
        print(product)

