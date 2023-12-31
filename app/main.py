from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import admin, business, business_type, business_image, business_item


# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canto API")

app.mount("/images", StaticFiles(directory="images"), name="images")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(business.router)
app.include_router(business_type.router)
app.include_router(business_image.router)
app.include_router(business_item.router)


@app.get("/")
def root():
    """Welcome mesage to my application

    Returns:
        string : Welcome message
    """
    return {
        "message": "Welcome to canto api, https://canto-api.onrender.com/docs"
    }
