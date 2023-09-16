import os

from typing import Annotated
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile, Form

from sqlalchemy.orm import Session

from .. import models, oauth2, database, utils


router = APIRouter(
    prefix="/business/image",
    tags=['BusinessImage']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_business_images(files: Annotated[list[UploadFile],
                           File(description="Multiple files as UploadFile")],
                           business_id: Annotated[int, Form()],
                           db: Session = Depends(database.conn),
                           current_user: int = Depends(oauth2.get_current_user)):

    business_name = db.query(models.Business.name).filter(models.Business.id == business_id).first()[0]

    allowed_images_type = [".jpeg", ".jpg", ".png", ".gif", ".webp", ".svg"]

    for file in files:
        file_extension = os.path.splitext(file.filename)[1]

        if file_extension not in allowed_images_type:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail=f"Uploaded file type {file.filename} is not allowed")
       
        image_name = utils.image_name(business_name, file.filename)
        image_type = file.content_type
        image_url = utils.image_url(image_name)

        try:
            contents = file.file.read()
            with open(image_url, 'wb') as f:
                f.write(contents)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Upload of {file.filename} failed, please try again later"
                                ) from exc
        finally:
            file.file.close()

        image_upload = models.BusinessImage(
            image_name=image_name,
            image_type=image_type,
            business_id=business_id,
            image_url=image_url
            )
        db.add(image_upload)
        db.commit()
        db.refresh(image_upload)
    return {"message": "Successfully uploaded all files"}


@router.post("/display", status_code=status.HTTP_201_CREATED)
def create_business_display_images(file: UploadFile,
                                   business_id: Annotated[int, Form()],
                                   db: Session = Depends(database.conn),
                                   current_user: int = Depends(oauth2.get_current_user)):
    
    business_name = db.query(models.Business.name).filter(models.Business.id == business_id).first()[0]

    allowed_images_type = [".jpeg", ".jpg", ".png", ".gif", ".webp", ".svg"]

    file_extension = os.path.splitext(file.filename)[1]

    if file_extension not in allowed_images_type:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f"Uploaded file type {file.filename} is not allowed")
    #print(business_name[0])
    image_name = utils.image_name(business_name, file.filename, "display_image")
    image_type = file.content_type
    image_url = utils.image_url(image_name)
    try:
        contents = file.file.read()
        with open(image_url, 'wb') as f:
            f.write(contents)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Upload of {file.filename} failed, please try again later"
                            ) from exc
    finally:
        file.file.close()

    image_upload = models.BusinessImage(
        image_name=image_name,
        image_type=image_type,
        business_id=business_id,
        image_url=image_url
        )
    db.add(image_upload)
    db.commit()
    db.refresh(image_upload)

    return {"message": f"Successfully uploaded {file.filename}"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business_image(business_id: Annotated[int, Form()],
                          id: int, db: Session = Depends(database.conn)):

    business_image_query = db.query(models.BusinessImage).filter(
        models.BusinessImage.id == id,
        models.BusinessImage.business_id == business_id)

    business_image = business_image_query.first()

    if business_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image not found")

    try:
        os.remove(business_image.image_url)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image not found")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"An error occurred while deleting the file, please try again later"
                        ) from exc
    business_image_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)