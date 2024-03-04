import uuid
from sqlalchemy import Column, UUID, String, Text
from sqlalchemy.orm import Relationship
from db_setup import Base
from base import TimeStamp


class Category(TimeStamp):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, uniqe=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)

    products = Relationship("Product", backref="products")

    def __str__(self):
        return f"{self.name}"
