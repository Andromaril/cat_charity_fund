from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class ProjectBase(BaseModel):
    name: Optional[str] = Field(None, example='Проект', min_length=1, max_length=100)
    description: Optional[str] = Field(None, example='На что собираем', min_length=1)
    full_amount: Optional[PositiveInt] = Field(
        None,
        example=1)

    class Config:
        extra = Extra.forbid


class ProjectCreate(BaseModel):
    name: str = Field(..., example='Проект', min_length=1, max_length=100)
    description: str = Field(..., example='На что собираем', min_length=1)
    full_amount: PositiveInt = Field(
        ...,
        example=1
    )


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    invested_amount: Optional[NonNegativeInt] = Field(
        ...,
        example=1
    )
    fully_invested: Optional[bool] = Field(
        ...,
        example=True
    )
    create_date: Optional[datetime] = Field(
        ...,
        example='2019-08-24T14:15:22Z'
    )

    class Config:
        orm_mode = True


class ProjectResponseDelete(ProjectResponse):

    close_date: Optional[datetime] = Field(
        None,
        example='2019-08-24T14:15:22Z'
    )