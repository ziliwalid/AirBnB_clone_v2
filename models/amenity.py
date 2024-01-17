#!/usr/bin/python3
"""defines model amenity to map"""

from sqlalchemy import String
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column

class Amenity(BaseModel, Base):
    """amenity stuff model to map
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
		    "Place", secondary="place_amenity",
                                   viewonly=False)
