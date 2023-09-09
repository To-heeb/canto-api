import os

from typing import Annotated
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile

from sqlalchemy.orm import Session

from .. import  schemas, models, oauth2, database


router = APIRouter(
    prefix="/business/image",
    tags=['BusinessImage']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_business_images(business: schemas.BusinessImage, files: Annotated[list[UploadFile], 
                                            File(description="Multiple files as UploadFile")],
                           db: Session = Depends(database.conn)):
    
     business_name = db.query(models.Business.name).filter(models.Business.id == id).first()
     
    # validate filetype 
    for file in files:
        print(file.content_type)

    #return {"data": new_business_type}


@router.post("/display", status_code=status.HTTP_201_CREATED)
def create_business_display_images(business: schemas.BusinessImage, files: Annotated[list[UploadFile], 
                                            File(description="Multiple files as UploadFile")],
                           db: Session = Depends(database.conn)):
    
    for file in files:
        print(file.filename)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business_image(id: int, db: Session = Depends(database.conn),
                        current_user: int = Depends(oauth2.get_current_user)):

    business_type_query = db.query(models.BusinessType).filter(models.BusinessType.id == id)

    business_type = business_type_query.first()

    if business_type == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_type_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)