from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, select
from app.core.db import Base
from app.models import CharityProject
from app.models import donation
from app.models.donation import Donation


async def invested_false1(
        project: CharityProject,
        session: AsyncSession
    ):

    #while project.fully_invested is False:
    db_donation = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False # noqa
        )
    )
    db_donation = db_donation.scalars().all()
    return db_donation

async def invested_false2(
        project: Donation,
        session: AsyncSession
    ):

    #while project.fully_invested is False:
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False # noqa
        )
    )
    db_project = db_project.scalars().all()
    return db_project

async def func_invest1(
    project: Base,

    #false_full: Base,
    session: AsyncSession
) -> None:

    not_true_full_invest = await invested_false1(project=project,
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
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    await session.commit()
    await session.refresh(project)


async def func_invest2(
    project: Base,

    #false_full: Base,
    session: AsyncSession
) -> None:

    not_true_full_invest = await invested_false2(project=project,
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
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    await session.commit()
    await session.refresh(project)



#async def func_invest(i, project, not_true_full_invest):

    #for i in not_true_full_invest:    
        #input_donation = project.full_amount - project.invested_amount
        #charity_project = i.full_amount - i.invested_amount
        #plus = min(input_donation, charity_project)
        #i.invested_amount += plus
        #project.invested_amount += plus
        #i.fully_invested = (i.full_amount == i.invested_amount)
        #if i.full_amount == i.invested_amount:
        #i.fully_invested = True
        #i.close_date = datetime.now()
    #if project.full_amount == project.invested_amount:
        #project.fully_invested = True
        #project.close_date = datetime.now()