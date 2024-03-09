import uuid
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from models.products import Product
from models.categories import Category
from models.brands import Brand
from schemas.products import GetProductSchema, CreateProductSchema, UpdateProductSchema
from db_setup import get_db


router = APIRouter(tags=["Product API"])


@router.get("/products", status_code=status.HTTP_200_OK, response_model=List[GetProductSchema])
async def fetch_products(db: Session=Depends(get_db)):
    product_objects = db.query(Product).all()
    return product_objects


@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=GetProductSchema)
async def create_products(product: CreateProductSchema, db: Session=Depends(get_db)):
    product_object = Product(**product.model_dump())
    db.add(product_object)
    db.commit()
    db.refresh(product_object)
    return product_object


@router.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=GetProductSchema)
async def get_product(product_id: uuid.UUID, db: Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    return product_object


@router.patch("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=GetProductSchema)
async def update_product(product_id: uuid.UUID, product: UpdateProductSchema, db: Session=Depends(get_db)):
    update_product_data = product.model_dump(exclude={"id"})

    product_query = db.query(Product).filter(Product.id == product_id)
    product_object = product_query.first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    product_query.update(update_product_data)
    db.commit()
    db.refresh(product_object)
    return product_object


@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: uuid.UUID, db: Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    db.delete(product_object)
    db.commit()
    return {"Deleted":True}


@router.get("products/{product_name}", status_code=status.HTTP_200_OK, response_model=List[GetProductSchema])
async def get_product_by_name(product_name: str, db: Session=Depends(get_db)):
    product_objects = db.query(Product).filter(Product.name == product_name).all()
    return product_objects 


@router.get("/products/{category_name}", status_code=status.HTTP_200_OK, response_model=List[GetProductSchema])
async def get_product_by_category_name(category_name: str, db: Session=Depends(get_db)):
    category_object = db.query(Category).filter(Category.name == category_name).first()
    category_associated_product_object = category_object.products
    return category_associated_product_object


@router.get("/products/{brand_name}", status_code=status.HTTP_200_OK, response_model=List[GetProductSchema])
async def get_product_by_brand_name(brand_name: str, db: Session=Depends(get_db)):
    brand_object = db.query(Brand).filter(Brand.name == brand_name).first()
    brand_associated_product_object = brand_object.products
    return brand_associated_product_object
