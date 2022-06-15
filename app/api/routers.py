from fastapi import APIRouter

from app.api.endpoints import project, donation, user

main_router = APIRouter()

main_router.include_router(
    router=project.router,
    prefix='/charity_project',
    tags=['Charity Projects'],
)

main_router.include_router(
    router=donation.router,
    prefix='/donation',
    tags=['Donations']
)
main_router.include_router(
    router=user.router
)