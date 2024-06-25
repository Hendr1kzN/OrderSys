from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data_model import Product, Category, product_to_category_table
from sqlalchemy import func, distinct

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
    session = Session(return_engine())
    subquery = (
    session.query(Product.id)
    .join(product_to_category_table, Product.id == product_to_category_table.c.product_id)\
    .filter(product_to_category_table.c.category_id.in_(categorie_ids))
    .group_by(Product.id)
    .having(func.count(distinct(product_to_category_table.c.category_id)) == len(categorie_ids))
    ).subquery()
    
    query = (
    session.query(Category)
    .join(product_to_category_table, Category.id == product_to_category_table.c.category_id)
    .join(subquery, subquery.c.id == product_to_category_table.c.product_id)
    .distinct()
    .order_by(Category.name)
    )
    return query.all()

if __name__ == '__main__':
    products_with_given_categories = get_categorys_valid_with_current({1})
    for product in products_with_given_categories:
        print(product)

