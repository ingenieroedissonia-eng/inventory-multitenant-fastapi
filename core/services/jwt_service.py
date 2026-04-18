"""
Modulo: JwtService
Capa: Core

Descripción:
Servicio para la generación y validación de tokens JWT (JSON Web Tokens).

Responsabilidades:
- Crear tokens de acceso con un payload específico y una fecha de expiración.
- Verificar la validez de un token de acceso, incluyendo su firma y expiración.
- Extraer información del payload de un token válido, como el ID de usuario.

Version: 1.0.0
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import jwt

from core.exceptions import InvalidTokenError, TokenExpiredError

logger = logging.getLogger(__name__)


class JwtService:
    """
    Gestiona la creación y verificación de JSON Web Tokens.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
    ):
        """
        Inicializa el servicio JWT.

        Args:
            secret_key (str): La clave secreta para firmar los tokens.
            algorithm (str): El algoritmo de firma a utilizar.
            access_token_expire_minutes (int): El tiempo de vida del token en minutos.
        """
        if not secret_key:
            logger.error("JWT secret key is missing.")
            raise ValueError("JWT secret key cannot be empty")
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(
        self, user_id: UUID, email: str, scopes: Optional[List[str]] = None
    ) -> str:
        """
        Genera un token de acceso JWT.

        El payload incluye el ID de usuario (sub), email, y opcionalmente scopes.

        Args:
            user_id (UUID): El identificador único del usuario.
            email (str): El correo electrónico del usuario.
            scopes (Optional[List[str]]): Lista de permisos o alcances.

        Returns:
            str: El token JWT codificado como una cadena.
        """
        try:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
            to_encode: Dict[str, Any] = {
                "sub": str(user_id),
                "email": email,
                "exp": expire,
                "iat": datetime.now(timezone.utc),
            }
            if scopes:
                to_encode["scopes"] = scopes

            encoded_jwt = jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
            logger.info(f"Access token created for user ID: {user_id}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating access token for user ID {user_id}: {e}")
            raise RuntimeError(f"Could not create access token: {e}") from e

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica un token de acceso JWT y devuelve el payload decodificado.

        Args:
            token (str): El token JWT a verificar.

        Raises:
            TokenExpiredError: Si el token ha expirado.
            InvalidTokenError: Si el token es inválido por cualquier otro motivo.

        Returns:
            Dict[str, Any]: El payload del token decodificado.
        """
        try:
            decoded_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            logger.info(f"Access token verified for user ID: {decoded_token.get('sub')}")
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            logger.warning("Token verification failed: Expired signature")
            raise TokenExpiredError("Token has expired") from e
        except jwt.InvalidTokenError as e:
            logger.error(f"Token verification failed: Invalid token - {e}")
            raise InvalidTokenError(f"Invalid token: {e}") from e

    def get_user_id_from_token(self, token: str) -> Optional[UUID]:
        """
        Extrae el ID de usuario (subject) de un token JWT.

        Args:
            token (str): El token JWT.

        Returns:
            Optional[UUID]: El ID de usuario como un objeto UUID, o None si el token
                            es inválido, ha expirado o no contiene el ID.
        """
        try:
            payload = self.verify_access_token(token)
            user_id_str = payload.get("sub")
            if user_id_str:
                return UUID(user_id_str)
            logger.warning("Token payload does not contain 'sub' (user ID).")
            return None
        except (InvalidTokenError, TokenExpiredError):
            logger.debug("Attempted to get user ID from an invalid or expired token.")
            return None
        except ValueError as e:
            logger.error(f"Error converting user ID from token to UUID: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error extracting user ID from token: {e}")
            return None