from datetime import datetime
from operator import and_
from typing import Optional

from sqlalchemy import and_, asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project


class CRUDProject(CRUDBase):

    async def get_project(
            self,
             *,
            close_data: datetime,
            session: AsyncSession,
    ) -> list[Project]:
        select_stmt = select(Project.close_data).order_by(asc('close_data'))
        project = await session.execute(select_stmt)
        project = project.scalars().all()
        return project 


    async def get_project_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_name_id = await session.execute(
            select(Project.id).where(
                Project.name == name
            )
        )
        db_name_id = db_name_id.scalars().first()
        return db_name_id


project_crud = CRUDProject(Project)