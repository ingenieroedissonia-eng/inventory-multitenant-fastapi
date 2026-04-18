import logging

logger = logging.getLogger(__name__)

class DomainError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error('DomainError: %s', message)

class TenantNotFound(DomainError):
    def __init__(self, tenant_id: str):
        super().__init__(f'Tenant con ID {tenant_id} no encontrado.')

class ProductNotFound(DomainError):
    def __init__(self, product_id: str):
        super().__init__(f'Producto con ID {product_id} no encontrado.')

class InvalidSKU(DomainError):
    def __init__(self, sku: str):
        super().__init__(f'SKU {sku} ya existe en este tenant.')
