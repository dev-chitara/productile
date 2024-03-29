import uvicorn
from fastapi import FastAPI
from routers import products
from routers import categories
from routers import brands
from routers import product_images


app = FastAPI(
    title="Productile API",
    description="Productile swagger documentation.",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.include_router(products.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(brands.router, prefix="/api")
app.include_router(product_images.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        access_log=True,
        reload=True
    )