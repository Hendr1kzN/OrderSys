#%% 
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select

Base = declarative_base()

product_to_category_table = Table(
    'product_to_category_table',
    Base.metadata,
    Column("product_id", ForeignKey('products_table.id')),
    Column("category_id", ForeignKey('categories_table.id'))
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
    prices : Mapped[list["SizeAndPrice"]] = relationship(back_populates="product")

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

    session.add(Product('Mineralwasser', [drink, low_carb],
                        []))
    session.add(Product('Cola Zero', [drink, low_carb], "gar kein Zucker"))
    session.add(Product('Schnitzel', [food]))
    empty_dish = Product('Leerer Teller')
    empty_dish.categories.append(food)
    empty_dish.categories.append(low_carb)
    session.add(SizeAndPrice('klein', 3.21, empty_dish))
    session.add(SizeAndPrice('gross', 8.32, empty_dish))
    empty_dish.prices.append(SizeAndPrice('riesig', 123.45))
    session.add(empty_dish)

    session.commit()

    session.expunge_all() # TODO what's the meaning of this?
    for product in session.query(Product):
        print(product)

# %%
