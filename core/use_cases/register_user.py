"""
Modulo: Register User Use Case
Capa: Core

Descripcion:
Contiene el caso de uso para registrar un nuevo usuario en el sistema.

Responsabilidades:
- Orquestar la lógica de negocio para el registro de usuarios.
- Validar que el correo electrónico no esté ya en uso.
- Utilizar el servicio de autenticación para hashear la contraseña.
- Persistir el nuevo usuario a través del puerto del repositorio.
"""

import logging
from typing import TYPE_CHECKING

from core.entities.user import User
from core.exceptions import UserAlreadyExists

if TYPE_CHECKING:
    from core.ports.user_repository import UserRepository
    from core.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class RegisterUser:
    """
    Caso de uso para registrar un nuevo usuario.
    """

    def __init__(
        self, user_repository: "UserRepository", auth_service: "AuthService"
    ) -> None:
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            user_repository (UserRepository): El puerto del repositorio de usuarios.
            auth_service (AuthService): El servicio para operaciones de autenticación.
        """
        self.user_repository = user_repository
        self.auth_service = auth_service
        logger.info("RegisterUser use case initialized.")

    def execute(self, email: str, plain_password: str, role: str = "user") -> User:
        """
        Ejecuta la lógica de registro de un nuevo usuario.

        Args:
            email (str): El correo electrónico del nuevo usuario.
            plain_password (str): La contraseña en texto plano del nuevo usuario.
            role (str): El rol asignado al nuevo usuario. Por defecto es 'user'.

        Returns:
            User: La entidad del usuario recién creado.

        Raises:
            UserAlreadyExists: Si ya existe un usuario con el mismo correo electrónico.
            ValueError: Si el email o la contraseña están vacíos.
        """
        logger.info("Executing RegisterUser use case for email: %s", email)

        if not email or not plain_password:
            logger.warning("Attempted registration with empty email or password.")
            raise ValueError("Email and password cannot be empty.")

        try:
            existing_user = self.user_repository.find_by_email(email)
            if existing_user:
                logger.warning("Registration failed: email %s already exists.", email)
                raise UserAlreadyExists(f"User with email '{email}' already exists.")
        except Exception as e:
            if not isinstance(e, UserAlreadyExists):
                logger.error(
                    "Unexpected error while checking for existing user: %s", e
                )
            raise

        logger.debug("Hashing password for new user: %s", email)
        password_hash = self.auth_service.hash_password(plain_password)

        new_user = User(
            email=email,
            password_hash=password_hash,
            role=role,
            active=True,
        )
        logger.debug("New user entity created for email: %s", email)

        try:
            saved_user = self.user_repository.save(new_user)
            logger.info("Successfully registered new user with ID: %s", saved_user.id)
            return saved_user
        except Exception as e:
            logger.error(
                "Failed to save new user with email %s: %s", email, e, exc_info=True
            )
            # Re-lanzar la excepción para que sea manejada por una capa superior
            raise