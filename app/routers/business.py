from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from typing import List, Optional

from .. import  schemas, utils, models
from ..database import conn


router = APIRouter(
    prefix="/business",
    tags=['Business']
)



# @router.get("/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.BusinessResponse])
# def get_businesses(admin: schemas.Business, db: Session = Depends(conn)):

#     # hash the password - admin.password
#     hashed_password = utils.hash(admin.password)
#     admin.password = hashed_password

#     new_admin = models.Admin(**admin.model_dump())
#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     return {"data": new_admin}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BusinessResponse)
def create_business(admin: schemas.Admin, db: Session = Depends(conn)):

    # hash the password - admin.password
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password

    new_admin = models.Admin(**admin.model_dump())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"data": new_admin}


# @router.get("/{id}", status_code=status.HTTP_204_OK, response_model=schemas.BusinessResponse)
# def get_business(admin: schemas.Admin, db: Session = Depends(conn)):

#     # hash the password - user.password
#     hashed_password = utils.hash(admin.password)
#     admin.password = hashed_password

#     new_admin = models.Admin(**admin.model_dump())
#     db.add(new_admin)   
#     db.commit()
#     db.refresh(new_admin)

#     return {"data": new_admin}
 
# @router.post("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessResponse)
# def update_business(admin: schemas.Admin, db: Session = Depends(conn)):

#     # hash the password - user.password
#     hashed_password = utils.hash(admin.password)
#     admin.password = hashed_password

#     new_admin = models.Admin(**admin.model_dump())
#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     return {"data": new_admin}


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.BusinessResponse)
# def delete_business(admin: schemas.Admin, db: Session = Depends(conn)):

#     # hash the password - user.password
#     hashed_password = utils.hash(admin.password)
#     admin.password = hashed_password

#     new_admin = models.Admin(**admin.model_dump())
#     db.add(new_admin)
#     db.commit()
#     db.refresh(new_admin)

#     return {"data": new_admin}