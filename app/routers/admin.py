from typing import List

from fastapi import status, HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, utils, models, database, oauth2


router = APIRouter(
    prefix="/admins",
    tags=['Admin']
)


@router.post('/login', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(database.conn)):
    """_summary_

    Args:
        admin_credentials (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(database.conn).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    admin = db.query(models.Admin).filter(
        models.Admin.email == admin_credentials.username.lower()).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(
        data={"admin_id": admin.id, "admin_role": admin.role})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)
def create_admin(admin: schemas.AdminIn, db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):
    """_summary_

    Args:
        admin (schemas.AdminIn): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Returns:
        _type_: _description_
    """
    hashed_password = utils.hash_password(admin.password)
    admin.password = hashed_password
    admin.email = admin.email.lower()
    new_admin = models.Admin(**admin.model_dump())
    db.add(new_admin)
    db.commit()
    return new_admin


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.AdminOut])
def get_admins(db: Session = Depends(database.conn),
               current_user: int = Depends(oauth2.get_current_user)):
    """_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Returns:
        _type_: _description_
    """
    admins = db.query(models.Admin).all()
    return admins


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.AdminOut)
def get_admin(id: int, db: Session = Depends(database.conn),
              current_user: int = Depends(oauth2.get_current_user)):
    """_summary_

    Args:
        id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    new_admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not new_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id: {id} does not exist")
    return new_admin


@router.put("/{id}", response_model=schemas.AdminOut)
def update_admin(id: int, updated_admin: schemas.AdminIn, db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):
    """_summary_

    Args:
        id (int): _description_
        updated_admin (schemas.AdminIn): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    hashed_password = utils.hash_password(updated_admin.password)
    updated_admin.password = hashed_password
    updated_admin.email = updated_admin.email.lower()
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)

    admin = admin_query.first()
    print(current_user.role != "super_admin")
    print(admin.id != current_user.id)
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    if current_user.role != "super_admin" and admin.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    if admin.role == "regular_admin" and current_user.role != "super_admin":
        updated_admin.role = "regular_admin"

    admin_query.update(updated_admin.model_dump(), synchronize_session=False)

    db.commit()

    return admin_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session = Depends(database.conn),
                 current_user: int = Depends(oauth2.get_current_user)):
    """Delete admin account

    Args:
        id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)

    admin = admin_query.first()

    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with id: {id} does not exist")

    if admin.role != "super_admin" or admin.id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    admin_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
