import uuid
from sqlalchemy import Column, Integer, UUID, String, Float, Text, ForeignKey
from db_setup import Base
from base import TimeStamp


class Product(TimeStamp):
    __tablename__ = "products" 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    category_id = Column(UUID, ForeignKey("categories", ondelete="CASCADE"))
    brand_id = Column(UUID, ForeignKey("brands",ondelete="CASCADE"))

    def __str__(self):
        return f"{self.name} {self.price}"
    