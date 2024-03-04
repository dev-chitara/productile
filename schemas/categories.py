import uuid
from pydantic import BaseModel
from datetime import datetime


class CategorySchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
