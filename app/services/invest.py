from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import CharityProject, Donation


async def invested_false_donation(
        project: CharityProject,
        session: AsyncSession
):
    db_donation = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False # noqa
        )
    )
    db_donation = db_donation.scalars().all()
    return db_donation


async def invested_false_project(
        project: Donation,
        session: AsyncSession
):
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False # noqa
        )
    )
    db_project = db_project.scalars().all()
    return db_project


async def func_invest_project(
    project: Base,
    session: AsyncSession
) -> None:

    not_true_full_invest = await invested_false_donation(project=project, session=session)

    for i in not_true_full_invest:
        input_donation = project.full_amount - project.invested_amount
        charity_project = i.full_amount - i.invested_amount
        plus = min(input_donation, charity_project)
        i.invested_amount += plus
        project.invested_amount += plus
        if i.full_amount == i.invested_amount:
            i.fully_invested = True
            i.close_date = datetime.now()
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    await session.commit()
    await session.refresh(project)
    return project


async def func_invest_donation(
    project: Base,
    session: AsyncSession
) -> None:

    not_true_full_invest = await invested_false_project(project=project, session=session)

    for i in not_true_full_invest:
        input_donation = project.full_amount - project.invested_amount
        charity_project = i.full_amount - i.invested_amount
        plus = min(input_donation, charity_project)
        i.invested_amount += plus
        project.invested_amount += plus
        if i.full_amount == i.invested_amount:
            i.fully_invested = True
            i.close_date = datetime.now()
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    await session.commit()
    await session.refresh(project)
    return project