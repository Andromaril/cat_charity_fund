from datetime import datetime
from typing import Union

from pydantic import (BaseModel, Extra, Field, NonNegativeInt, PositiveInt,
                      validator)


class ProjectBase(BaseModel):

    name: str = Field(
        ...,
        example='Проект',
        min_length=1,
        max_length=100
    )
    description: str = Field(
        None,
        example='На что собираем',
        min_length=1
    )
    full_amount: Union[None, PositiveInt] = Field(
        None,
        example=0
    )


    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value    
    
    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value   

    class Config:
        extra = Extra.forbid


class ProjectCreate(ProjectBase):
    
    pass

class ProjectUpdate(ProjectBase):

    pass


class ProjectResponse(ProjectCreate):

    id: int
    invested_amount: NonNegativeInt = Field(
        ...,
        example=1
    )
    fully_invested: bool = Field(
        ...,
        example=True
    )
    create_date: datetime = Field(
        ...,
        example='2019-08-24T14:15:22Z'
    )
    close_date: Union[None, datetime] = Field(
        None,
        example='2019-08-24T14:15:22Z'
    )

    class Config:
        orm_mode = True