"""
Modulo: Excepciones del Core
Capa: Core

Descripcion:
Define las excepciones personalizadas utilizadas en la capa de dominio y aplicacion.
Estas excepciones permiten un manejo de errores mas granular y semantico
en toda la aplicacion, facilitando la depuracion y la respuesta adecuada
en las capas superiores (e.g., API).

Responsabilidades:
- Proveer una clase base para todas las excepciones de la aplicacion.
- Definir excepciones especificas para escenarios de negocio comunes como
  autenticacion, autorizacion y gestion de entidades.

Version: 1.0.0
"""

import logging

logger = logging.getLogger(__name__)


class ApplicationException(Exception):
    """
    Clase base para todas las excepciones personalizadas de la aplicacion.

    Heredar de esta clase permite capturar todas las excepciones de negocio
    de forma centralizada si es necesario.
    """

    def __init__(self, message: str):
        """
        Inicializa la excepcion con un mensaje descriptivo.

        Args:
            message (str): El mensaje de error.
        """
        self.message = message
        logger.warning(f"{self.__class__.__name__}: {message}")
        super().__init__(self.message)


class UserNotFound(ApplicationException):
    """
    Lanzada cuando se intenta operar sobre un usuario que no existe en el sistema.

    Esto es comun en operaciones de busqueda, actualizacion o eliminacion.
    """

    def __init__(self, identifier: str):
        """
        Inicializa la excepcion.

        Args:
            identifier (str): El identificador (ID, email, etc.) usado para buscar al usuario.
        """
        message = f"User with identifier '{identifier}' not found."
        super().__init__(message)


class UserAlreadyExists(ApplicationException):
    """
    Lanzada cuando se intenta crear un usuario que ya existe en el sistema.

    Tipicamente se verifica por un campo unico como el email.
    """

    def __init__(self, email: str):
        """
        Inicializa la excepcion.

        Args:
            email (str): El email que ya esta registrado en el sistema.
        """
        message = f"User with email '{email}' already exists."
        super().__init__(message)


class InvalidCredentials(ApplicationException):
    """
    Lanzada durante el proceso de autenticacion cuando las credenciales
    proporcionadas (e.g., email/password) son incorrectas.
    """

    def __init__(self, message: str = "Invalid credentials provided."):
        """
        Inicializa la excepcion con un mensaje generico para no revelar
        informacion sobre si el usuario existe o no.

        Args:
            message (str): Mensaje de error generico.
        """
        super().__init__(message)


class PermissionDenied(ApplicationException):
    """
    Lanzada cuando un usuario autenticado intenta realizar una accion
    para la cual no tiene los permisos necesarios.
    """

    def __init__(self, user_id: str, required_permission: str):
        """
        Inicializa la excepcion detallando el usuario y el permiso faltante.

        Args:
            user_id (str): El ID del usuario que intenta realizar la accion.
            required_permission (str): La descripcion del permiso requerido.
        """
        message = (
            f"User '{user_id}' does not have the required permission "
            f"'{required_permission}' to perform this action."
        )
        super().__init__(message)