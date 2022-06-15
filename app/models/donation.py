from sqlalchemy import Column, String, Integer, Text, ForeignKey

from app.core.db import Base
from app.models.base import GeneralInfo

class Donation(Base, GeneralInfo):

    user_id = Column(Integer, ForeignKey('user.id'))

    comment = Column(Text, nullable=False)