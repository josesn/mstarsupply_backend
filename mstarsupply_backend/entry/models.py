import enum

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from sqlalchemy import event

from mstarsupply_backend.database import db

ENTRY_CHOICES = (
    ('Entrada', 'Entrada'),
    ('Saida', 'Saida'),
)

# def register_stock(product):
#     total_stock = 0
#     entry_in = db.session.query(db.func.sum(Entry.quantity)).filter(Entry._type == "Entrada").scalar()
#     entry_out = db.session.query(db.func.sum(Entry.quantity)).filter(Entry._type == "Saida").scalar()
    
#     if entry_in and entry_out:
#         total_stock = entry_in - entry_out

class Entry(db.Model):
    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    local: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship()
    _type: Mapped[str] = mapped_column(ChoiceType(ENTRY_CHOICES, impl=String(length=8)))


# @event.listens_for(Entry, 'after_insert')
# def receive_after_insert(mapper, connection, target):
#     register_stock(target.product_id)