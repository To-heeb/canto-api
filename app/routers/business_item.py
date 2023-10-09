from typing import List

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models, oauth2, database


router = APIRouter(
    prefix="/business",
    tags=['Business Item']
)


@router.post("/item/", status_code=status.HTTP_201_CREATED, response_model=schemas.BusinessItemOut)
def create_business_item(business_item: schemas.BusinessItemIn,
                         db: Session = Depends(database.conn),
                         current_user: int = Depends(oauth2.get_current_user)):

    new_business_item = models.BusinessItem(**business_item.model_dump())
    db.add(new_business_item)
    db.commit()
    db.refresh(new_business_item)

    return new_business_item


@router.get("/{business_id}/item/", status_code=status.HTTP_200_OK, response_model=List[schemas.BusinessItemOut])
def get_business_items(business_id: int, db: Session = Depends(database.conn),
                       current_user: int = Depends(oauth2.get_current_user)):
    business_items = db.query(models.BusinessItem).filter(
        models.BusinessItem.business_id == business_id, models.BusinessItem.status == 1).all()
    return business_items


@router.get("/item/", status_code=status.HTTP_200_OK, response_model=List[schemas.BusinessItemOut])
def get_all_items(db: Session = Depends(database.conn),
                  current_user: int = Depends(oauth2.get_current_user)):
    business_items = db.query(models.BusinessItem).all()
    return business_items


@router.get("/item/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessItemOut)
def get_business_item(id: int, db: Session = Depends(database.conn),
                      current_user: int = Depends(oauth2.get_current_user)):

    business_item = db.query(models.BusinessItem).filter(
        models.BusinessItem.id == id).first()
    if not business_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business item with id: {id} does not exist")

    return business_item


@router.put("/item/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessItemOut)
def update_business_item(id: int, updated_business_item: schemas.BusinessItemIn,
                         db: Session = Depends(database.conn),
                         current_user: int = Depends(oauth2.get_current_user)):

    business_item_query = db.query(models.BusinessItem).filter(
        models.BusinessItem.id == id)

    business_item = business_item_query.first()

    if business_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business item with id: {id} does not exist")

    business_item_query.update(
        updated_business_item.model_dump(), synchronize_session=False)

    db.commit()

    return business_item_query.first()


@router.delete("/item/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business_type(id: int, db: Session = Depends(database.conn),
                         current_user: int = Depends(oauth2.get_current_user)):

    business_item_query = db.query(models.BusinessItem).filter(
        models.BusinessItem.id == id)

    business_item = business_item_query.first()

    if business_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_item_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
