from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db, user
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.crud.project import project_crud
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationMyResponse,
                                  DonationResponse)
from app.services import invest

router = APIRouter()


@router.get(
    path='/',
    response_model=List[DonationResponse],
    dependencies=[Depends(user.current_superuser)]
)
async def get_all_donations(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[DonationResponse]:

    return await donation_crud.get_multi(session=session)


@router.post(
    path='/',
    response_model=DonationMyResponse,
    response_model_exclude_none=True
)
async def create_donation(
    new_donation: DonationCreate,
    session: db.AsyncSession = Depends(db.get_async_session),
    user: User = Depends(current_user),
) -> DonationMyResponse:

    donation = await donation_crud.create(
        obj_in=new_donation,
        session=session,
        user=user
    )
    await invest.distribution_of_amounts(
        project=donation,
        false_full=project_crud,
        session=session
    )

    return donation


@router.get(path='/my',
            response_model=List[DonationMyResponse], 
            response_model_exclude={'user_id'},
)
async def get_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations 