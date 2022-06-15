from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.core.db import Base
from app.models.financialbase import FinancialBase


class Donation(Base, FinancialBase):

    user_id = Column(Integer, ForeignKey('user.id'))

    comment = Column(Text, nullable=False)