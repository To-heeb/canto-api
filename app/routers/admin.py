from fastapi import status, HTTPException, Depends, APIRouter
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
def create_admin(admin: schemas.Admin, db: Session = Depends(database.conn)):
    # hash the password - user.password
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    admin.email =  admin.email.lower()
    print(admin)
    new_admin = models.Admin(**admin.model_dump())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"data": new_admin}


@router.get('/{id}', response_model=schemas.AdminResponse)
def get_admin(id: int, db: Session = Depends(database.conn),
              current_user: int = Depends(oauth2.get_current_user)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with id: {id} does not exist")
    return {"data": admin}
