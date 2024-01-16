from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from mstarsupply_backend.database import db

class ProductType(db.Model):
    __tablename__ = "product_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

class Product(db.Model):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    number_register: Mapped[int] = mapped_column(nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"), nullable=False)
    manufacturer: Mapped["Manufacturer"] = relationship()
    type_id: Mapped[int] = mapped_column(ForeignKey("product_type.id"), nullable=False)
    _type: Mapped["ProductType"] = relationship()
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(unique=False, default=True)



