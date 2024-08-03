from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from data_model import Order, OrderedProduct, Product, Category, SizeAndPrice, product_to_category_table
from sqlalchemy import func, distinct

db_path = Path('ordermanagement.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session_from_maker = sessionmaker(engine)

def get_all_categorys():
    with Session(engine, expire_on_commit=False) as session:
        return session.query(Category)

def get_all_products():
    with Session_from_maker.begin() as session:
        products = session.query(Product).all()
        session.expunge_all()
        return products

def get_products_with_given_categories(categories: set):
    with Session_from_maker.begin() as session:
        products = session.query(Product).select_from(Product, Category)\
        .join(Product.categories)\
            .where(Category.id.in_([category.id for category in categories]))\
                .group_by(Product.id)\
                    .having(func.count(Product.id) == len(categories)).all()
        session.expunge_all()
        return products

def get_categorys_valid_with_current(categories: set):
    with Session(engine, expire_on_commit=False) as session:
        subquery = (
        session.query(Product.id)
        .join(product_to_category_table, Product.id == product_to_category_table.c.product_id)\
        .filter(product_to_category_table.c.category_id.in_([category.id for category in categories]))
        .group_by(Product.id)
        .having(func.count(distinct(product_to_category_table.c.category_id)) == len(categories))
        ).subquery()

        query = (
        session.query(Category)
        .join(product_to_category_table, Category.id == product_to_category_table.c.category_id)
        .join(subquery, subquery.c.id == product_to_category_table.c.product_id)
        .distinct()
        .order_by(Category.name)
        )
        return query.all()

def create_order(table_number, items) -> Order:
    if len(items) <= 0:
        return
    with Session_from_maker.begin() as session:
        order = Order(table_number)
        session.add(order)
        for item in items:
            order.ordered_products.append(OrderedProduct(item.size, order, item.addon_text))
        session.commit()
        return get_new_order()

def get_new_order():
    with Session_from_maker.begin() as session:
        order = session.query(Order).order_by(Order.id.desc()).first()
        session.expunge_all()
        return order

def create_product(name, info, price, categorie_names):
    with Session_from_maker.begin() as session:
        try:
            categories = session.query(Category).filter(Category.name.in_(categorie_names)).all()
            size = SizeAndPrice("Normal", price)
            session.add(size)
            new_product = Product(name, categories, info, [size])
            session.add(new_product)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

def add_categorie(name):
    with Session_from_maker.begin() as session:
        try:
            session.add(Category(name=name))
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
        
def get_product_of_size(size):
    with Session(engine, expire_on_commit=False) as session:
        product = session.query(Product).where(Product.prices.contains(size)).first()
        session.expunge_all()
        return product

if __name__ == '__main__':
    create_product("Natchos", "scharf", 8.99, ["Speisen"])

