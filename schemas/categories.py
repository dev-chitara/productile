from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseCategorySchema(BaseModel):
    name: str
    description: str


class CreateCategorySchema(BaseCategorySchema):
    pass


class UpdateCategorySchema(BaseCategorySchema):
    name: str | None = None
    description: str | None = None


class GetCategorySchema(BaseCategorySchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None=None


    class Config:
        from_attributes = True
