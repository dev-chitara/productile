from db_setup import engine, Base
from models import products, categories, brands, product_images, base

Base.metadata.create_all(bind=engine)