from pathlib import Path
from sqlalchemy import create_engine, func
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.ext.hybrid import hybrid_property 
from datetime import datetime

Base = declarative_base()

product_to_category_table = Table(
    'product_to_category_table',
    Base.metadata,
    Column("product_id", ForeignKey('products_table.id'), primary_key=True),
    Column("category_id", ForeignKey('categories_table.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories_table'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False)

    products : Mapped[list["Product"]] = relationship(secondary=product_to_category_table, back_populates="categories")

    def __repr__(self):
        products_in_category = ", ".join([product.name for product in self.products])
        return f'Category({self.name}\n  -> {products_in_category})'

class Product(Base):
    __tablename__ = 'products_table'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False)
    info : Mapped[str] = mapped_column(nullable=True)
    categories : Mapped[list["Category"]] = relationship(secondary=product_to_category_table, back_populates="products")
    prices : Mapped[list["SizeAndPrice"]] = relationship(back_populates="product", cascade="all,delete")

    def __init__(self, name, categories=None, info=None, prices=None):
        self.name = name
        self.categories = categories or []
        self.prices = prices or []
        self.info = info or ""

    def __repr__(self):
        categories_repr = ', '.join((c.name for c in self.categories))
        price_repr = '|'.join((f'{s.size}: {s.price}' for s in self.prices))
        return f'Product({self.name}, {self.info}\n  -> {categories_repr}\n  -> {price_repr})'

class SizeAndPrice(Base):
    __tablename__ = 'size_and_price'
    id : Mapped[int] = mapped_column(primary_key=True)
    product_id : Mapped[int] = mapped_column(ForeignKey('products_table.id'))
    product : Mapped["Product"] = relationship(back_populates='prices')
    size : Mapped[str] = mapped_column()
    price : Mapped[float] = mapped_column()

    def __init__(self, size : str, price : float, product : Product = None):
        self.product = product
        self.size = size
        self.price = price
    
    def __repr__(self):
        product_repr = self.product.name if self.product else '(?)'
        return f'{product_repr}, {self.size}: {self.price}'

class OrderedProduct(Base):
    __tablename__ = "ordered_products"
    id : Mapped[int] = mapped_column(primary_key=True)
    size_and_price_id : Mapped[int] = mapped_column(ForeignKey('size_and_price.id')) 
    size_and_price : Mapped["SizeAndPrice"] = relationship()
    order_id : Mapped[int] = mapped_column(ForeignKey('orders.id'))
    order : Mapped["Order"] = relationship(back_populates="ordered_products")
    addon : Mapped[str] = mapped_column()

    def __init__(self, size_and_price, order, addon = ""):
        self.size_and_price = size_and_price
        self.order = order
        self.addon = addon

class Order(Base):
    __tablename__ = 'orders'
    id : Mapped[int] = mapped_column(primary_key=True)
    table_number : Mapped[int] = mapped_column()
    ordered_products : Mapped[list["OrderedProduct"]] = relationship(back_populates="order")
    done : Mapped[bool] = mapped_column()
    time_created : Mapped["datetime"] = mapped_column(server_default=func.current_timestamp())

    @hybrid_property
    def total(self):
        return sum([product.size_and_price.price for product in self.ordered_products])
    
    def __init__(self, table_number: int):
        self.table_number = table_number
        self.done = False
    
    def __repr__(self):
        products = "\n".join([f"{p.size_and_price.product.name}, {p.size_and_price.size} {p.size_and_price.price}" for p in self.ordered_products])
        string = f"Bestellung: Tisch: {self.table_number}\n {products} \n Gesammt: {self.total:.2f}"
        return string


if __name__ == "__main__":
    db_path = Path('ordermanagement.db')
    if db_path.exists():
        db_path.unlink()
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)

    session = Session(engine)

    drink = Category(name='Getraenke')
    food = Category(name='Speisen')
    low_carb = Category(name='Low-Carb')

    session.add(Product('Mineralwasser', [drink, low_carb], None, [SizeAndPrice('Normal', 2.50)]))
    session.add(Product('Cola Zero', [drink, low_carb], "gar kein Zucker", [SizeAndPrice('klein', 1.50), SizeAndPrice('gross', 3)]))
    session.add(Product('Schnitzel', [food], None, [SizeAndPrice("Normal", 15.50)]))
    empty_dish = Product('Leerer Teller')
    empty_dish.categories.append(food)
    empty_dish.categories.append(low_carb)
    small = SizeAndPrice('klein', 3.21, empty_dish)
    big = SizeAndPrice('gross', 8.32, empty_dish)
    empty_dish.prices.append(small)
    empty_dish.prices.append(big)
    empty_dish.prices.append(SizeAndPrice('riesig', 123.45))
    session.add(empty_dish)
    order = Order(12)
    session.add(OrderedProduct(small, order))
    session.add(OrderedProduct(big, order))
    session.add(order)
    session.commit()

    session.expunge_all()
    for product in session.query(Product):
        print(product)
    
    for order in session.query(Order):
        print(order)
    session.commit()