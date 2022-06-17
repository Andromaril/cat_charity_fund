from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.financial_base import FinancialBase


class CharityProject(Base, FinancialBase):
    """Модель для проектов, наследуется от базовой. Содержит поля:
    id — первичный ключ;
    name — уникальное название проекта, обязательное строковое поле;
           допустимая длина строки — от 1 до 100 символов включительно;
    description — описание, обязательное поле, текст;
                  не менее одного символа;
    """

    name = Column(String(100), unique=True, nullable=False)

    description = Column(Text, nullable=False)
