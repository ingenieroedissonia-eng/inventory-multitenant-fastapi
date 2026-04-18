"""
Modulo: product_router
Capa: API

Descripcion:
Router de FastAPI para gestionar las operaciones relacionadas con productos,
específicamente la actualización de stock.

Responsabilidades:
- Exponer el endpoint PUT /products/{id}/stock.
- Validar los datos de entrada de las solicitudes HTTP usando Pydantic.
- Orquestar la ejecución del caso de uso UpdateStock.
- Traducir las excepciones del dominio a respuestas HTTP apropiadas.
- Formatear la respuesta HTTP en caso de éxito.

Version: 1.0.0
"""

import logging
from typing import TypeAlias

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from core.exceptions import DomainError, ProductNotFound
from core.use_cases.update_stock import UpdateStock
from infrastructure.product_repository import ProductRepositorySingleton

logger = logging.getLogger(__name__)

ProductId: TypeAlias = str | int
StockLevel: TypeAlias = int

class UpdateStockRequestModelModel(BaseModel):
    """Modelo de datos para la solicitud de actualización de stock."""
    stock_level: StockLevel = Field(..., ge=0, description="Nuevo nivel de stock para el producto. No puede ser negativo.")

class UpdateStockResponseModelModel(BaseModel):
    """Modelo de datos para la respuesta de actualización de stock."""
    product_id: ProductId
    stock_level: StockLevel

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)

def get_update_stock_use_case() -> UpdateStock:
    """
    Crea y devuelve una instancia del caso de uso para actualizar stock,
    inyectando el repositorio de productos como dependencia.
    Este enfoque facilita las pruebas al permitir el mockeo de dependencias.
    """
    product_repository = ProductRepositorySingleton.get_instance()
    return UpdateStock(product_repository=product_repository)

@router.put(
    "/{product_id}/stock",
    response_model=UpdateStockResponseModelModel,
    status_code=status.HTTP_200_OK,
    summary="Actualizar stock de un producto",
    description="Actualiza el nivel de stock de un producto específico por su ID."
)
def update_product_stock(
    product_id: ProductId,
    request: UpdateStockRequestModelModel,
    use_case: UpdateStock = Depends(get_update_stock_use_case)
) -> UpdateStockResponseModelModel:
    try:
        logger.info(f'Actualizando stock para producto {product_id}')
        result = use_case.execute(product_id=str(product_id), new_stock=request.stock_level)
        return UpdateStockResponseModelModel(product_id=result.id, stock_level=result.stock)
    except ProductNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(f'Error inesperado actualizando stock: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error interno')


from uuid import UUID
from fastapi import Header
from core.use_cases.create_product import CreateProduct
from core.use_cases.get_inventory_report import GetInventoryReport
from infrastructure.in_memory_tenant_repository import InMemoryTenantRepository
from infrastructure.in_memory_product_repository import InMemoryProductRepository

class CreateProductRequest(BaseModel):
    name: str
    sku: str
    price: float
    stock: int = 0
    category: str

def get_create_use_case() -> CreateProduct:
    return CreateProduct(product_repository=InMemoryProductRepository.get_instance(), tenant_repository=InMemoryTenantRepository.get_instance())

def get_report_use_case() -> GetInventoryReport:
    return GetInventoryReport(product_repository=InMemoryProductRepository.get_instance(), tenant_repository=InMemoryTenantRepository.get_instance())

@router.post('/', status_code=status.HTTP_201_CREATED, summary='Crear producto')
async def create_product(request: CreateProductRequest, tenant_id: str = Header(..., alias='X-Tenant-ID'), use_case: CreateProduct = Depends(get_create_use_case)):
    try:
        product = await use_case.execute(tenant_id=tenant_id, name=request.name, sku=request.sku, price=request.price, stock=request.stock, category=request.category)
        return product
    except TenantNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/', summary='Listar productos')
async def get_products(tenant_id: str = Header(..., alias='X-Tenant-ID')):
    products = await InMemoryProductRepository.get_instance().list_by_tenant(tenant_id)
    return products

@router.get('/reports/inventory', summary='Reporte inventario')
async def get_inventory_report(tenant_id: str = Header(..., alias='X-Tenant-ID'), threshold: int = 10, use_case: GetInventoryReport = Depends(get_report_use_case)):
    try:
        products = await use_case.execute(tenant_id=tenant_id, low_stock_threshold=threshold)
        return products
    except TenantNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))