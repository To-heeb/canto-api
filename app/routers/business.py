from typing import Optional, List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import schemas, models, oauth2, database


router = APIRouter(
    prefix="/business",
    tags=['Business']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BusinessOut)
def create_business(business: schemas.BusinessIn, db: Session = Depends(database.conn),
                    current_user: int = Depends(oauth2.get_current_user)):

    new_business = models.Business(**business.model_dump())
    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business


@router.get("/", status_code=status.HTTP_200_OK,  response_model=List[schemas.BusinessOut])
def get_businesses(db: Session = Depends(database.conn),
                   current_user: int = Depends(oauth2.get_current_user),
                   limit: int = 10,
                   offset: int = 0):
    businesses = db.query(models.Business).order_by(models.Business.views.desc()).limit(
        limit).offset(offset).all()
    return businesses


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[schemas.BusinessOut])
def search_businesses(db: Session = Depends(database.conn),
                      current_user: int = Depends(oauth2.get_current_user),
                      limit: int = 10,
                      offset: int = 0,
                      keyword: Optional[str] = ""):

    businesses = db.query(models.Business).filter(models.Business.name.contains(
        keyword) | models.Business.description.contains(keyword)).order_by(models.Business.views.desc()).limit(limit).offset(offset).all()
    return businesses


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessOut)
def get_business(id: int, db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):

    business = db.query(models.Business).join(
        models.BusinessImage,
        models.BusinessImage.business_id == models.Business.id,
        isouter=True).filter(
        models.Business.id == id).first()

    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business Type with id: {id} does not exist")

    db.query(models.Business).filter(models.Business.id == id).update(
        {"views": func.coalesce(models.Business.views, 0) + 1})

    db.commit()

    return business


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessOut)
def update_business(id: int, updated_business: schemas.BusinessIn,
                    db: Session = Depends(database.conn),
                    current_user: int = Depends(oauth2.get_current_user)):

    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business with id: {id} does not exist")

    business_query.update(updated_business.model_dump(),
                          synchronize_session=False)

    db.commit()

    return business_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(id: int, db: Session = Depends(database.conn),
                    current_user: int = Depends(oauth2.get_current_user)):

    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
