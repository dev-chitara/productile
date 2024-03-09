from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class BaseProductSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity_available: int
    category_id: UUID
    brand_id: UUID


class CreateProductSchema(BaseProductSchema):
    pass


class UpdateProductSchema(BaseProductSchema):
    name: str | None=None
    description: str | None=None
    price: int | None
    quantity_available: int | None=None
    category_id: UUID 
    brand_id: UUID


class GetProductSchema(BaseProductSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


    class Config:
        from_attributes = True
    