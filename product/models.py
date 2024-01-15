from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from mstarsupply_backend.database import db

class ProductType(db.Model):
    __tablename__ = "product_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

class Product(db.Model):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    number_register: Mapped[int]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))
    manufacturer: Mapped["Manufacturer"] = relationship()
    type_id: Mapped[int] = mapped_column(ForeignKey("product_type.id"))
    _type: Mapped["ProductType"] = relationship()
    description: Mapped[str] = mapped_column(String(200))


