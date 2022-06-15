from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import Base


def close_obj(obj: Base) -> None:
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.now()


async def distribution_of_amounts(
    undivided: Base,
    crud_class: Base,
    session: AsyncSession
) -> None:

    receptions = await crud_class.invested_false(
        session=session
    )
    for reception in receptions:
        needed = undivided.full_amount - undivided.invested_amount
        available = reception.full_amount - reception.invested_amount
        to_add = min(needed, available)
        reception.invested_amount += to_add
        undivided.invested_amount += available
        close_obj(reception)

    close_obj(undivided)

    await session.commit()
    await session.refresh(undivided)
    return undivided