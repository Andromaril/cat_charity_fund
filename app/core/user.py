from typing import Union

import fastapi as fa
import fastapi_users as fa_u
import fastapi_users.authentication as auth
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, db
from app.models import user as models
from app.schemas import user as schemas


async def get_user_db(
    session: db.AsyncSession = fa.Depends(db.get_async_session)
):
    yield SQLAlchemyUserDatabase(schemas.UserDB, session, models.UserTable)


def get_jwt_strategy() -> auth.JWTStrategy:

    return auth.JWTStrategy(
        secret=config.settings.secret,
        lifetime_seconds=3600
    )


bearer_transport = auth.BearerTransport(tokenUrl='auth/jwt/login')

auth_backend = auth.AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(fa_u.BaseUserManager[schemas.UserCreate, schemas.UserDB]):

    user_db_model = schemas.UserDB
    reset_password_token_secret = config.settings.secret
    verification_token_secret = config.settings.secret

    async def validate_password(
        self,
        password: str,
        user: Union[schemas.UserCreate, schemas.UserDB],
    ) -> None:

        if len(password) < 3:
            raise fa_u.InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        if user.email in password:
            raise fa_u.InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self,
            user: schemas.UserDB,
            request: Union[None, fa.Request] = None
    ):

        print(f'Пользователь {user.email} был зарегистрирован')


async def get_user_manager(user_db=fa.Depends(get_user_db)):
 
    yield UserManager(user_db)

fastapi_users = fa_u.FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
    user_model=schemas.User,
    user_create_model=schemas.UserCreate,
    user_update_model=schemas.UserUpdate,
    user_db_model=schemas.UserDB
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)