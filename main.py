import uvicorn
from fastapi import FastAPI
from routers import products


app = FastAPI(
    title="Productile API",
    description="Productile swagger documentation.",
    version="0.0.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.include_router(products.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="warning",
        access_log=True,
        reload=True
    )