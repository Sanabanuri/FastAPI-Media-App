import uuid
from typing import Optional
from fastapi import Depends, Request, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
    Strategy
)
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db

SECRET = "hy$3j4sim3r3lY4s3c"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

def get_custom_auth_router(
    backend: AuthenticationBackend,
    get_user_manager = get_user_manager,
    authenticator = None,
):
    router = APIRouter()

    @router.post("/login", name=f"auth:{backend.name}.login")
    async def login(
        request: Request,
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: BaseUserManager[User, uuid.UUID] = Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        
        try:
             user = await user_manager.get_by_email(credentials.username)
        except exceptions.UserNotExists:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not registered",
            )

        user = await user_manager.authenticate(credentials)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials",
            )
        
        if not user.is_active:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is inactive",
            )



        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    return router

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, auth_backends=[auth_backend])
current_active_user = fastapi_users.current_user(active=True)