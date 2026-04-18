"""
Modulo: Dependencias de API
Capa: API

Descripcion:
Este modulo define dependencias de FastAPI que se pueden inyectar en las rutas
de la API para realizar tareas comunes, como la validación y extracción de datos
de las peticiones.

Responsabilidades:
- Extraer el X-Tenant-ID de las cabeceras de la petición.
- Validar el formato del X-Tenant-ID.
- Lanzar excepciones HTTP si la validación falla.

Version: 1.0.0
"""

import logging
import uuid
from typing import Optional

from fastapi import Header, HTTPException, status

logger = logging.getLogger(__name__)


async def get_tenant_id(
    tenant_id_header: Optional[str] = Header(None, alias="X-Tenant-ID")
) -> uuid.UUID:
    """
    Dependencia de FastAPI para extraer y validar el header X-Tenant-ID.

    Esta función se inyecta en los endpoints de la API que operan en el contexto
    de un tenant específico. Se asegura de que el header `X-Tenant-ID` esté
    presente y contenga un UUID válido.

    Args:
        tenant_id_header: El valor del header X-Tenant-ID, inyectado por FastAPI.

    Raises:
        HTTPException:
            - 400 Bad Request: Si el header X-Tenant-ID está ausente.
            - 400 Bad Request: Si el valor del header no es un UUID válido.

    Returns:
        El ID del tenant como un objeto UUID.
    """
    if tenant_id_header is None:
        detail_message = "El header X-Tenant-ID es obligatorio."
        logger.warning(detail_message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message,
        )

    try:
        tenant_uuid = uuid.UUID(tenant_id_header)
        logger.info(f"Petición validada para el tenant_id: {tenant_uuid}")
        return tenant_uuid
    except ValueError:
        detail_message = f"Formato inválido para X-Tenant-ID. '{tenant_id_header}' no es un UUID válido."
        logger.error(f"Formato de UUID inválido para X-Tenant-ID: '{tenant_id_header}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message,
        ) from None
    except TypeError:
        detail_message = "El header X-Tenant-ID debe ser una cadena de texto."
        logger.error(f"Tipo de dato inválido para X-Tenant-ID: se recibió {type(tenant_id_header)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message,
        ) from None