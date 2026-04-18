"""
Modulo: Product
Capa: Core (Entidades)

Descripcion:
Define la entidad de dominio `Product`, que representa un producto en el sistema.
Contiene la logica de negocio y las validaciones inherentes al producto.

Responsabilidades:
- Definir la estructura de datos de un producto.
- Validar la consistencia de los datos (e.g., stock no negativo).
- Proveer metodos para la creacion y manipulacion segura del estado del producto.

Version: 1.0.0
"""

import logging
import uuid
from dataclasses import dataclass, field, replace

from core.exceptions import DomainError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Product:
    """
    Entidad que representa un producto en el inventario.

    Es un objeto de valor inmutable. Cualquier cambio en el estado
    (como actualizar el stock) debe resultar en una nueva instancia.

    Attributes:
        id (str): Identificador unico del producto.
        stock (int): Cantidad de unidades disponibles del producto.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    stock: int = field(default=0)

    def __post_init__(self):
        """
        Realiza validaciones despues de la inicializacion del objeto.
        """
        self._validate_stock()
        self._validate_id()
        logger.debug("Product instance created/validated: id=%s", self.id)

    def _validate_stock(self):
        """Valida que el stock no sea un numero negativo."""
        if self.stock < 0:
            msg = f"Stock no puede ser negativo. Valor recibido: {self.stock}"
            logger.error(msg)
            raise DomainError(msg)

    def _validate_id(self):
        """Valida que el ID no sea una cadena vacia."""
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            msg = "El ID del producto no puede ser nulo o vacio."
            logger.error(msg)
            raise DomainError(msg)

    def update_stock(self, new_stock: int) -> 'Product':
        """
        Crea una nueva instancia de Product con el stock actualizado.

        Args:
            new_stock (int): El nuevo valor para el stock.

        Returns:
            Product: Una nueva instancia de Product con el stock modificado.

        Raises:
            DomainError: Si el nuevo stock es negativo.
        """
        if new_stock < 0:
            msg = f"El nuevo stock no puede ser negativo. Valor: {new_stock}"
            logger.warning("Intento de actualizar stock a valor negativo para producto %s", self.id)
            raise DomainError(msg)

        logger.info("Stock actualizado para producto %s: de %d a %d", self.id, self.stock, new_stock)
        return replace(self, stock=new_stock)

    @classmethod
    def create(cls, initial_stock: int = 0) -> 'Product':
        """
        Metodo de fabrica para crear una nueva instancia de Product.

        Genera un ID unico y establece un stock inicial.

        Args:
            initial_stock (int): El stock inicial del producto. Por defecto es 0.

        Returns:
            Product: Una nueva instancia de la clase Product.
        """
        product_id = str(uuid.uuid4())
        logger.info("Creando nuevo producto con ID: %s y stock inicial: %d", product_id, initial_stock)
        return cls(id=product_id, stock=initial_stock)