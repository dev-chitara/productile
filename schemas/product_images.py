from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseProductImageSchema(BaseModel):
    url: str
    product_id: UUID


class CreateProductImageSchema(BaseProductImageSchema):
    pass


class UpdateProductImageSchema(BaseProductImageSchema):
    url: str | None=None
    product_id: UUID


class GetProductImageSchema(BaseProductImageSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None=None
    