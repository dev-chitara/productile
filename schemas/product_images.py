import uuid
from pydantic import BaseModel
from datetime import datetime


class ProductImageSchema(BaseModel):
    id: uuid.UUID
    url: str
    product_id: uuid.UUID
    created_at: datetime
    updated_atr: datetime
    