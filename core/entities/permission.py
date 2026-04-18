"""
Modulo: core.entities.permission
Capa: Core

Descripcion:
Define la entidad de dominio `Permission`, que representa una autorización específica
dentro del sistema.

Responsabilidades:
- Encapsular los datos de un permiso (recurso y acción).
- Garantizar la validez e invariantes de la entidad a través de validaciones internas.
- Proporcionar una representación inmutable de un permiso.

Version: 1.0.0
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Permission:
    """
    Entidad que representa un permiso para realizar una acción sobre un recurso.

    Atributos:
        resource (str): El recurso al que se aplica el permiso (ej: 'users', 'orders').
        action (str): La acción permitida sobre el recurso (ej: 'create', 'read', 'update', 'delete').
        id (UUID): Identificador único del permiso.
        created_at (datetime): Fecha y hora de creación del permiso.
    """
    resource: str
    action: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """
        Realiza validaciones después de la inicialización del objeto.
        """
        try:
            self._validate_invariants()
            logger.debug("Permission entity created successfully: %s", self)
        except ValueError as e:
            logger.error("Failed to create Permission entity due to validation error: %s", e)
            raise

    def _validate_invariants(self) -> None:
        """
        Valida las reglas de negocio y consistencia interna de la entidad.

        Raises:
            ValueError: Si el recurso o la acción son cadenas vacías o inválidas.
        """
        if not self.resource or not self.resource.strip():
            raise ValueError("Resource cannot be empty or just whitespace.")

        if not self.action or not self.action.strip():
            raise ValueError("Action cannot be empty or just whitespace.")

        logger.debug("Invariants validated for permission ID: %s", self.id)

    def __str__(self) -> str:
        """
        Representación en cadena de la entidad Permission.
        """
        return f"Permission(action='{self.action}', resource='{self.resource}')"

    def __repr__(self) -> str:
        """
        Representación detallada de la entidad Permission para depuración.
        """
        return f"<Permission id={self.id} action='{self.action}' resource='{self.resource}'>"