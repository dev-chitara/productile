from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseBrandSchema(BaseModel):
    name: str
    description: str


class CreateBrandSchema(BaseBrandSchema):
    pass


class UpdateBrandSchema(BaseBrandSchema):
    name: str | None=None
    description: str | None=None


class GetBrandSchema(BaseBrandSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime | None=None