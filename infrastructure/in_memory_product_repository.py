"""
Modulo: in_memory_product_repository
Capa: Infrastructure

Descripcion:
Implementacion en memoria del repositorio de productos.
Este repositorio simula una base de datos para productos utilizando un diccionario en memoria
y se inicializa con datos de prueba (mock) para dos inquilinos (tenants).

Responsabilidades:
- Almacenar y gestionar entidades de Producto en memoria.
- Proveer una implementacion concreta de la interfaz ProductRepository.
- Cargar datos de prueba para demostracion y desarrollo.

Version: 1.0.0
"""

import logging
import uuid
from typing import Dict, List, Optional
from uuid import UUID

from core.exceptions import ProductNotFound
from core.interfaces import ProductRepository
from core.product import Product

logger = logging.getLogger(__name__)

class InMemoryProductRepository(ProductRepository):
    """
    Implementación en memoria de ProductRepository.
    """

    def __init__(self) -> None:
        """
        Inicializa el repositorio y carga los datos de prueba.
        """
        self._products: Dict[UUID, Product] = {}
        self._load_mock_data()
        logger.info("InMemoryProductRepository inicializado con %d productos.", len(self._products))

    def _load_mock_data(self) -> None:
        """
        Carga un conjunto de productos de prueba para dos tenants diferentes.
        """
        tenant_1_id = uuid.uuid4()
        tenant_2_id = uuid.uuid4()

        mock_products = [
            Product(id=uuid.uuid4(), tenant_id=tenant_1_id, name="Laptop Pro", sku="LP-001", price=1200.00, stock=50, category="Electronics"),
            Product(id=uuid.uuid4(), tenant_id=tenant_1_id, name="Wireless Mouse", sku="WM-002", price=25.50, stock=200, category="Accessories"),
            Product(id=uuid.uuid4(), tenant_id=tenant_1_id, name="4K Monitor", sku="4K-003", price=450.00, stock=30, category="Electronics"),
            Product(id=uuid.uuid4(), tenant_id=tenant_2_id, name="Organic Coffee Beans", sku="OCB-A1", price=18.99, stock=150, category="Groceries"),
            Product(id=uuid.uuid4(), tenant_id=tenant_2_id, name="Gourmet Chocolate Bar", sku="GCB-B2", price=5.75, stock=300, category="Groceries"),
            Product(id=uuid.uuid4(), tenant_id=tenant_2_id, name="Artisan Bread", sku="AB-C3", price=4.50, stock=80, category="Bakery"),
        ]

        for product in mock_products:
            self._products[product.id] = product

        logger.info("Datos de prueba cargados para 2 tenants.")

    async def save(self, product: Product) -> Product:
        """
        Guarda un nuevo producto en el repositorio. Si ya existe, lo actualiza.
        """
        if not isinstance(product, Product):
            raise TypeError("El objeto a guardar debe ser una instancia de Product.")
        
        logger.info("Guardando producto con ID %s para tenant %s", product.id, product.tenant_id)
        self._products[product.id] = product
        return product

    async def update(self, product: Product) -> Product:
        """
        Actualiza un producto existente en el repositorio.
        """
        if product.id not in self._products:
            logger.warning("Intento de actualizar producto no existente con ID %s", product.id)
            raise ProductNotFound(f"Producto con ID {product.id} no encontrado.")
        
        logger.info("Actualizando producto con ID %s", product.id)
        self._products[product.id] = product
        return product

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Obtiene un producto por su ID.
        """
        logger.debug("Buscando producto con ID %s", product_id)
        return self._products.get(product_id)

    async def get_by_sku(self, tenant_id: UUID, sku: str) -> Optional[Product]:
        """
        Obtiene un producto por su SKU dentro de un tenant específico.
        """
        logger.debug("Buscando producto con SKU %s para tenant %s", sku, tenant_id)
        for product in self._products.values():
            if product.tenant_id == tenant_id and product.sku == sku:
                return product
        return None

    async def list_by_tenant(self, tenant_id: UUID) -> List[Product]:
        """
        Lista todos los productos pertenecientes a un tenant.
        """
        logger.debug("Listando productos para el tenant %s", tenant_id)
        return [
            product for product in self._products.values()
            if product.tenant_id == tenant_id
        ]