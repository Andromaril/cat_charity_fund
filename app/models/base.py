from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean

class GeneralInfo:
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