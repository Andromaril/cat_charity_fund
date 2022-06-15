from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.crud.project import project_crud
from app.models.donation import Donation
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    name_id = await project_crud.get_project_id_by_name(name, session)
    if name_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )

async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=422,
            detail='В данный проект уже были сделаны инвестиции!'
        )

    return project 


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession, 
) -> CharityProject:
    project = await project_crud.get(
        # Для понятности кода можно передавать аргументы по ключу.
        obj_id=project_id, session=session 
    )
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    if project.fully_invested:
        raise HTTPException(status_code=404, detail='Закрыт!')

    return project