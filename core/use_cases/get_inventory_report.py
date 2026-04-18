"""
Modulo: Get Inventory Report Use Case
Capa: Core

Descripcion:
Implementa el caso de uso para obtener un reporte de productos con bajo inventario
para un tenant específico.

Responsabilidades:
- Validar los datos de entrada (umbral de stock).
- Orquestar la obtención de datos desde el repositorio de productos.
- Aplicar la lógica de negocio para filtrar productos por debajo del umbral.
- Devolver una lista de productos que cumplen con el criterio.

Version: 1.0.0
"""
import logging
from typing import List
from uuid import UUID

from core.exceptions import DomainError, TenantNotFound
from core.interfaces import ProductRepository, TenantRepository
from core.product import Product

logger = logging.getLogger(__name__)


class GetInventoryReport:
    """
    Caso de uso para generar un reporte de productos con stock bajo.
    """

    def __init__(
        self,
        product_repository: ProductRepository,
        tenant_repository: TenantRepository,
    ):
        """
        Inicializa el caso de uso con las dependencias necesarias.

        Args:
            product_repository: Repositorio para acceder a los datos de los productos.
            tenant_repository: Repositorio para verificar la existencia del tenant.
        """
        self.product_repository = product_repository
        self.tenant_repository = tenant_repository

    async def execute(
        self, tenant_id: UUID, low_stock_threshold: int
    ) -> List[Product]:
        """
        Ejecuta el caso de uso para obtener productos con bajo stock.

        Args:
            tenant_id: El identificador único del tenant.
            low_stock_threshold: El umbral de stock por debajo del cual un producto
                                 se considera con bajo inventario.

        Returns:
            Una lista de entidades Product que tienen un stock inferior al umbral.

        Raises:
            DomainError: Si el umbral de stock es un valor negativo.
            TenantNotFound: Si el tenant con el ID proporcionado no existe.
        """
        logger.info(
            "Executing GetInventoryReport for tenant %s with threshold %d",
            tenant_id,
            low_stock_threshold,
        )

        if low_stock_threshold < 0:
            msg = "Low stock threshold cannot be negative."
            logger.error(msg)
            raise DomainError(msg)

        try:
            tenant = await self.tenant_repository.get_by_id(tenant_id)
            if not tenant:
                raise TenantNotFound(f"Tenant with id '{tenant_id}' not found.")

            all_products = await self.product_repository.get_all_by_tenant(tenant_id)

            low_stock_products = [
                product
                for product in all_products
                if product.stock < low_stock_threshold
            ]

            logger.info(
                "Found %d products with stock below threshold %d for tenant %s.",
                len(low_stock_products),
                low_stock_threshold,
                tenant_id,
            )

            return low_stock_products

        except TenantNotFound as e:
            logger.warning("Tenant not found during inventory report generation: %s", e)
            raise

        except Exception as e:
            msg = f"An unexpected error occurred while generating inventory report for tenant {tenant_id}: {e}"
            logger.exception(msg)
            raise DomainError(msg) from e