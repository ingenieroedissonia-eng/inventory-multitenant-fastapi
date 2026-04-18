"""
Modulo: Authenticate User Use Case
Capa: Core

Descripción:
Define el caso de uso para autenticar a un usuario existente en el sistema.

Responsabilidades:
- Validar las credenciales (email y contraseña) de un usuario.
- Orquestar la obtención de datos del usuario desde el repositorio.
- Utilizar el servicio de autenticación para verificar la contraseña.
- Utilizar el servicio JWT para generar un token de acceso si las credenciales son válidas.
- Lanzar excepciones específicas en caso de fallo (usuario no encontrado, credenciales inválidas).

Version: 1.0.0
"""
import logging
from typing import TYPE_CHECKING

from core.exceptions import InvalidCredentials, UserNotFound

if TYPE_CHECKING:
    from core.ports.user_repository import UserRepository
    from core.services.auth_service import AuthService
    from core.services.jwt_service import JwtService

logger = logging.getLogger(__name__)


class AuthenticateUser:
    """
    Caso de uso para autenticar un usuario y generar un token JWT.
    """

    def __init__(
        self,
        user_repository: "UserRepository",
        auth_service: "AuthService",
        jwt_service: "JwtService",
    ):
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            user_repository (UserRepository): El puerto del repositorio de usuarios.
            auth_service (AuthService): El servicio para la lógica de autenticación (hashing, verificación).
            jwt_service (JwtService): El servicio para la creación y validación de tokens JWT.
        """
        self._user_repository = user_repository
        self._auth_service = auth_service
        self._jwt_service = jwt_service

    def execute(self, email: str, plain_password: str) -> str:
        """
        Ejecuta el flujo de autenticación del usuario.

        Args:
            email (str): El correo electrónico del usuario a autenticar.
            plain_password (str): La contraseña en texto plano del usuario.

        Returns:
            str: Un token de acceso JWT si la autenticación es exitosa.

        Raises:
            UserNotFound: Si no se encuentra ningún usuario con el email proporcionado.
            InvalidCredentials: Si la contraseña proporcionada no coincide con la almacenada.
        """
        logger.info("Iniciando intento de autenticación para el email: %s", email)

        try:
            user = self._user_repository.get_by_email(email)

            if not user:
                logger.warning(
                    "Fallo de autenticación: Usuario no encontrado para el email: %s",
                    email,
                )
                raise UserNotFound(f"User with email {email} not found.")

            is_password_valid = self._auth_service.verify_password(
                plain_password, user.password_hash
            )

            if not is_password_valid:
                logger.warning(
                    "Fallo de autenticación: Contraseña inválida para el usuario: %s",
                    user.id,
                )
                raise InvalidCredentials("Invalid credentials provided.")

            if not user.active:
                logger.warning(
                    "Fallo de autenticación: El usuario %s está inactivo.", user.id
                )
                raise InvalidCredentials("User account is not active.")

            token = self._jwt_service.create_access_token(user=user)
            logger.info(
                "Autenticación exitosa para el usuario: %s. Token generado.", user.id
            )

            return token

        except UserNotFound as e:
            raise e
        except InvalidCredentials as e:
            raise e
        except Exception as e:
            logger.error(
                "Error inesperado durante la autenticación para el email %s: %s",
                email,
                e,
                exc_info=True,
            )
            raise InvalidCredentials("An unexpected error occurred during authentication.") from e