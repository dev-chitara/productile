from uuid import UUID
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter, Request
from sqlalchemy.orm import Session
from models.products import Product
from models.categories import Category
from models.brands import Brand
from schemas.products import GetProductSchema, CreateProductSchema, UpdateProductSchema
from db_setup import get_db


# http://www.myapp.com/products/1?category_name=Clothing&order=name


# http://www.myapp.com - Base URL

# http - Protocal
# www - Sub Domain
# myapp.com - Domain


# /products/1?category_name=Clothing&order=name - Complete Endpoint

# /products/1 - Endpoint
# /products - resource or collection name --> GET LIST, POST
# /1 - Path Params - Particular ID or Targeted Record --> GET SINGLE, PUT, PATCH, DELETE
# ?category_name=Clothing&order=name& - Query Params - Searching, Sorting, Filtering, Pagination, Column Selection --> GET LIST 


router = APIRouter(tags=["Product API"])


@router.get("/products", status_code=status.HTTP_200_OK, response_model=List[GetProductSchema])
async def fetch_products(request: Request, db: Session=Depends(get_db)):
    name_query_param = request.query_params.get("name")

    if name_query_param:
        product_objects = db.query(Product).filter(Product.name.ilike(f'%{name_query_param}%'))
    else:
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
async def get_product(product_id: UUID, db: Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    return product_object


@router.patch("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=GetProductSchema)
async def update_product(product_id: UUID, product: UpdateProductSchema, db: Session=Depends(get_db)):
    update_product_data = product.model_dump(exclude_none=True)

    product_query = db.query(Product).filter(Product.id == product_id)
    product_object = product_query.first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    product_query.update(update_product_data)
    db.commit()
    db.refresh(product_object)
    return product_object


@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: UUID, db: Session=Depends(get_db)):
    product_object = db.query(Product).filter(Product.id == product_id).first()

    if product_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Product was not found!"})
    
    db.delete(product_object)
    db.commit()
    return {"Deleted":True}
