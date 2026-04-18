"""
Modulo: Tenant
Capa: Core

Descripcion:
Define la entidad de dominio 'Tenant', que representa a un inquilino o cliente en el sistema.

Responsabilidades:
- Definir la estructura de datos para un Tenant.
- Contener las reglas de negocio y validaciones inherentes a un Tenant.
- Asegurar la integridad de los datos de la entidad.

Version: 1.0.0
"""
import logging
import uuid
from dataclasses import dataclass, field
from typing import Literal, get_args

from core.exceptions import DomainError

logger = logging.getLogger(__name__)

# Define los tipos de planes permitidos para un inquilino.
# Esto mejora la seguridad de tipos y la validación.
TenantPlan = Literal["free", "basic", "premium"]


@dataclass(frozen=True)
class Tenant:
    """
    Entidad que representa a un inquilino del sistema.

    Esta clase es inmutable (frozen=True) para garantizar la consistencia de la entidad
    una vez creada. Las modificaciones deben realizarse a través de casos de uso
    que generen una nueva instancia de la entidad, promoviendo un estado predecible.

    Attributes:
        id (str): Identificador único del inquilino (UUID). Se genera automáticamente si no se provee.
        name (str): Nombre comercial o identificativo del inquilino.
        plan (TenantPlan): El plan de suscripción actual del inquilino.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), kw_only=True)
    name: str
    plan: TenantPlan

    def __post_init__(self):
        """
        Realiza validaciones de negocio después de la inicialización del objeto.
        Este método es invocado automáticamente por la dataclass.
        """
        try:
            self._validate_name()
            self._validate_plan()
            logger.debug(f"Tenant entity created or validated successfully: id={self.id}")
        except DomainError as e:
            logger.error(f"Failed to create Tenant entity. Error: {e}")
            raise

    def _validate_name(self):
        """
        Valida que el nombre del inquilino sea una cadena de texto no vacía.
        """
        if not self.name or not isinstance(self.name, str) or not self.name.strip():
            raise DomainError("Tenant name cannot be empty or just whitespace.")

    def _validate_plan(self):
        """
        Valida que el plan del inquilino sea uno de los valores permitidos en TenantPlan.
        """
        allowed_plans = get_args(TenantPlan)
        if self.plan not in allowed_plans:
            raise DomainError(f"Invalid tenant plan '{self.plan}'. Must be one of {allowed_plans}.")

    def change_plan(self, new_plan: TenantPlan) -> "Tenant":
        """
        Crea una nueva instancia de Tenant con un plan actualizado.

        Este método sigue el principio de inmutabilidad. En lugar de modificar
        el estado del objeto actual, devuelve un nuevo objeto con el estado actualizado.

        Args:
            new_plan: El nuevo plan para el inquilino. Debe ser un valor válido de TenantPlan.

        Returns:
            Una nueva instancia de Tenant con el plan modificado.

        Raises:
            DomainError: Si el nuevo plan no es válido.
        """
        if new_plan not in get_args(TenantPlan):
            raise DomainError(f"Cannot change to invalid plan '{new_plan}'.")

        if new_plan == self.plan:
            logger.warning(f"Tenant {self.id} already has plan '{new_plan}'. No change made.")
            return self

        logger.info(f"Changing plan for tenant {self.id} from '{self.plan}' to '{new_plan}'.")
        return Tenant(id=self.id, name=self.name, plan=new_plan)