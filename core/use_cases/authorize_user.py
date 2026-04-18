"""
Módulo: Authorize User Use Case
Capa: Core

Descripción:
Define el caso de uso para autorizar a un usuario a realizar una acción específica
basándose en su rol.

Responsabilidades:
- Verificar si el rol de un usuario le concede un permiso requerido.
- Lanzar una excepción si la autorización falla.
- Centralizar la lógica de permisos basada en roles.

Version: 1.0.0
"""
import logging
from typing import Dict, List

from core.entities.user import User
from core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class AuthorizeUser:
    """
    Caso de uso para verificar si un usuario tiene permiso para realizar una acción.
    """

    # Este mapa de permisos define qué puede hacer cada rol.
    # En un sistema real, esto podría provenir de una base de datos o un archivo de configuración.
    _permissions: Dict[str, List[str]] = {
        "admin": ["*"],  # El administrador tiene acceso a todo.
        "manager": [
            "product:read",
            "product:create",
            "product:update",
            "product:delete",
            "user:read",
            "user:update_role",
        ],
        "user": [
            "product:read",
            "user:read_self",
        ],
    }

    def __init__(self):
        """
        Inicializa el caso de uso AuthorizeUser.
        """
        logger.info("Caso de uso AuthorizeUser inicializado.")

    def execute(self, user: User, required_permission: str) -> None:
        """
        Ejecuta la lógica de autorización.

        Args:
            user (User): El objeto de usuario que intenta realizar la acción.
            required_permission (str): El permiso requerido, en formato "recurso:acción".
                                       Ej: "product:create".

        Raises:
            PermissionDenied: Si el usuario no está activo o no tiene el rol
                              necesario para el permiso requerido.
        """
        if not user.active:
            logger.warning(
                "Intento de autorización denegado para usuario inactivo ID: %s", user.id
            )
            raise PermissionDenied("El usuario no está activo.")

        user_role = user.role
        allowed_permissions = self._permissions.get(user_role, [])

        if self._has_permission(allowed_permissions, required_permission):
            logger.info(
                "Autorización exitosa para usuario ID: %s (rol: %s) en permiso: %s",
                user.id,
                user_role,
                required_permission,
            )
            return

        logger.warning(
            "Autorización denegada para usuario ID: %s (rol: %s). Permiso requerido: %s. Permisos del rol: %s",
            user.id,
            user_role,
            required_permission,
            allowed_permissions,
        )
        raise PermissionDenied(
            f"El rol '{user_role}' no tiene el permiso '{required_permission}'."
        )

    def _has_permission(
        self, allowed_permissions: List[str], required_permission: str
    ) -> bool:
        """
        Verifica si un permiso requerido está incluido en la lista de permisos permitidos,
        considerando wildcards.

        Args:
            allowed_permissions (List[str]): Lista de permisos que tiene un rol.
            required_permission (str): El permiso que se está verificando.

        Returns:
            bool: True si el permiso es concedido, False en caso contrario.
        """
        if "*" in allowed_permissions:
            return True

        if required_permission in allowed_permissions:
            return True

        try:
            required_resource, _ = required_permission.split(":", 1)
            wildcard_permission = f"{required_resource}:*"
            if wildcard_permission in allowed_permissions:
                return True
        except ValueError:
            # Si el permiso no tiene el formato "recurso:acción", no se puede aplicar wildcard de recurso.
            pass

        return False