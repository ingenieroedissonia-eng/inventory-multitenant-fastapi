"""
Modulo: in_memory_stock_movement_repository
Capa: Infrastructure

Descripcion:
Implementacion en memoria del repositorio de movimientos de stock.

Responsabilidades:
- Almacenar y recuperar entidades de StockMovement en un diccionario en memoria.
- Simular la persistencia de datos para desarrollo y pruebas.
- Cumplir con la interfaz StockMovementRepository.

Version: 1.0.0
"""
import logging
import uuid
from typing import Dict, List, Optional
from uuid import UUID

from core.exceptions import DomainError
from core.interfaces import StockMovementRepository
from core.stock_movement import StockMovement

logger = logging.getLogger(__name__)


class InMemoryStockMovementRepository(StockMovementRepository):
    """
    Implementa el repositorio de movimientos de stock con almacenamiento en memoria.
    """

    def __init__(self) -> None:
        """
        Inicializa el repositorio en memoria para movimientos de stock.
        """
        self._movements: Dict[UUID, StockMovement] = {}
        logger.info("InMemoryStockMovementRepository initialized.")

    async def save(self, movement: StockMovement) -> StockMovement:
        """
        Guarda un nuevo movimiento de stock o actualiza uno existente.

        Args:
            movement: La entidad StockMovement a guardar.

        Returns:
            La entidad StockMovement guardada.

        Raises:
            DomainError: Si ocurre un error inesperado al guardar.
        """
        try:
            if not movement.id:
                movement.id = uuid.uuid4()

            logger.info("Saving stock movement with ID: %s", movement.id)
            self._movements[movement.id] = movement
            return movement
        except Exception as e:
            logger.error(
                "Failed to save stock movement %s: %s", movement.id, e, exc_info=True
            )
            raise DomainError(f"Could not save stock movement: {e}") from e

    async def get_by_id(self, movement_id: UUID) -> Optional[StockMovement]:
        """
        Obtiene un movimiento de stock por su ID.

        Args:
            movement_id: El ID del movimiento de stock a buscar.

        Returns:
            La entidad StockMovement si se encuentra, de lo contrario None.
        """
        logger.debug("Fetching stock movement by ID: %s", movement_id)
        return self._movements.get(movement_id)

    async def list_by_product(self, product_id: UUID) -> List[StockMovement]:
        """
        Lista todos los movimientos de stock para un producto específico, ordenados por fecha.

        Args:
            product_id: El ID del producto para el cual listar los movimientos.

        Returns:
            Una lista de entidades StockMovement.
        """
        logger.info("Listing stock movements for product ID: %s", product_id)
        try:
            product_movements = [
                mov
                for mov in self._movements.values()
                if mov.product_id == product_id
            ]

            sorted_movements = sorted(
                product_movements, key=lambda m: m.timestamp, reverse=True
            )
            logger.info(
                "Found %d movements for product %s", len(sorted_movements), product_id
            )
            return sorted_movements
        except Exception as e:
            logger.error(
                "Failed to list movements for product %s: %s", product_id, e, exc_info=True
            )
            raise DomainError(f"Could not list movements for product {product_id}: {e}") from e