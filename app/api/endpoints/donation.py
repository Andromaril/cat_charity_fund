from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate,
                                  DonationResponse, DonationResponseMyDonation)
from app.services import invest

router = APIRouter()


@router.get(
    path='/',
    response_model=List[DonationResponse],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: db.AsyncSession = Depends(db.get_async_session)
) -> List[DonationResponse]:

    return await donation_crud.get_multi(session=session)


@router.post(
    path='/',
    response_model=DonationResponseMyDonation,
    response_model_exclude_none=True
)
async def create_donation(
    new_donation: DonationCreate,
    session: db.AsyncSession = Depends(db.get_async_session),
    user: User = Depends(current_user),
) -> DonationResponseMyDonation:

    donation = await donation_crud.create(
        obj_in=new_donation,
        session=session,
        user=user
    )
    await invest.func_invest_donation(
        project=donation,
        session=session
    )

    return donation


@router.get(path='/my',
            response_model=List[DonationResponseMyDonation],
            response_model_exclude={'user_id'},
            )
async def get_my_donation(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> List[DonationResponseMyDonation]:
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations