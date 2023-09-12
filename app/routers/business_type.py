from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import  schemas, models, oauth2, database


router = APIRouter(
    prefix="/business/type",
    tags=['BusinessType']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_business_type(business_type: schemas.BusinessType,
                        db: Session = Depends(database.conn),
                        current_user: int = Depends(oauth2.get_current_user)):
    print(business_type)
    new_business_type = models.BusinessType(**business_type.model_dump())
    db.add(new_business_type)
    db.commit()
    db.refresh(new_business_type)

    return {"data": new_business_type}


@router.get("/", status_code=status.HTTP_200_OK)
def get_business_types(db: Session = Depends(database.conn),
                  current_user: int = Depends(oauth2.get_current_user)):
    print("get_business_types")
    business_types = db.query(models.BusinessType).all()
    return {"data": business_types}


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_business_type(id: int, db: Session = Depends(database.conn),
                  current_user: int = Depends(oauth2.get_current_user)):

    business_type = db.query(models.BusinessType).filter(models.BusinessType.id == id).first()
    if not business_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business Type with id: {id} does not exist")
 
    business_type = schemas.BusinessTypeResponse(
                id=business_type.id,
                name=business_type.name,
                description=business_type.description,
                created_at=business_type.created_at
                )
    return {"data": business_type}


@router.put("/{id}")
def update_business_type(id: int, updated_business_type: schemas.BusinessType,
                         db: Session = Depends(database.conn),
                        current_user: int = Depends(oauth2.get_current_user)):

    business_type_query = db.query(models.BusinessType).filter(models.BusinessType.id == id)

    business_type = business_type_query.first()

    if business_type == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_type_query.update(updated_business_type.model_dump(), synchronize_session=False)

    db.commit()

    return business_type_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business_type(id: int, db: Session = Depends(database.conn),
                        current_user: int = Depends(oauth2.get_current_user)):

    business_type_query = db.query(models.BusinessType).filter(models.BusinessType.id == id)

    business_type = business_type_query.first()

    if business_type == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_type_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)