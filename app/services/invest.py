from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


async def func_invest(
    project: Base,
    false_full: Base,
    session: AsyncSession
) -> None:

    not_true_full_invest = await false_full.invested_false(
        session=session
    )

    for i in not_true_full_invest:
        input_donation = project.full_amount - project.invested_amount
        charity_project = i.full_amount - i.invested_amount
        plus = min(input_donation, charity_project)
        i.invested_amount += plus
        project.invested_amount += plus
        i.fully_invested = (i.full_amount == i.invested_amount)
        if i.full_amount == i.invested_amount:
            i.fully_invested = True
            i.close_date = datetime.now()
        #close_obj(i)
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    #close_obj(project)
    await session.commit()
    await session.refresh(project)
    return project
