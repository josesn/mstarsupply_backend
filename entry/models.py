from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from mstarsupply_backend.database import db

class Entry(db.Model):
    __tablename__ = "entry"

    id: Mapped[int] = mapped_column(primary_key=True)