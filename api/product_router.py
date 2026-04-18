# File: api/product_router.py
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from core.exceptions import DomainError, ProductNotFound, TenantNotFound
from core.use_cases.update_stock import UpdateStock
from core.use_cases.create_product import CreateProduct
from core.use_cases.get_inventory_report import GetInventoryReport
from infrastructure.in_memory_product_repository import InMemoryProductRepository
from infrastructure.in_memory_tenant_repository import InMemoryTenantRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/products', tags=['Products'])

class UpdateStockRequestModel(BaseModel):
    stock_level: int = Field(..., ge=0)

class UpdateStockResponseModel(BaseModel):
    product_id: str
    stock_level: int

class CreateProductRequest(BaseModel):
    name: str
    sku: str
    price: float
    stock: int = 0
    category: str

def get_update_stock_use_case() -> UpdateStock:
    return UpdateStock(product_repository=InMemoryProductRepository.get_instance())

def get_create_use_case() -> CreateProduct:
    return CreateProduct(product_repository=InMemoryProductRepository.get_instance(), tenant_repository=InMemoryTenantRepository.get_instance())

def get_report_use_case() -> GetInventoryReport:
    return GetInventoryReport(product_repository=InMemoryProductRepository.get_instance(), tenant_repository=InMemoryTenantRepository.get_instance())

@router.put('/{product_id}/stock', status_code=status.HTTP_200_OK, summary='Actualizar stock de un producto')
async def update_product_stock(product_id: str, request: UpdateStockRequestModel, use_case: UpdateStock = Depends(get_update_stock_use_case)) -> UpdateStockResponseModel:
    try:
        result = await use_case.execute(product_id=product_id, new_stock=request.stock_level)
        return UpdateStockResponseModel(product_id=result.id, stock_level=result.stock)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))

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