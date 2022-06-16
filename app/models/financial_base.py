from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class FinancialBase:

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