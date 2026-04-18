"""
Modulo: InMemoryUserRepository
Capa: Infrastructure

Descripcion:
Implementación en memoria del repositorio de usuarios. Esta clase simula una base de datos
para la entidad User, manteniendo los datos en un diccionario en memoria.

Responsabilidades:
- Simular el almacenamiento y recuperación de entidades User.
- Proveer una implementación concreta de la interfaz UserRepository para desarrollo y pruebas.
- Contener datos mock para una experiencia de desarrollo inicial, con usuarios de diferentes roles.

Version: 1.0.0
"""

import logging
from typing import List, Optional, Dict
from uuid import UUID, uuid4

from core.entities.user import User
from core.ports