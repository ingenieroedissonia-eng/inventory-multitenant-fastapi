"""
Modulo: AuthService
Capa: Core (Servicios de Dominio)

Descripcion:
Proporciona servicios de autenticacion, encapsulando la logica de hashing
y verificacion de contraseñas de forma segura utilizando la libreria bcrypt.

Responsabilidades:
- Crear un hash seguro de una contraseña en texto plano.
- Verificar si una contraseña en texto plano coincide con un hash existente.

Version: 1.0.0
"""

import logging
from typing import TYPE_CHECKING

import bcrypt

from core.exceptions import InvalidCredentials

if TYPE_CHECKING:
    from core.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    """
    Servicio de dominio para gestionar la autenticacion y la seguridad de contraseñas.
    """

    def __init__(self, user_repository: "UserRepository"):
        """
        Inicializa el servicio de autenticacion.

        Args:
            user_repository (UserRepository): El puerto del repositorio de usuarios
                                              para futuras interacciones de datos.
        """
        self.user_repository = user_repository
        logger.info("AuthService inicializado.")

    def hash_password(self, plain_password: str) -> str:
        """
        Genera un hash seguro para una contraseña en texto plano.

        Args:
            plain_password (str): La contraseña en texto plano a hashear.

        Returns:
            str: El hash de la contraseña, codificado como una cadena utf-8.
        """
        try:
            password_bytes = plain_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_bytes = bcrypt.hashpw(password_bytes, salt)
            hashed_password = hashed_bytes.decode('utf-8')
            logger.debug("Contraseña hasheada exitosamente.")
            return hashed_password
        except (TypeError, ValueError) as e:
            logger.error("Error al hashear la contraseña: %s", e, exc_info=True)
            raise InvalidCredentials("Error interno durante el procesamiento de la contraseña.") from e

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con un hash almacenado.

        Args:
            plain_password (str): La contraseña en texto plano a verificar.
            hashed_password (str): El hash de la contraseña contra el cual comparar.

        Returns:
            bool: True si la contraseña es valida.

        Raises:
            InvalidCredentials: Si la contraseña no coincide o el hash es invalido.
        """
        logger.debug("Iniciando verificacion de contraseña.")
        try:
            plain_password_bytes = plain_password.encode('utf-8')
            hashed_password_bytes = hashed_password.encode('utf-8')

            if bcrypt.checkpw(plain_password_bytes, hashed_password_bytes):
                logger.info("Verificacion de contraseña exitosa.")
                return True
            else:
                logger.warning("Intento de autenticacion fallido: contraseña incorrecta.")
                raise InvalidCredentials("La contraseña proporcionada es incorrecta.")

        except ValueError as e:
            logger.error(
                "Error de verificacion: el hash almacenado podria ser invalido. %s",
                e,
                exc_info=True
            )
            raise InvalidCredentials("Error al verificar credenciales.") from e
        except Exception as e:
            logger.critical(
                "Error inesperado durante la verificacion de contraseña: %s",
                e,
                exc_info=True
            )
            raise InvalidCredentials("Ocurrio un error inesperado durante la autenticacion.") from e