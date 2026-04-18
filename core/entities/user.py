"""
Modulo: User Entity
Capa: Core - Entities

Descripción:
Define la entidad de dominio 'User', que representa a un usuario en el sistema.
Esta entidad encapsula los datos y el comportamiento fundamental de un usuario.

Responsabilidades:
- Definir la estructura de datos de un usuario.
- Proporcionar validaciones básicas de sus atributos.
- Encapsular la lógica de negocio simple relacionada con el estado del usuario.

Version: 1.0.0
"""
import logging
from dataclasses import dataclass, field
from uuid import UUID, uuid4

# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

@dataclass
class User:
    """
    Representa la entidad de un usuario en el dominio.

    Esta clase es un objeto de datos que contiene la información esencial
    de un usuario. Es utilizada a través de las capas de la aplicación
    para representar a los usuarios de manera consistente.

    Atributos:
        id (UUID): El identificador único del usuario.
        email (str): La dirección de correo electrónico del usuario. Debe ser única.
        password_hash (str): El hash de la contraseña del usuario.
        role (str): El rol asignado al usuario (e.g., 'admin', 'user').
        active (bool): Estado de activación de la cuenta del usuario.
    """
    email: str
    password_hash: str
    role: str = "user"
    active: bool = True
    id: UUID = field(default_factory=uuid4, kw_only=True)

    def __post_init__(self):
        """
        Realiza validaciones y logging después de la inicialización del objeto.
        """
        self._validate_email()
        self._validate_invariants()
        logger.debug("Entidad User inicializada para el email: %s", self.email)

    def _validate_email(self) -> None:
        """
        Valida que el correo electrónico tenga un formato básico.
        Lanza ValueError si el formato no es válido.
        """
        if not self.email or "@" not in self.email or "." not in self.email.split('@')[1]:
            logger.error("Intento de crear usuario con email inválido: %s", self.email)
            raise ValueError("El formato del correo electrónico no es válido.")

    def _validate_invariants(self) -> None:
        """
        Valida las invariantes de la entidad.
        """
        if not self.role or not self.role.strip():
            logger.error("Intento de crear usuario con rol vacío para email: %s", self.email)
            raise ValueError("El rol del usuario no puede estar vacío.")
        if not self.password_hash:
            logger.error("Intento de crear usuario sin hash de contraseña para email: %s", self.email)
            raise ValueError("El hash de la contraseña no puede estar vacío.")

    def deactivate(self) -> None:
        """
        Desactiva la cuenta del usuario.
        """
        if self.active:
            self.active = False
            logger.info("Usuario %s (ID: %s) ha sido desactivado.", self.email, self.id)
        else:
            logger.warning("Intento de desactivar un usuario ya inactivo: %s", self.email)

    def activate(self) -> None:
        """
        Activa la cuenta del usuario.
        """
        if not self.active:
            self.active = True
            logger.info("Usuario %s (ID: %s) ha sido activado.", self.email, self.id)
        else:
            logger.warning("Intento de activar un usuario ya activo: %s", self.email)

    def change_role(self, new_role: str) -> None:
        """
        Cambia el rol del usuario, validando que el nuevo rol no esté vacío.
        """
        if not new_role or not new_role.strip():
            raise ValueError("El nuevo rol no puede ser nulo o vacío.")
        
        normalized_new_role = new_role.strip().lower()
        if self.role != normalized_new_role:
            old_role = self.role
            self.role = normalized_new_role
            logger.info(
                "Rol del usuario %s cambiado de '%s' a '%s'.",
                self.email, old_role, self.role
            )
        else:
            logger.info(
                "El nuevo rol para %s es el mismo que el actual ('%s'). No se realizaron cambios.",
                self.email, self.role
            )