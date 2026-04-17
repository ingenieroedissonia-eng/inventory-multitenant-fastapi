"""
Modulo: api/auth_router.py
Capa: API (Presentación)

Descripción:
Router de FastAPI para los endpoints de autenticación y autorización.

Responsabilidades:
- Exponer endpoints para registro, login, obtención de usuario actual y chequeo de permisos.
- Manejar las solicitudes HTTP y las respuestas.
- Utilizar inyección de dependencias para desacoplar la lógica de negocio.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from api.dependencies.auth import PermissionChecker, get_current_user
from config.settings import Settings
from core.entities.permission import Permission
from core.entities.user import User
from core.exceptions import InvalidCredentials, UserAlreadyExists
from core.ports.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.services.jwt_service import JwtService
from core.use_cases.authenticate_user import AuthenticateUser
from core.use_cases.register_user import RegisterUser
from infrastructure.repositories.in_memory_user_repository import \
    get_in_memory_user_repository

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class UserRegistrationRequest(BaseModel):
    """Schema para el registro de un nuevo usuario."""
    email: EmailStr
    password: str
    role: str = "user"


class UserResponse(BaseModel):
    """Schema para la respuesta de datos de usuario (sin password)."""
    id: str
    email: EmailStr
    role: str
    active: bool

    class Config:
        """Configuración del modelo Pydantic."""
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema para la respuesta del token de acceso."""
    access_token: str
    token_type: str


def get_settings() -> Settings:
    """Dependencia para obtener la configuración de la aplicación."""
    return Settings()


def get_user_repository() -> UserRepository:
    """Dependencia para obtener el repositorio de usuarios."""
    return get_in_memory_user_repository()


def get_auth_service() -> AuthService:
    """Dependencia para obtener el servicio de autenticación."""
    return AuthService()


def get_jwt_service(
    settings: Annotated[Settings, Depends(get_settings)]
) -> JwtService:
    """Dependencia para obtener el servicio de JWT."""
    return JwtService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def get_register_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> RegisterUser:
    """Dependencia para obtener el caso de uso de registro de usuario."""
    return RegisterUser(user_repository=user_repo, auth_service=auth_service)


def get_authenticate_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)]
) -> AuthenticateUser:
    """Dependencia para obtener el caso de uso de autenticación de usuario."""
    return AuthenticateUser(
        user_repository=user_repo,
        auth_service=auth_service,
        jwt_service=jwt_service
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegistrationRequest,
    register_user_uc: Annotated[RegisterUser, Depends(get_register_user_use_case)],
):
    """
    Endpoint para registrar un nuevo usuario.
    """
    try:
        logger.info(f"Attempting to register user with email: {request.email}")
        user = register_user_uc.execute(
            email=request.email,
            password=request.password,
            role=request.role
        )
        logger.info(f"User {request.email} registered successfully.")
        return user
    except UserAlreadyExists as e:
        logger.warning(f"Registration failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(
    request: UserRegistrationRequest,
    authenticate_user_uc: Annotated[AuthenticateUser, Depends(get_authenticate_user_use_case)],
):
    """
    Endpoint para autenticar un usuario y obtener un token JWT.
    """
    try:
        logger.info(f"Login attempt for user: {request.email}")
        token_data = authenticate_user_uc.execute(request.email, request.password)
        logger.info(f"User {request.email} authenticated successfully.")
        return token_data
    except InvalidCredentials as e:
        logger.warning(f"Invalid login attempt for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Endpoint protegido para obtener los detalles del usuario autenticado.
    Requiere un token JWT válido en la cabecera de autorización.
    """
    logger.info(f"Fetching details for current user: {current_user.email}")
    return current_user


@router.get("/check-permission")
async def check_permission(
    user: Annotated[User, Depends(PermissionChecker(Permission(resource="dashboard", action="read")))]
):
    """
    Endpoint protegido para verificar si el usuario tiene un permiso específico.

    Este endpoint está protegido por `PermissionChecker` que valida si el rol del
    usuario autenticado tiene el permiso `dashboard:read`.
    """
    logger.info(f"User {user.email} successfully accessed protected endpoint with permission 'dashboard:read'.")
    return {
        "status": "ok",
        "message": "Permission granted",
        "user_email": user.email,
        "user_role": user.role
    }