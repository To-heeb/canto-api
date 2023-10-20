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
    """_summary_

    Args:
        business (schemas.BusinessIn): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Returns:
        _type_: _description_
    """
    new_business = models.Business(
        **business.model_dump(exclude=["working_hours"]))

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    for working_day, working_hour in business.working_hours.items():
        new_working_hour = models.BusinessWorkingHours(
            business_id=new_business.id,
            weekday=working_day,
            opened_at=working_hour.opened_at,
            closed_at=working_hour.closed_at
        )
        db.add(new_working_hour)

    db.commit()
    return new_business


@router.get("/", status_code=status.HTTP_200_OK,  response_model=List[schemas.BusinessOut])
def get_businesses(db: Session = Depends(database.conn),
                   limit: int = 10,
                   offset: int = 0):
    """_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        limit (int, optional): _description_. Defaults to 10.
        offset (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    businesses = db.query(models.Business).order_by(models.Business.views.desc()).limit(
        limit).offset(offset).all()
    return businesses


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[schemas.BusinessOut])
def search_businesses(db: Session = Depends(database.conn),
                      limit: int = 10,
                      offset: int = 0,
                      keyword: Optional[str] = ""):
    """_summary_

    Args:
        db (Session, optional): _description_. Defaults to Depends(database.conn)
        limit (int, optional): _description_. Defaults to 10.
        offset (int, optional): _description_. Defaults to 0.
        keyword (Optional[str], optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    businesses = db.query(models.Business).join(models.BusinessItem, models.BusinessItem.business_id ==
                                                models.Business.id, isouter=True).filter(models.Business.name.icontains(
                                                    keyword) | models.Business.description.icontains(keyword) | models.BusinessItem.name.icontains(
                                                    keyword)).order_by(models.Business.views.desc()).limit(limit).offset(offset).all()
    # the all() is smart enough to filter objects of exactly the same value and return those of different values

    return businesses


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessOut)
def get_business(id: int, db: Session = Depends(database.conn)):
    """_summary_

    Args:
        id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn)

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    # test tomorrow
    businesses = db.query(models.Business).filter(
        models.Business.id == id).first()

    # businesses = db.query(models.Business, models.BusinessItem).join(models.BusinessItem, models.BusinessItem.business_id ==
    #                                                                  models.Business.id, isouter=True).filter(models.Business.id == id).all()

    business_working_hours = db.query(models.BusinessWorkingHours).filter(
        models.BusinessWorkingHours.business_id == id).all()

    # business_images = db.query(models.BusinessImage).filter(
    #     models.BusinessImage.business_id == id).all()

    # business_query = db.query(models.Business, models.BusinessItem, models.BusinessImage).join(models.BusinessItem,
    #                                                                                            models.BusinessItem.business_id == models.Business.id, isouter=True).join(models.BusinessImage, models.BusinessImage.business_id == models.Business.id, isouter=True).filter(models.Business.id == id)

    # raw_query = str(business_query)
    # breakpoint()
    if not businesses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business Type with id: {id} does not exist")

    db.query(models.Business).filter(models.Business.id == id).update(
        {"views": func.coalesce(models.Business.views, 0) + 1})

    db.commit()

    # business_response = schemas.BusinessOut(
    #     id=businesses[0].Business.id,
    #     name=businesses[0].Business.name,
    #     description=businesses[0].Business.description,
    #     location=businesses[0].Business.location,
    #     status=businesses[0].Business.status,
    #     business_type_id=businesses[0].Business.business_type_id,
    #     display_image=businesses[0].Business.display_image,
    #     created_at=businesses[0].Business.created_at,
    #     business_items=[],
    #     business_images=[],
    #     working_hours=[]
    # )

    # for business in businesses:
    #     if business.BusinessItem is not None:
    #         business_response.business_items.append(schemas.BusinessItemOut(
    #             id=business.BusinessItem.id,
    #             name=business.BusinessItem.name,
    #             status=business.BusinessItem.status,
    #             business_id=business.BusinessItem.business_id,
    #             created_at=business.BusinessItem.created_at
    #         ))

    # if business_images is not None:
    #     for business_image in business_images:
    #         business_response.business_images.append(schemas.BusinessImage(
    #             image_url=business_image.image_url,
    #             image_type=business_image.image_type,
    #             image_name=business_image.image_name
    #         ))

    for business_working_hour in business_working_hours:
        businesses.working_hours.append(schemas.BusinessWorkingDay(
            day=business_working_hour.weekday,
            opened_at=business_working_hour.opened_at,
            closed_at=business_working_hour.closed_at
        ))

    return businesses


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BusinessOut)
def update_business(id: int, updated_business: schemas.BusinessIn,
                    db: Session = Depends(database.conn),
                    current_user: int = Depends(oauth2.get_current_user)):
    """_summary_

    Args:
        id (int): _description_
        updated_business (schemas.BusinessIn): _description_
        db (Session, optional): _description_. Defaults to Depends(database.conn).
        current_user (int, optional): _description_. Defaults to Depends(oauth2.get_current_user).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business with id: {id} does not exist")

    business_query.update(updated_business.model_dump(exclude=["working_hours"]),
                          synchronize_session=False)

    db.commit()

    for working_day, working_hour in updated_business.working_hours.items():
        new_working_hour = models.BusinessWorkingHours(
            business_id=id,
            weekday=working_day,
            opened_at=working_hour.opened_at,
            closed_at=working_hour.closed_at
        )
        db.add(new_working_hour)
    db.commit()

    return business_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(id: int, db: Session = Depends(database.conn),
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
    business_query = db.query(models.Business).filter(models.Business.id == id)

    business = business_query.first()

    if business is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Business type with id: {id} does not exist")

    business_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
