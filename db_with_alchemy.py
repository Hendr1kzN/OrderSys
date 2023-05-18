import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from pathlib import Path


class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String)
    
    prices_and_sizes: Mapped[List["PriceAndSize"]] = relationship(back_populates="product")
    product_to_categorie: Mapped[List["ProductToCategorie"]] = relationship(back_populates="product")
    
    def __repr__(self):
        return f"Product(id = {self.id!r}, name = {self.name!r})"

class PriceAndSize(Base):
    __tablename__ = 'price_and_size'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id = mapped_column(ForeignKey("products.id"))
    size: Mapped[str] = mapped_column(db.String)
    price: Mapped[float] = mapped_column(db.REAL)
    
    product: Mapped[Product] = relationship(back_populates="prices_and_sizes")
    
    def __repr__(self):
        return f"PriceAndSize(id = {self.id!r}, product_id = {self.product_id!r}, size = {self.size!r}, price = {self.price!r})"

class Categorie(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String)
    
    product_to_categorie: Mapped[List["ProductToCategorie"]] = relationship(back_populates="categorie")
    
    def __repr__(self):
        return f"Categorie(id = {self.id!r}, name = {self.name!r})"
    
class ProductToCategorie(Base):
    __tablename__ = 'product_to_categorie'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id = mapped_column(ForeignKey("products.id"))
    categorie_id = mapped_column(ForeignKey("categories.id"))
    
    product: Mapped[Product] = relationship(back_populates="product_to_categorie")
    categorie: Mapped[Categorie] = relationship(back_populates="product_to_categorie")
    
    def __repr__(self):
        return f"Categorie(id = {self.id!r}, product_id = {self.product_id!r}, name = {self.categorie_id!r})"




if __name__ == '__main__':
    db_path = Path('ordermanagement.db')
    if db_path.exists():
        db_path.unlink()
    engine = db.create_engine(f'sqlite:///{db_path}', echo=False)
    with Session(engine) as session:
        Base.metadata.create_all(engine)
        pizza = Product(name="Pizza")
        food = Categorie(name="food")
        session.add(pizza)
        session.add(food)
        session.flush()
        session.commit()


