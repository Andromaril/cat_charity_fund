from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):

    full_amount: PositiveInt = Field(
        ...,
        example=200
    )
    comment: Optional[str]= Field(
        None,
        example='Помощь'
    )

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationMyResponse(DonationBase):

    id: PositiveInt = Field(
        ...,
        example=1
    )
    create_date: datetime = Field(
        ...,
        example='2019-08-24T14:15:22Z'
    )

    class Config:
        orm_mode = True


class DonationResponse(DonationMyResponse):

    user_id: int
    invested_amount: NonNegativeInt = Field(
        ...,
        example=200
    )
    fully_invested: bool = Field(
        ...,
        example=True
    )
    #close_date: Optional[datetime] = Field(
        #None,
        #example='2019-08-24T14:15:22Z'
    #)