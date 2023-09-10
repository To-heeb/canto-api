from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, TIME

from .database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False,  unique=True)
    location = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey(
        "business_types.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    opened_at = Column(TIME, nullable=False)
    closed_at = Column(TIME, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    # business_images = relationship("BusinessImage")


class BusinessType(Base):
    __tablename__ = "business_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class BusinessImage(Base):
    __tablename__ = "business_images"

    id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    image_type = Column(String, nullable=False)
    business_id = Column(Integer, ForeignKey(
        "businesses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
 