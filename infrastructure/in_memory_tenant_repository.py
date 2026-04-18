"""
Módulo: InMemoryTenantRepository
Capa: Infrastructure

Descripción:
Implementación en memoria del repositorio de tenants. Este repositorio simula la
persistencia de datos utilizando una estructura de datos en memoria (un diccionario)
y es útil para pruebas, desarrollo local o entornos donde no se requiere
persistencia real.

Responsabilidades:
- Implementar la interfaz `TenantRepository`.
- Gestionar el ciclo de vida de los objetos `Tenant` en memoria.
- Proveer métodos para guardar, recuperar y listar tenants.

Versión: 1.0.0
"""

import logging
import uuid
from typing import Dict, List, Optional

from core.exceptions import TenantNotFound
from core.interfaces import TenantRepository
from core.tenant import Tenant

logger = logging.getLogger(__name__)


class InMemoryTenantRepository(TenantRepository):
    """
    Implementación en memoria de la interfaz TenantRepository.

    Esta clase utiliza un diccionario para almacenar los tenants. No ofrece
    persistencia de datos entre ejecuciones de la aplicación.
    """

    def __init__(self) -> None:
        """
        Inicializa el repositorio en memoria con un diccionario vacío.
        """
        self._tenants: Dict[uuid.UUID, Tenant] = {}
        logger.info("InMemoryTenantRepository initialized.")

    async def save(self, tenant: Tenant) -> Tenant:
        """
        Guarda un nuevo tenant o actualiza uno existente en el almacenamiento en memoria.

        Args:
            tenant: El objeto Tenant a guardar.

        Returns:
            El objeto Tenant guardado.
        """
        logger.info("Saving tenant with id %s", tenant.id)
        self._tenants[tenant.id] = tenant
        logger.debug("Current tenants: %s", list(self._tenants.keys()))
        return tenant

    async def get_by_id(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        """
        Obtiene un tenant por su ID.

        Args:
            tenant_id: El UUID del tenant a buscar.

        Returns:
            El objeto Tenant si se encuentra, de lo contrario None.
        """
        logger.info("Fetching tenant by id: %s", tenant_id)
        tenant = self._tenants.get(tenant_id)
        if tenant:
            logger.debug("Tenant found: %s", tenant.name)
        else:
            logger.warning("Tenant with id %s not found.", tenant_id)
        return tenant

    async def get_by_name(self, name: str) -> Optional[Tenant]:
        """
        Obtiene un tenant por su nombre.

        Args:
            name: El nombre del tenant a buscar.

        Returns:
            El objeto Tenant si se encuentra, de lo contrario None.
        """
        logger.info("Fetching tenant by name: %s", name)
        for tenant in self._tenants.values():
            if tenant.name == name:
                logger.debug("Tenant found with name %s: id %s", name, tenant.id)
                return tenant
        logger.warning("Tenant with name '%s' not found.", name)
        return None

    async def list_all(self) -> List[Tenant]:
        """
        Lista todos los tenants almacenados.

        Returns:
            Una lista de todos los objetos Tenant.
        """
        logger.info("Listing all tenants.")
        tenants_list = list(self._tenants.values())
        logger.debug("Found %d tenants.", len(tenants_list))
        return tenants_list