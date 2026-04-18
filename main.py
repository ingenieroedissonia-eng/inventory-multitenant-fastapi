import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.product_router import router as product_router
from infrastructure.in_memory_tenant_repository import InMemoryTenantRepository
from infrastructure.in_memory_product_repository import InMemoryProductRepository
from core.tenant import Tenant
from core.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    tenant_repo = InMemoryTenantRepository.get_instance()
    product_repo = InMemoryProductRepository.get_instance()

    t1 = Tenant(id='tenant-1', name='Acme Corp', plan='pro')
    t2 = Tenant(id='tenant-2', name='Globex Inc', plan='enterprise')
    tenant_repo.save(t1)
    tenant_repo.save(t2)

    p1 = Product(id='prod-1', tenant_id='tenant-1', name='Laptop', sku='LAP001', price=999.99, stock=10, category='electronics')
    p2 = Product(id='prod-2', tenant_id='tenant-1', name='Mouse', sku='MOU001', price=29.99, stock=50, category='electronics')
    p3 = Product(id='prod-3', tenant_id='tenant-1', name='Keyboard', sku='KEY001', price=79.99, stock=5, category='electronics')
    p4 = Product(id='prod-4', tenant_id='tenant-2', name='Desk', sku='DSK001', price=299.99, stock=8, category='furniture')
    p5 = Product(id='prod-5', tenant_id='tenant-2', name='Chair', sku='CHR001', price=199.99, stock=15, category='furniture')
    p6 = Product(id='prod-6', tenant_id='tenant-2', name='Monitor', sku='MON001', price=399.99, stock=3, category='electronics')

    product_repo.save(p1)
    product_repo.save(p2)
    product_repo.save(p3)
    product_repo.save(p4)
    product_repo.save(p5)
    product_repo.save(p6)

    logger.info('Mock data loaded: 2 tenants, 6 products')
    yield

app = FastAPI(
    title='Inventory Multi-tenant API',
    description='REST API for multi-tenant inventory management',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(product_router, prefix='/api/v1')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
