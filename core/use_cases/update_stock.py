"""
Módulo: Update Stock Use Case
Capa: Core

Descripción:
Implementa el caso de uso para actualizar el stock de un producto existente.

Responsabilidades:
- Orquestar la lógica para encontrar un producto, actualizar su stock y guardarlo.
- Manejar los errores de dominio, como un producto no encontrado.

Version: 1.0.0
"""

import logging
from typing import Dict, Any

from core.product import Product
from core.product_repository import ProductRepository
from core.exceptions import ProductNotFound, DomainError

logger = logging.getLogger(__name__)


class UpdateStock:
    """
    Caso de uso para actualizar la cantidad de stock de un producto.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Inicializa el caso de uso con una implementación del repositorio de productos.

        Args:
            product_repository: Una instancia que cumple con la interfaz ProductRepository.
        """
        self.product_repository = product_repository

    def execute(self, product_id: str, new_stock: int) -> Product:
        """
        Ejecuta el caso de uso para actualizar el stock.

        Args:
            product_id: El ID del producto a actualizar.
            new_stock: La nueva cantidad de stock.

        Returns:
            La entidad Product actualizada.

        Raises:
            ProductNotFound: Si el producto con el ID especificado no se encuentra.
            DomainError: Si el nuevo stock no es válido (p. ej., negativo).
        """
        logger.info(
            "Iniciando caso de uso 'UpdateStock' para el producto ID: %s", product_id
        )

        try:
            product = self.product_repository.find_by_id(product_id)

            if not product:
                logger.warning("Producto no encontrado con ID: %s", product_id)
                raise ProductNotFound(product_id=product_id)

            logger.info(
                "Producto %s encontrado. Stock actual: %d. Actualizando a: %d.",
                product_id,
                product.stock,
                new_stock,
            )

            updated_product = product.update_stock(new_stock)

            self.product_repository.save(updated_product)

            logger.info(
                "Stock del producto %s actualizado exitosamente a %d.",
                product_id,
                new_stock,
            )

            return updated_product

        except DomainError as e:
            logger.error(
                "Error de dominio al actualizar stock para producto %s: %s",
                product_id,
                e,
            )
            raise
        except Exception as e:
            logger.exception(
                "Error inesperado en el caso de uso 'UpdateStock' para el producto ID: %s",
                product_id,
            )
            raise DomainError(
                f"Error inesperado al actualizar el stock: {e}"
            ) from e