from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, TIME

from .database import Base


class Admin(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    display_image = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Business(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False,  unique=True)
    location = Column(String, nullable=False)
    status = Column(Integer, nullable=False,
                    doc="0 for inactive, 1 for active")
    business_type_id = Column(Integer, ForeignKey(
        "business_types.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    views = Column(Integer, nullable=True, server_default="0")
    display_image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'),
                        server_onupdate=text('now()'))
    business_images = relationship("BusinessImage")


class BusinessType(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "business_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'),
                        server_onupdate=text('now()'))


class BusinessImage(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "business_images"

    id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    image_type = Column(String, nullable=False)
    business_id = Column(Integer, ForeignKey(
        "businesses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class BusinessItem(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "business_items"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(Integer, nullable=False,
                    doc="0 for inactive, 1 for active")
    business_id = Column(Integer, ForeignKey(
        "businesses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'),
                        server_onupdate=text('now()'))


class BusinessWorkingHours(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "business_working_hours"

    id = Column(Integer, primary_key=True, nullable=False)
    business_id = Column(Integer, ForeignKey(
        "businesses.id", ondelete="CASCADE"), nullable=False)
    weekday = Column(Integer, nullable=False)
    opened_at = Column(TIME, nullable=False)
    closed_at = Column(TIME, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'),
                        server_onupdate=text('now()'))
