"""
Modulo: stock_movement
Capa: Core

Descripcion:
Define la entidad de dominio para los movimientos de stock.

Responsabilidades:
- Representar un movimiento de stock (entrada o salida).
- Validar la integridad de los datos de un movimiento de stock.
- Asegurar que los atributos de la entidad sean consistentes.

Version: 1.0.0
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from core.exceptions import DomainError

logger = logging.getLogger(__name__)

VALID_MOVEMENT_TYPES = ("IN", "OUT")


@dataclass
class StockMovement:
    """
    Entidad que representa un movimiento de inventario para un producto.

    Atributos:
        product_id (uuid.UUID): ID del producto asociado al movimiento.
        type (Literal["IN", "OUT"]): Tipo de movimiento (entrada o salida).
        quantity (int): Cantidad de unidades movidas.
        reason (str): Motivo del movimiento (ej. 'venta', 'ajuste', 'compra').
        id (uuid.UUID): Identificador único del movimiento.
        timestamp (datetime): Fecha y hora en que se registró el movimiento.
    """
    product_id: uuid.UUID
    type: Literal["IN", "OUT"]
    quantity: int
    reason: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """
        Realiza validaciones de la entidad después de su inicialización.
        """
        logger.debug(f"Validating StockMovement with id: {self.id}")
        self._validate_product_id()
        self._validate_type()
        self._validate_quantity()
        self._validate_reason()
        self._validate_timestamp()
        logger.debug(f"StockMovement with id: {self.id} validated successfully.")

    def _validate_product_id(self):
        """Valida que el product_id sea un UUID válido."""
        if not isinstance(self.product_id, uuid.UUID):
            logger.error(f"Validation failed for product_id: {self.product_id}. Not a UUID.")
            raise DomainError("Invalid product_id. Must be a UUID.")

    def _validate_type(self):
        """Valida que el tipo de movimiento sea 'IN' o 'OUT'."""
        if self.type not in VALID_MOVEMENT_TYPES:
            logger.error(f"Validation failed for type: {self.type}. Not in {VALID_MOVEMENT_TYPES}.")
            raise DomainError(f"Invalid movement type. Must be one of {VALID_MOVEMENT_TYPES}.")

    def _validate_quantity(self):
        """Valida que la cantidad sea un entero positivo."""
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            logger.error(f"Validation failed for quantity: {self.quantity}. Not a positive integer.")
            raise DomainError("Invalid quantity. Must be a positive integer.")

    def _validate_reason(self):
        """Valida que la razón sea una cadena de texto no vacía."""
        reason_stripped = self.reason.strip() if isinstance(self.reason, str) else ""
        if not reason_stripped:
            logger.error("Validation failed for reason. Must be a non-empty string.")
            raise DomainError("Invalid reason. Must be a non-empty string.")
        self.reason = reason_stripped

    def _validate_timestamp(self):
        """Valida que el timestamp sea un objeto datetime."""
        if not isinstance(self.timestamp, datetime):
            logger.error(f"Validation failed for timestamp: {self.timestamp}. Not a datetime object.")
            raise DomainError("Invalid timestamp. Must be a datetime object.")