from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class FinancialBase:
    """Модель базовая, содержит общие поля остальных моделей. Содержит поля:
    full_amount — требуемая сумма, целочисленное поле; больше 0;
    invested_amount — внесённая сумма, целочисленное поле;
                      значение по умолчанию — 0;
    fully_invested — булево значение, указывающее на то,
                     собрана ли нужная сумма для проекта (закрыт ли проект);
                     значение по умолчанию — False;
    create_date — дата создания проекта, тип DateTime,
                  должно добавляться автоматически в момент создания проекта.
    close_date — дата закрытия проекта, DateTime,
                 проставляется автоматически в момент набора нужной суммы.
    """

    __abstract__ = True

    full_amount = Column(
        Integer,
        nullable=False
    )
    invested_amount = Column(
        Integer,
        nullable=False,
        default=0
    )
    fully_invested = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )
    create_date = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )
    close_date = Column(
        DateTime,
        nullable=True
    )