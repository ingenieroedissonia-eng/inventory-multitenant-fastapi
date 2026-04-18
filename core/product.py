from dataclasses import dataclass, field, replace
import uuid
from core.exceptions import DomainError

@dataclass(frozen=True)
class Product:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = field(default='')
    name: str = field(default='')
    sku: str = field(default='')
    price: float = field(default=0.0)
    stock: int = field(default=0)
    category: str = field(default='')

    def __post_init__(self):
        if self.stock < 0:
            raise DomainError('Stock no puede ser negativo')
        if self.price < 0:
            raise DomainError('Precio no puede ser negativo')

    def update_stock(self, new_stock: int):
        if new_stock < 0:
            raise DomainError('Stock no puede ser negativo')
        return replace(self, stock=new_stock)
