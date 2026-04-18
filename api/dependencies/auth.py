"""
Modulo: Autenticacion y Autorizacion de Dependencias
Capa: API (Presentacion)

Descripcion:
Provee dependencias de FastAPI para manejar la autenticacion y autorizacion
de usuarios a traves de tokens JWT.

Responsabilidades:
- Extraer y validar tokens JWT de las cabeceras de autorizacion.
- Proveer el objeto de usuario autenticado a los endpoints.
- Crear una factoria de dependencias para verificar permisos especificos.

Version: 1.0.0
"""

import logging
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config.settings import Settings
from core.entities.permission import Permission
from core.entities.user import User
from core.exceptions import InvalidCredentials, PermissionDenied, UserNotFound
from core.ports.user_repository import UserRepository
from core.services.jwt_service import JwtService
from core.use_cases.authorize_user import AuthorizeUser
from infrastructure.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_user_repository_instance = InMemoryUserRepository()


def get_settings() -> Settings:
    """
    Dependency para obtener la configuracion de la aplicacion.
    """
    return Settings()


def get_user_repository() -> UserRepository:
    """
    Dependency para obtener la instancia del repositorio de usuarios.
    """
    return _user_repository_instance


def get_jwt_service(
    settings: Annotated[Settings, Depends(get_settings)]
) -> JwtService:
    """
    Dependency para obtener el servicio de JWT.
    """
    return JwtService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def get_authorize_user_use_case(
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthorizeUser:
    """
    Dependency para obtener el caso de uso AuthorizeUser.
    """
    return AuthorizeUser(jwt_service=jwt_service, user_repository=user_repo)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """
    Dependency de FastAPI para obtener el usuario autenticado a partir de un token JWT.

    Raises: