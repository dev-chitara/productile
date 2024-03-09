import uuid 
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from models.product_images import ProductImage
from schemas.product_images import ProductImageSchema
from db_setup import get_db


router = APIRouter(tags=["ProductImage API"])


@router.post("/product_images/", status_code=status.HTTP_201_CREATED)
async def create_product_images(product_image: ProductImageSchema, db: Session=Depends(get_db)):
    product_image_object = ProductImage(**product_image.model_dump(exclude={"id"}))
    db.add(product_image_object)
    db.commit()
    return product_image_object


@router.get("/product_images/{product_image_id}", status_code=status.HTTP_200_OK)
async def get_product_image(product_image_id: uuid.UUID, db: Session=Depends(get_db)):
    product_image_object = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()

    if product_image_object is None:
        raise HTTPException(status_code=404, detail="Product Image does not found")
    
    return product_image_object


@router.patch("/product_images/{product_image_id}", status_code=status.HTTP_200_OK)
async def update_product_image(product_image_id: uuid.UUID, product_image: ProductImageSchema, db: Session=Depends(get_db)):
    update_product_image_data = product_image.model_dump(exclude={"id"})

    product_image_query = db.query(ProductImage).filter(ProductImage.id == product_image_id)
    product_image_object = product_image_query.first()

    if product_image_object is None:
        raise HTTPException(status_code=404, detail="Product Image does not found")
    
    product_image_query.upadte(update_product_image_data)
    db.commit()
    db.refresh(product_image_object)
    return product_image_object


@router.delete("/product_images/{product_image_id}", status_code=status.HTTP_200_OK)
async def delete_product_image(product_image_id: uuid.UUID, db: Session=Depends(get_db)):
    product_image_object = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()

    if product_image_object is None:
        raise HTTPException(status_code=404, detail="Product Image does not found")
    
    db.delete(product_image_object)
    db.commit()
    return {"Deleted":True} 