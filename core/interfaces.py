"""
Modulo: Interfaces
Capa: Core

Descripcion:
Define las interfaces (contratos) para los repositorios de persistencia.
Estas interfaces son clases base abstractas que desacoplan el núcleo de la
aplicación de las implementaciones concretas de la capa de infraestructura.

Responsabilidades:
- Definir el contrato para el repositorio de Tenants (`TenantRepository`).
- Definir el contrato para el repositorio de Productos (`ProductRepository`).
- Definir el contrato para el repositorio de Movimientos de Stock (`StockMovementRepository`).

Version: 1.0.0
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.product import Product
from core.stock_movement import StockMovement
from core.tenant import Tenant

logger = logging.getLogger(__name__)


class TenantRepository(ABC):
    """
    Interfaz abstracta para el repositorio de Tenants.
    Define los métodos que cualquier implementación concreta debe proporcionar
    para interactuar con la persistencia de datos de Tenants.
    """

    @abstractmethod
    async def get_by_id(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Recupera un tenant por su ID.

        :param tenant_id: El UUID del tenant a recuperar.
        :return: Un objeto Tenant si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        Recupera un tenant por su nombre.

        :param name: El nombre del tenant a recuperar.
        :return: Un objeto Tenant si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, tenant: Tenant) -> Tenant:
        """
        Guarda (crea o actualiza) un tenant en la persistencia.

        :param tenant: El objeto Tenant a guardar.
        :return: El objeto Tenant guardado, posiblemente con campos actualizados (ej. ID).
        """
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> List[Tenant]:
        """
        Lista todos los tenants disponibles.

        :return: Una lista de objetos Tenant.
        """
        raise NotImplementedError


class ProductRepository(ABC):
    """
    Interfaz abstracta para el repositorio de Productos.
    Define los métodos necesarios para la persistencia de datos de Productos.
    """

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Recupera un producto por su ID.

        :param product_id: El UUID del producto a recuperar.
        :return: Un objeto Product si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_sku(self, tenant_id: UUID, sku: str) -> Optional[Product]:
        """
        Recupera un producto por su SKU dentro de un tenant específico.

        :param tenant_id: El UUID del tenant al que pertenece el producto.
        :param sku: El SKU del producto a buscar.
        :return: Un objeto Product si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        Guarda un nuevo producto en la persistencia.

        :param product: El objeto Product a guardar.
        :return: El objeto Product guardado.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """
        Actualiza un producto existente en la persistencia.

        :param product: El objeto Product con los datos actualizados.
        :return: El objeto Product actualizado.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID) -> List[Product]:
        """
        Lista todos los productos pertenecientes a un tenant.

        :param tenant_id: El UUID del tenant.
        :return: Una lista de objetos Product.
        """
        raise NotImplementedError


class StockMovementRepository(ABC):
    """
    Interfaz abstracta para el repositorio de Movimientos de Stock.
    Define los métodos para la persistencia de los registros de movimientos de inventario.
    """

    @abstractmethod
    async def save(self, movement: StockMovement) -> StockMovement:
        """
        Guarda un nuevo movimiento de stock en la persistencia.

        :param movement: El objeto StockMovement a guardar.
        :return: El objeto StockMovement guardado.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, movement_id: UUID) -> Optional[StockMovement]:
        """
        Recupera un movimiento de stock por su ID.

        :param movement_id: El UUID del movimiento a recuperar.
        :return: Un objeto StockMovement si se encuentra, de lo contrario None.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_by_product(
        self, product_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[StockMovement]:
        """
        Lista los movimientos de stock para un producto específico, con paginación.

        :param product_id: El UUID del producto.
        :param limit: El número máximo de movimientos a devolver.
        :param offset: El número de movimientos a omitir (para paginación).
        :return: Una lista de objetos StockMovement.
        """
        raise NotImplementedError