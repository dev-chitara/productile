import uuid
from fastapi import HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session
from models.products import Product
from schemas.products import ProductSchema
from db_setup import get_db


router = APIRouter(tags=["Product API"])


@router.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_products(product: ProductSchema, db:Session=Depends(get_db)):
    product_object = Product(**product.model_dump())
    db.add(product_object)
    db.commit()
    return product_object

@router.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: uuid.UUID, db:Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=404, detail="Product was not found!")
    return product_object


@router.patch("/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: uuid.UUID, product: ProductSchema, db: Session=Depends(get_db)):
    update_product_data = product.model_dump()
    update_product_data.pop("id")

    product_query = db.query(Product).filter(Product.id == product_id)
    product_object = product_query.first()
    product_query.update(update_product_data)
    db.commit()
    db.refresh(product_object)
    return product_object


@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: uuid.UUID, db:Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=404, detail="Product was not found!")
    db.delete(product_id)
    db.commit()
    return product_object

