from typing import List

from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import  schemas, utils, models, database, oauth2


router = APIRouter(
    prefix="/admins",
    tags=['Admin']
)


@router.post('/login', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(database.conn)):
    "Admin login"
    admin = db.query(models.Admin).filter(
        models.Admin.email == admin_credentials.username.lower()).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(data={"admin_id": admin.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_admin(admin: schemas.Admin, db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    admin.email =  admin.email.lower()
    new_admin = models.Admin(**admin.model_dump())
    print(new_admin)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    # new_admin = schemas.AdminResponse(
    #                 id=new_admin.id,
    #                 first_name=new_admin.first_name,
    #                 last_name=new_admin.last_name,
    #                 email=new_admin.email,
    #                 role=new_admin.role
    #                 )
    return {"data": new_admin}


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.AdminResponse])
def get_admins(db: Session = Depends(database.conn),
              current_user: int = Depends(oauth2.get_current_user)):
    admins = db.query(models.Admin).all()

    return {"data": admins}


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.AdminResponse)
def get_admin(id: int, db: Session = Depends(database.conn),
              current_user: int = Depends(oauth2.get_current_user)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id: {id} does not exist")
    # admin = schemas.AdminResponse(admin)
    
    # admin = schemas.AdminResponse(
    #                 id=admin.id,
    #                 first_name=admin.first_name,
    #                 last_name=admin.last_name,
    #                 email=admin.email,
    #                 role=admin.role
    #                 )
    return {"data": admin}


@router.put("/{id}")
def update_admin(id: int, updated_admin: schemas.Admin, db: Session = Depends(database.conn),
                current_user: int = Depends(oauth2.get_current_user)):

    admin_query = db.query(models.Admin).filter(models.Admin.id == id)

    admin = admin_query.first()

    if admin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    if admin.role != "super_admin" or admin.id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # regualr_admin shouldn't update themselve to super_admin
    admin_query.update(updated_admin.model_dump(), synchronize_session=False)

    db.commit()

    return admin_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session = Depends(database.conn), 
                current_user: int = Depends(oauth2.get_current_user)):

    admin_query = db.query(models.Admin).filter(models.Admin.id == id)

    admin = admin_query.first()

    if admin == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    if admin.role != "super_admin" or admin.id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    admin_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)