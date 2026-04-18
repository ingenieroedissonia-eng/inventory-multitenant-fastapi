"""
Módulo: UserRepository Port
Capa: Core (Ports)

Descripción:
Define la interfaz (puerto) para el repositorio de usuarios.
Esta interfaz abstracta establece el contrato que deben seguir las implementaciones
concretas de repositorios de usuarios, garantizando que la lógica de negocio
(casos de uso) sea independiente de la tecnología de persistencia de datos.

Responsabilidades:
- Definir los métodos estándar para operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
  sobre las entidades de usuario.
- Abstraer los detalles de la base de datos de la capa de dominio.

Version: 1.0.0
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.entities.user import User

logger = logging.getLogger(__name__)


class UserRepository(ABC):
    """
    Interfaz abstracta para el repositorio de usuarios.

    Esta interfaz define el contrato que cualquier repositorio de usuarios
    debe implementar. Desacopla la lógica del dominio de los detalles
    específicos de almacenamiento de datos, siguiendo el Principio de Inversión
    de Dependencias.
    """

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        Guarda una entidad de usuario (crea o actualiza).

        Args:
            user: La entidad User a guardar.

        Returns:
            La entidad User guardada, que puede incluir un ID actualizado
            o timestamps de la base de datos.
        """
        ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Recupera un usuario por su identificador único.

        Args:
            user_id: El identificador único del usuario.

        Returns:
            Una entidad User si se encuentra, de lo contrario None.
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Recupera un usuario por su dirección de correo electrónico.

        Args:
            email: La dirección de correo electrónico del usuario.

        Returns:
            Una entidad User si se encuentra, de lo contrario None.
        """
        ...

    @abstractmethod
    async def get_all(self) -> List[User]:
        """
        Recupera una lista de todos los usuarios.

        Returns:
            Una lista de entidades User. La lista puede estar vacía si no hay usuarios.
        """
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """
        Elimina un usuario por su identificador único.

        Args:
            user_id: El identificador único del usuario a eliminar.

        Returns:
            True si la eliminación fue exitosa, False en caso contrario (por ejemplo,
            si el usuario no fue encontrado).
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> Optional[User]:
        """
        Actualiza una entidad de usuario existente.

        Args:
            user: La entidad User con los datos actualizados.

        Returns:
            La entidad User actualizada si se encuentra y se actualiza,
            de lo contrario None.
        """
        ...