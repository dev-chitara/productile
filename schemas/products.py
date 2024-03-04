import uuid
from datetime import datetime
from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: int | float
    qnatity_available: int
    category_id: uuid.UUID
    brand_id: uuid.UUID
    created_at: datetime
    updated_at: datetime