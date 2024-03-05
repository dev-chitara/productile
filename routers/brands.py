import uuid
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from models.brands import Brand
from schemas.brands import BrandSchema
from db_setup import get_db


router = APIRouter(tags=["Brand API"])


@router.post("/brands/", status_code=status.HTTP_201_CREATED)
async def create_brands(brand: BrandSchema, db: Session=Depends(get_db)):
    brand_object = Brand(**brand.model_dump(exclude={"id"}))
    db.add(brand_object)
    db.commit()
    return brand_object


@router.get("/brands/{brand_id}", status_code=status.HTTP_200_OK)
async def get_brand(brand_id: uuid.UUID, db: Session=Depends(get_db)):
    brand_object = db.query(Brand).filter(Brand.id == brand_id).first()

    if brand_object is None:
        raise HTTPException(status_code=404, detail="Brand does not exist")
    return brand_object


@router.patch("/brands/{brand_id}", status_code=status.HTTP_200_OK)
async def update_brand(brand_id: uuid.UUID, brand: BrandSchema, db: Session=Depends(get_db)):
    update_brand_data = brand.model_dump(exclude={"id"})

    brand_query = db.query(Brand).filter(Brand.id == brand_id)
    brand_object = brand_query.first()
    
    if brand_object is None:
        raise HTTPException(status_code=404, detail="Brand does not exist")
    brand_query.update(update_brand_data)
    db.commit()
    db.refresh(brand_object)
    return brand_object


@router.delete("/brands/{brand_id}", status_code=status.HTTP_200_OK)
async def delete_brand(brand_id: uuid.UUID, db: Session=Depends(get_db)):
    brand_object = db.query(Brand).filter(Brand.id == brand_id).first()

    if brand_object is None:
        raise HTTPException(status_code=404, detail="Brand does not exist")
    db.delete(brand_object)
    db.commit()
    return True