import uuid
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from models.categories import Category
from schemas.categories import CategorySchema
from db_setup import get_db


router = APIRouter(tags=["Category API"])


@router.post("/categories/", status_code=status.HTTP_201_CREATED)
async def create_categories(category: CategorySchema, db: Session=Depends(get_db)):
    category_object = Category(**category.model_dump())
    db.add(category_object)
    db.commit()
    return category_object


@router.get("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(category_id: uuid.UUID, db: Session=Depends(get_db)):
    category_object = db.query(Category).filter(Category.id == category_id).first()

    if category_object is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    return category_object


@router.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: uuid.UUID, category: CategorySchema, db: Session=Depends(get_db)):
    update_category_data = category.model_dump(exclude={"id"})
    
    category_query = db.query(Category).filter(Category.id == category_id)
    category_object = category_query.first()

    if category_object is None:
        raise HTTPException(status_code=404, detail="Category does not exist")

    category_query.update(update_category_data)
    db.commit()
    db.refresh(category_object)
    return category_object


@router.delete("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: uuid.UUID, db: Session=Depends(get_db)):
    category_object = db.query(Category).filter(Category.id == category_id).first()

    if category_object is None:
        raise HTTPException(status_code=404, detail="Category does not exist")
    db.delete(category_object)
    db.commit()
    return True