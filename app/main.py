from fastapi import FastAPI

from . import models
from .routers import admin, business, business_type, business_image
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(business.router)
app.include_router(business_type.router)
app.include_router(business_image.router)

@app.get("/")
def root():
    return {"message": "Welcome to canto api"}