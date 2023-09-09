from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import  schemas, models, oauth2, database


router = APIRouter(
    prefix="/business",
    tags=['Business']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_business(business: schemas.Business, db: Session = Depends(database.conn),
                    current_user: int = Depends(oauth2.get_current_user)):

    new_business = models.Business(**business.model_dump())
    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return {"data": new_business}


@router.get("/", status_code=status.HTTP_200_OK)
def get_businesses(db: Session = Depends(database.conn),
                   current_user: int = Depends(oauth2.get_current_user)):

    businesses = db.query(models.Business).all()
    return {"data": businesses}


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_business(id: int,db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    business = db.query(models.Business).filter(models.Business.id == id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business Type with id: {id} does not exist")
    
    return {"data": business}


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_business(id: int, updated_business: schemas.Business, db: Session = Depends(database.conn)):
    
    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business with id: {id} does not exist")
   
    business_query.update(updated_business.model_dump(), synchronize_session=False)

    db.commit()
    
    return business_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(id: int, db: Session = Depends(database.conn),
                       current_user: int = Depends(oauth2.get_current_user)):
    
    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
                           

#  