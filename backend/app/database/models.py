from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    critical_stock = Column(Integer, nullable=False)


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    cargo_id = Column(Integer, unique=True, index=True)
    status = Column(String, nullable=False)
    estimated_delivery = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    cargo_id = Column(Integer, nullable=False)