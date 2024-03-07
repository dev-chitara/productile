import uuid
from sqlalchemy import Column, Integer, UUID, String, ForeignKey
from sqlalchemy.orm import Relationship
from db_setup import Base
from models.base import TimeStamp


class Product(TimeStamp):
    __tablename__ = "products" 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    category_id = Column(UUID, ForeignKey("categories.id", ondelete="CASCADE"))
    brand_id = Column(UUID, ForeignKey("brands.id", ondelete="CASCADE"))

    product_images = Relationship("ProductImage")
    brand = Relationship("Brand", backref="brands")
    category = Relationship("Category", backref="categories")

    def __str__(self):
        return f"{self.name} {self.price}"
    