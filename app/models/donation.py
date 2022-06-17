from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.financial_base import FinancialBase


class Donation(Base, FinancialBase):
    """Модель для инвестиций, наследуется от базовой. Содержит поля:
    id — первичный ключ;
    user_id — id пользователя, сделавшего пожертвование.
              Foreign Key на поле user.id из таблицы пользователей;
    comment — текстовое поле;
    """

    user_id = Column(Integer, ForeignKey('user.id'))

    comment = Column(Text, nullable=True)