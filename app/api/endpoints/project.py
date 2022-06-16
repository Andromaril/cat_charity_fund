from typing import List

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from app.api import validators
from app.core import db, user
from app.crud.donation import donation_crud
from app.crud.project import project_crud
from app.schemas.project import (ProjectBase, ProjectCreate, ProjectResponse,
                                 ProjectUpdate, ProjectResponseDelete)
from app.services import invest

router = APIRouter()


@router.get(
    path='/',
    response_model=List[ProjectResponse]
)
async def get_all_projects(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[ProjectResponse]:
    return await project_crud.get_multi(
        session=session
    )


@router.post(
    path='/',
    response_model=ProjectResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def create_charity_project(
    new_project: ProjectCreate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> ProjectResponse:

    await validators.check_name_duplicate(
        name=new_project.name,
        session=session
    )
    project = await project_crud.create(
        obj_in=new_project,
        session=session
    )
    await invest.distribution_of_amounts(
        undivided=project,
        crud_class=donation_crud,
        session=session
    )

    return project


@router.patch(
    path='/{project_id}',
    response_model=ProjectResponseDelete,
    response_model_exclude_none=False,
    dependencies=[Depends(user.current_superuser)]
)
async def update_charity_project(
    project_id: PositiveInt,
    obj_in: ProjectUpdate,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> ProjectResponseDelete:

    project= await validators.check_project_before_edit(
        project_id=project_id, session=session, obj_in=obj_in
    )

    project = await project_crud.update(
        db_obj=project, obj_in=obj_in, session=session
    )
    await invest.distribution_of_amounts(
        undivided=project,
        crud_class=donation_crud,
        session=session
    )
    return project


@router.delete(
    path='/{project_id}',
    response_model=ProjectResponseDelete,
    response_model_exclude_none=False,
    dependencies=[Depends(user.current_superuser)]
)
async def delete_charity_project(
    project_id: PositiveInt,
    session: db.AsyncSession = Depends(db.get_async_session)
) -> ProjectResponseDelete:

    project = await validators.check_project_exists(
        project_id=project_id,
        session=session
    )

    return await project_crud.remove(
        db_obj=project,
        session=session
    )