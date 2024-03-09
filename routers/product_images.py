from uuid import UUID
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from models.product_images import ProductImage
from schemas.product_images import CreateProductImageSchema, GetProductImageSchema, UpdateProductImageSchema
from db_setup import get_db


router = APIRouter(tags=["ProductImage API"])


@router.get("/product_images", status_code=status.HTTP_200_OK, response_model=List[GetProductImageSchema])
async def fetch_product_images(db: Session=Depends(get_db)):
    product_image_objects = db.query(ProductImage).all()
    return product_image_objects


@router.post("/product_images", status_code=status.HTTP_201_CREATED, response_model=GetProductImageSchema)
async def create_product_images(product_image: CreateProductImageSchema, db: Session=Depends(get_db)):
    product_image_object = ProductImage(**product_image.model_dump())
    db.add(product_image_object)
    db.commit()
    db.refresh(product_image_object)
    return product_image_object


@router.get("/product_images/{product_image_id}", status_code=status.HTTP_200_OK, response_model=GetProductImageSchema)
async def get_product_image(product_image_id: UUID, db: Session=Depends(get_db)):
    product_image_object = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()

    if product_image_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product Image does not found"})
    
    return product_image_object


@router.patch("/product_images/{product_image_id}", status_code=status.HTTP_200_OK, response_model=GetProductImageSchema)
async def update_product_image(product_image_id: UUID, product_image: UpdateProductImageSchema, db: Session=Depends(get_db)):
    update_product_image_data = product_image.model_dump()

    product_image_query = db.query(ProductImage).filter(ProductImage.id == product_image_id)
    product_image_object = product_image_query.first()

    if product_image_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product Image does not found"})
    
    product_image_query.update(update_product_image_data)
    db.commit()
    db.refresh(product_image_object)
    return product_image_object


@router.delete("/product_images/{product_image_id}", status_code=status.HTTP_200_OK)
async def delete_product_image(product_image_id: UUID, db: Session=Depends(get_db)):
    product_image_object = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()

    if product_image_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product Image does not found"})
    
    db.delete(product_image_object)
    db.commit()
    return {"Deleted":True} 