from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project_crud
from app.models.charity_project import CharityProject
from app.schemas.project import ProjectUpdate


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    name_id = await project_crud.get_project_id_by_name(name, session)
    if name_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(obj_id=project_id, session=session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )

    return project


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession,
        obj_in: ProjectUpdate
) -> CharityProject:
    project = await project_crud.get(
        obj_id=project_id, session=session
    )
    if obj_in.name is not None:
        if obj_in.name == project.name:
            raise HTTPException(status_code=400, detail='При редактировании проекта его новое имя должно быть уникальным.')
        await check_name_duplicate(name=obj_in.name, session=session)

    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    if project.fully_invested is True:
        raise HTTPException(status_code=400, detail='Закрытый проект нельзя редактировать!')

    if obj_in.full_amount is not None:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(status_code=404, detail='Введённая сумма превышает инвестированную!')

    return project