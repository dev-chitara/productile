import uuid
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter, Request
from sqlalchemy.orm import Session
from models.brands import Brand
from schemas.brands import GetBrandSchema, CreateBrandSchema,UpdateBrandSchema
from db_setup import get_db


router = APIRouter(tags=["Brand API"])


@router.get("/brands", status_code=status.HTTP_200_OK, response_model=List[GetBrandSchema])
async def fetch_brands(request: Request, db: Session=Depends(get_db)):

    name_query_param = request.query_params.get("name")

    if name_query_param:
        brand_objects = db.query(Brand).filter(Brand.name.ilike(f'%{name_query_param}%'))
    else:
        brand_objects = db.query(Brand).all()

    return brand_objects
    

@router.post("/brands/", status_code=status.HTTP_201_CREATED, response_model=GetBrandSchema)
async def create_brands(brand_data: CreateBrandSchema, db: Session=Depends(get_db)):
    brand_object = Brand(**brand_data.model_dump())
    db.add(brand_object)
    db.commit()
    return brand_object


@router.get("/brands/{brand_id}", status_code=status.HTTP_200_OK, response_model=GetBrandSchema)
async def get_brand(brand_id: uuid.UUID, db: Session=Depends(get_db)):
    brand_object = db.query(Brand).filter(Brand.id == brand_id).first()

    if brand_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Brand does not exist"})
    
    return brand_object


@router.patch("/brands/{brand_id}", status_code=status.HTTP_200_OK, response_model=GetBrandSchema)
async def update_brand(brand_id: uuid.UUID, brand_data: UpdateBrandSchema, db: Session=Depends(get_db)):
    update_brand_data = brand_data.model_dump(exclude_none=True)

    brand_query = db.query(Brand).filter(Brand.id == brand_id)
    brand_object = brand_query.first()
    
    if brand_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Brand does not exist"})
    
    brand_query.update(update_brand_data)
    db.commit()
    db.refresh(brand_object)
    return brand_object


@router.delete("/brands/{brand_id}", status_code=status.HTTP_200_OK)
async def delete_brand(brand_id: uuid.UUID, db: Session=Depends(get_db)):
    brand_object = db.query(Brand).filter(Brand.id == brand_id).first()

    if brand_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Brand does not exist"})
    
    db.delete(brand_object)
    db.commit()
    return {"Deleted":True}

