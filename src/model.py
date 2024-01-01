from sqlalchemy import Column, UUID, String, Float, ForeignKey

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column('category_id', UUID, primary_key=True)
    category_name = Column(String)


class Product(Base):
    __tablename__ = 'products'

    id = Column('product_id', UUID, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    category_id = Column(UUID, ForeignKey('categories.category_id'))
