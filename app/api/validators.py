from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project_crud
from app.models import CharityProject
from app.schemas.project import ProjectUpdate


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    name_id = await project_crud.get_project_id_by_name(name, session)
    if name_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(obj_id=project_id, session=session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
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
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='При редактировании проекта его новое имя должно быть уникальным.')
        await check_name_duplicate(name=obj_in.name, session=session)

    if not project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!')
    if project.fully_invested:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Закрытый проект нельзя редактировать!')

    if obj_in.full_amount is not None:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Введённая сумма превышает инвестированную!')

    return project