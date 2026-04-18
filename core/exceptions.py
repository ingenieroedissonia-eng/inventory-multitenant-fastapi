"""
Modulo: exceptions
Capa: Core

Descripcion:
Define las excepciones personalizadas utilizadas en la capa de dominio de la aplicacion.
Estas excepciones permiten un manejo de errores mas granular y especifico del contexto
del negocio, desacoplando la logica de dominio de los detalles de implementacion
de capas externas.

Responsabilidades:
- Definir una excepcion base `DomainError` para todos los errores de logica de negocio.
- Definir excepciones especificas que heredan de `DomainError`, como `ProductNotFound`.

Version: 1.0.0
"""

import logging

# Configuracion del logger para este modulo
logger = logging.getLogger(__name__)

class DomainError(Exception):
    """
    Excepcion base para errores ocurridos en la capa de dominio.

    Esta es la clase padre para todas las excepciones personalizadas que representan
    violaciones de las reglas de negocio o inconsistencias en el estado del modelo
    de dominio. Capturar esta excepcion permite manejar de forma general todos los
    errores de negocio.
    """
    def __init__(self, message: str):
        """
        Inicializa la excepcion con un mensaje descriptivo.

        Args:
            message (str): El mensaje que describe el error de dominio.
        """
        super().__init__(message)
        logger.error("DomainError raised: %s", message)


class ProductNotFound(DomainError):
    """
    Excepcion especifica para cuando no se encuentra un producto.

    Se lanza cuando una operacion (como busqueda, actualizacion o eliminacion)
    intenta acceder a un producto que no existe en el sistema de persistencia.
    Hereda de `DomainError` ya que representa una condicion de error especifica
    dentro de la logica de negocio.
    """
    def __init__(self, product_id: str):
        """
        Inicializa la excepcion con un mensaje formateado.

        Args:
            product_id (str): El identificador del producto que no fue encontrado.
        """
        message = f"El producto con el ID '{product_id}' no fue encontrado."
        super().__init__(message)
        logger.warning("ProductNotFound raised for product_id: %s", product_id)