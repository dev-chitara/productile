import uuid
from typing import List
from fastapi import HTTPException, Depends, status, APIRouter, Request
from sqlalchemy.orm import Session
from models.categories import Category
from schemas.categories import GetCategorySchema, CreateCategorySchema, UpdateCategorySchema
from db_setup import get_db


router = APIRouter(tags=["Category API"])


@router.get("/categories", status_code=status.HTTP_200_OK, response_model=List[GetCategorySchema]) 
async def fetch_categories(request:Request, db: Session=Depends(get_db)):
    name_query_params = request.query_params.get("name")

    if name_query_params:
        category_objects = db.query(Category).filter(Category.name.ilike(f'%{name_query_params}%'))
    else:
        category_objects = db.query(Category).all()
        
    return category_objects


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=GetCategorySchema)
async def create_categories(category_data: CreateCategorySchema, db: Session=Depends(get_db)):
    category_object = Category(**category_data.model_dump())
    db.add(category_object)
    db.commit()
    db.refresh(category_object)
    return category_object


@router.get("/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=GetCategorySchema)
async def get_category(category_id: uuid.UUID, db: Session=Depends(get_db)):
    category_object = db.query(Category).filter(Category.id == category_id).first()

    if category_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Category does not exist"})
    
    return category_object


@router.patch("/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=GetCategorySchema)
async def update_category(category_id: uuid.UUID, category_data: UpdateCategorySchema, db: Session=Depends(get_db)):
    update_category_data = category_data.model_dump()
    
    category_query = db.query(Category).filter(Category.id == category_id)
    category_object = category_query.first()

    if category_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Category does not exist"})

    category_query.update(update_category_data)
    db.commit()
    db.refresh(category_object)
    return category_object


@router.delete("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: uuid.UUID, db: Session=Depends(get_db)):
    category_object = db.query(Category).filter(Category.id == category_id).first()

    if category_object is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Category does not exist"})
    
    db.delete(category_object)
    db.commit()
    return {"Deleted":True}
