import enum
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from mstarsupply_backend.database import db

ENTRY_CHOICES = (
    ('Entrada', 'Entrada'),
    ('Saida', 'Saida'),
)

class Entry(db.Model):
    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    local: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship()
    _type: Mapped[str] = mapped_column(ChoiceType(ENTRY_CHOICES, impl=String(length=8)))