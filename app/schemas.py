from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, PositiveInt
from enum import Enum, IntEnum


#  Admin Resource

class RoleEnum(str, Enum):
    reg = 'regular_admin'
    sup = 'super_admin'


class AdminBase(BaseModel):
    """AdminBase Model

    Args:
        BaseModel (_type_): _description_
    """
    first_name: str
    last_name: str
    email: EmailStr
    display_image: str = None
    role: Optional[str] = 'regular_admin'


class AdminIn(AdminBase):
    """_summary_

    Args:
        AdminBase (_type_): _description_
    """
    password: str

    class Config:
        from_attributes = True


class AdminOut(AdminBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# Business Resource

class BusinessWorkingDuration(BaseModel):
    opened_at: time
    closed_at: time


class BusinessWorkingDay(BaseModel):
    working_hours: dict[str, BusinessWorkingDuration]


class BusinessTypeBase(BaseModel):
    name: str
    description: str


class BusinessTypeIn(BusinessTypeBase):
    pass


class BusinessTypeOut(BusinessTypeBase):
    id: int

    class Config:
        from_attributes = True


class BusinessImage(BaseModel):
    image_url: str
    image_type: str
    image_name: str


class BusinessImageIds(BaseModel):
    business_id: int
    image_ids: List[int] = Field(
        examples=[1, 2, 3]
    )


class BusinessId(BaseModel):
    business_id: int


class BusinessBase(BaseModel):
    name: str
    description: str


class BusinessIn(BusinessBase):
    location: str
    business_type_id: int
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    working_hours: dict[int, BusinessWorkingDuration]
    opened_at: time
    closed_at: time

    class Config:
        from_attributes = True


class BusinessOut(BusinessBase):
    id: int
    location: str
    business_type_id: int
    display_image: str | None
    opened_at: time
    closed_at: time
    created_at: datetime
    business_images: list[BusinessImage] = []

    class Config:
        from_attributes = True


# Token models


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = "regular_admin"


admin = AdminIn.model_validate({"first_name": "toheeb", "last_name": "oyekola",
                                "password": "mypassword", "email": "oyekola@gmail.com", "role": "regular_admin"})
