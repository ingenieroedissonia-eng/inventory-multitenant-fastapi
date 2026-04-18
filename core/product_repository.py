"""
Módulo: Product Repository Interface
Capa: Core

Descripción:
Define la interfaz abstracta para el repositorio de productos.
Esta interfaz desacopla los casos de uso de la implementación concreta
de la persistencia de datos.

Responsabilidades:
- Definir los métodos que cualquier repositorio de productos debe implementar.
- Servir como un contrato para la capa de infraestructura.

Version: 1.0.0
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

from core.product import Product

logger = logging.getLogger(__name__)


class ProductRepository(ABC):
    """
    Interfaz abstracta que define las operaciones de persistencia para la entidad Product.
    """

    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        """
        Busca un producto por su ID.

        Args:
            product_id: El ID del producto a buscar.

        Returns:
            Una instancia de Product si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, product: Product) -> None:
        """
        Guarda o actualiza un producto en el sistema de persistencia.

        Args:
            product: La instancia del producto a guardar.

        Raises:
            Exception: Si ocurre un error durante la operación de guardado.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Product]:
        """
        Recupera todos los productos del sistema de persistencia.

        Returns:
            Una lista de todas las instancias de Product.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id: El ID del producto a eliminar.

        Returns:
            True si el producto fue eliminado, False si no se encontró.
        """
        raise NotImplementedError