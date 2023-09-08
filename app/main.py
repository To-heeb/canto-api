from fastapi import FastAPI

from . import models
from .routers import admin, business
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(business.router)

@app.get("/")
def root():
    return {"message": "Welcome to canto api once again"}