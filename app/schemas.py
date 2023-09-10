from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from enum import Enum, IntEnum

# Model Request
class RoleEnum(str, Enum):
    reg = 'regular_admin'
    sup = 'super_admin'

class Admin(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: Optional[str] = 'regular_admin'

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


# Model response
class AdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name:str
    email: str
    role: str

    # class Config:
    #     from_attributes = True


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

    # class Config:
    #     from_attributes = True

class BusinessTypeResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

# Other models
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

admin = Admin.model_validate({"first_name": "toheeb", "last_name": "oyekola", "password": "mypassword","email": "oyekola@gmail.com", "role": "regular_admin"})
