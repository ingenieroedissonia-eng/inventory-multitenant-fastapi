"""
Modulo: Repositorio de Productos
Capa: Infrastructure

Descripcion:
Implementacion concreta y en memoria del repositorio de productos.
Utiliza el patron Singleton para garantizar una unica instancia del repositorio
en toda la aplicacion, manteniendo un estado consistente de los datos de productos.

Responsabilidades:
- Persistir y recuperar entidades de Producto en un diccionario en memoria.
- Implementar la interfaz ProductRepository definida en la capa Core.
- Proporcionar una unica instancia global del repositorio.

Version: 1.0.0
"""

import logging
from typing import Dict, Optional, List, Type
from threading import Lock

from core.product import Product
from core.product_repository import ProductRepository
from core.exceptions import ProductNotFound

logger = logging.getLogger(__name__)

class ProductRepositorySingleton(ProductRepository):
    """
    Implementacion Singleton del repositorio de productos en memoria.
    """
    _instance: Optional['ProductRepositorySingleton'] = None
    _lock: Lock = Lock()

    def __init__(self) -> None:
        """
        Constructor privado para el Singleton. No debe ser llamado directamente.
        """
        if ProductRepositorySingleton._instance is not None:
            raise RuntimeError("Esta clase es un Singleton. Use get_instance() para obtener la instancia.")
        self._products: Dict[str, Product] = {}
        logger.info("Instancia de ProductRepositorySingleton creada en memoria.")

    @classmethod
    def get_instance(cls: Type['ProductRepositorySingleton']) -> 'ProductRepositorySingleton':
        """
        Obtiene la unica instancia del repositorio.
        Es thread-safe.

        Returns:
            La instancia unica de ProductRepositorySingleton.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def find_by_id(self, product_id: str) -> Optional[Product]:
        """
        Busca un producto por su ID.

        Args:
            product_id: El ID del producto a buscar.

        Returns:
            El objeto Product si se encuentra, de lo contrario None.
            En esta implementacion, se opta por no lanzar ProductNotFound aqui
            para dar mas flexibilidad al caso de uso, que sera quien decida
            si la no existencia es un error.
        """
        logger.info(f"Buscando producto por ID en repositorio: {product_id}")
        product = self._products.get(product_id)
        if not product:
            logger.warning(f"Producto con ID '{product_id}' no encontrado en el repositorio.")
        return product

    def save(self, product: Product) -> None:
        """
        Guarda (crea o actualiza) un producto en el repositorio.

        Args:
            product: El objeto Product a guardar.
        """
        logger.info(f"Guardando producto ID: {product.id} con stock: {product.stock}")
        try:
            self._products[product.id] = product
            logger.debug(f"Producto {product.id} guardado exitosamente.")
        except Exception as e:
            logger.error(f"Error inesperado al guardar el producto {product.id}: {e}", exc_info=True)
            # En un sistema real, podriamos querer re-lanzar una excepcion de infraestructura
            raise

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos del repositorio.

        Returns:
            Una lista de todos los objetos Product.
        """
        logger.info("Recuperando todos los productos del repositorio.")
        return list(self._products.values())

    def delete(self, product_id: str) -> bool:
        """
        Elimina un producto del repositorio por su ID.

        Args:
            product_id: El ID del producto a eliminar.

        Returns:
            True si el producto fue eliminado, False si no se encontro.
        """
        logger.info(f"Intentando eliminar producto con ID: {product_id}")
        if product_id in self._products:
            try:
                del self._products[product_id]
                logger.info(f"Producto con ID: {product_id} eliminado exitosamente.")
                return True
            except KeyError:
                logger.warning(f"Condicion de carrera: Producto {product_id} no encontrado durante eliminacion.")
                return False
        else:
            logger.warning(f"Intento de eliminar producto no existente con ID: {product_id}")
            return False

    def clear(self) -> None:
        """
        Limpia todos los productos del repositorio.
        Util principalmente para testing.
        """
        logger.info("Limpiando todos los datos del repositorio en memoria.")
        self._products.clear()