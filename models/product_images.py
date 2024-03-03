import uuid 
from sqlalchemy import Column, UUID, String, ForeignKey
from db_setup import Base
from base import TimeStamp


class ProductImage(TimeStamp):
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, uniqe=True)
    url = Column(String(80), nullable=False)
    product_id = Column(UUID, ForeignKey("products",ondelete="CASCADE"))

    def __str__(self):
        return f"{self.url}"