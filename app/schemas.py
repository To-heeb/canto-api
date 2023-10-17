from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError
from enum import Enum


#  Admin Resource

class RoleEnum(str, Enum):
    reg = 'regular_admin'
    sup = 'super_admin'


class Status(int, Enum):
    true = 1
    false = 0


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
    model_config = ConfigDict(from_attributes=True)
    password: str


class AdminOut(AdminBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    display_image: str | None
    created_at: datetime


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# Business Resource

class BusinessWorkingDuration(BaseModel):
    opened_at: time
    closed_at: time


class DayOfTheWeek(BaseModel):
    day: int

    @field_validator("day")
    @classmethod
    def validate_day(cls, value):
        if value < 1 or value > 7:
            raise ValueError("Day must be between 1 and 7")
        return value


class BusinessWorkingDay(BaseModel):
    day: int
    opened_at: time
    closed_at: time


class BusinessTypeBase(BaseModel):
    name: str
    description: str


class BusinessTypeIn(BusinessTypeBase):
    pass


class BusinessTypeOut(BusinessTypeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


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


class BusinessItemBase(BaseModel):
    name: str
    status: Status
    business_id: int


class BusinessItemIn(BusinessItemBase):
    pass


class BusinessItemsIn(BaseModel):
    items: list[BusinessItemBase]


class BusinessItemOut(BusinessItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class BusinessItemsOut(BaseModel):
    items: list[BusinessItemBase]


class BusinessBase(BaseModel):
    name: str
    description: str


class BusinessIn(BusinessBase):
    model_config = ConfigDict(from_attributes=True)
    location: str
    status: int
    business_type_id: int
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    working_hours: dict[int, BusinessWorkingDuration]

    @field_validator("working_hours")
    @classmethod
    def validate_working_hours(cls, value):
        if not all(1 <= key <= 7 for key in value.keys()):
            raise PydanticCustomError(
                "Keys in working_hours dictionary must be between 1 and 7")
        if len(value) > 7:
            raise ValueError(
                "The length of working_hours dictionary must not exceed 7")
        return value


class BusinessOut(BusinessBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    location: str
    status: int
    business_type_id: int
    display_image: str | None
    created_at: datetime
    business_images: list[BusinessImage] = []
    business_items: list[BusinessItemBase] = []
    working_hours: list[BusinessWorkingDay] = []


# Token models


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = "regular_admin"


admin = AdminIn.model_validate({"first_name": "toheeb", "last_name": "oyekola",
                                "password": "mypassword", "email": "oyekola@gmail.com", "role": "regular_admin"})
