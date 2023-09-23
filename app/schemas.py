from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from enum import Enum, IntEnum


#  Admin Resource

class RoleEnum(str, Enum):
    reg = 'regular_admin'
    sup = 'super_admin'


class AdminBase(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    first_name: str
    last_name: str
    email: EmailStr
    role: Optional[str] = 'regular_admin'


class AdminIn(AdminBase):
    """_summary_

    Args:
        AdminBase (_type_): _description_
    """
    password: str


class AdminOut(AdminBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# Business Resource

class Business(BaseModel):
    name: str
    location: str
    type_id: int
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    opened_at: time
    closed_at: time


class BusinessType(BaseModel):
    name: str
    description: str


class BusinessImage(BaseModel):
    business_id: int


class BusinessResponse(BaseModel):
    id: int
    name: str
    location: str
    type_id: int
    description: str
    opened_at: time
    closed_at: time
    created_at: datetime
    images: BusinessImage

    class Config:
        from_attributes = True


class BusinessTypeResponse(BaseModel):
    id: int
    name: str
    description: str

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
