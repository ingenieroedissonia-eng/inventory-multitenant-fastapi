"""
Modulo: Create Product Use Case
Capa: Core (Casos de Uso)

Descripcion:
Implementa el caso de uso para crear un nuevo producto, asegurando la unicidad
del SKU por tenant.

Responsabilidades:
- Orquestar la validación de la existencia del tenant.
- Orquestar la validación de la unicidad del SKU del producto.
- Orquestar la creación y persistencia de una nueva entidad de producto.

Version: 1.0.0
"""

import logging
from uuid import UUID

from core.exceptions import DomainError, TenantNotFound
from core.interfaces import ProductRepository, TenantRepository
from core.product import Product

logger = logging.getLogger(__name__)


class CreateProduct:
    """
    Caso de uso para crear un nuevo producto.
    """

    def __init__(
        self,
        product_repository: ProductRepository,
        tenant_repository: TenantRepository,
    ):
        """
        Inicializa el caso de uso con las dependencias necesarias.

        Args:
            product_repository (ProductRepository): El repositorio para operaciones de productos.
            tenant_repository (TenantRepository): El repositorio para operaciones de tenants.
        """
        self.product_repository = product_repository
        self.tenant_repository = tenant_repository

    async def execute(
        self,
        tenant_id: UUID,
        name: str,
        sku: str,
        price: float,
        stock: int,
        category: str,
    ) -> Product:
        """
        Ejecuta el caso de uso para crear un producto.

        Args:
            tenant_id (UUID): El ID del tenant al que pertenece el producto.
            name (str): El nombre del producto.
            sku (str): El SKU (Stock Keeping Unit) del producto, debe ser único por tenant.
            price (float): El precio del producto.
            stock (int): La cantidad inicial de stock.
            category (str): La categoría del producto.

        Returns:
            Product: La entidad del producto creado.

        Raises:
            TenantNotFound: Si el tenant especificado no existe.
            DomainError: Si el SKU ya existe para el tenant o si hay otros errores de dominio.
        """
        logger.info(
            "Iniciando caso de uso CreateProduct para tenant %s con SKU %s",
            tenant_id,
            sku,
        )

        try:
            tenant = await self.tenant_repository.get_by_id(tenant_id)
            if not tenant:
                logger.warning("Tenant no encontrado con ID: %s", tenant_id)
                raise TenantNotFound(f"Tenant with id '{tenant_id}' not found.")

            existing_product = await self.product_repository.get_by_sku(
                tenant_id, sku
            )
            if existing_product:
                logger.warning(
                    "Intento de crear producto con SKU duplicado '%s' para tenant '%s'",
                    sku,
                    tenant_id,
                )
                raise DomainError(f"Product with SKU '{sku}' already exists for this tenant.")

            new_product = Product.create(
                tenant_id=tenant_id,
                name=name,
                sku=sku,
                price=price,
                stock=stock,
                category=category,
            )

            saved_product = await self.product_repository.save(new_product)

            logger.info(
                "Producto creado exitosamente con ID %s para tenant %s",
                saved_product.id,
                tenant_id,
            )

            return saved_product

        except (TenantNotFound, DomainError) as e:
            raise e
        except Exception as e:
            logger.error(
                "Error inesperado en CreateProduct para tenant %s: %s",
                tenant_id,
                e,
                exc_info=True,
            )
            raise DomainError(f"An unexpected error occurred during product creation: {e}") from e