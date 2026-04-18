"""
Modulo: API Router for Authentication
Capa: Presentation (API)

Descripcion:
Define los endpoints de la API para registro, login, y gestión de sesión de usuario.

Responsabilidades:
- Exponer el endpoint POST /auth/register para crear nuevos usuarios.
- Exponer el endpoint POST /auth/login para autenticar usuarios y obtener un token JWT.
- Exponer el endpoint GET /auth/me para obtener la información del usuario autenticado.
- Exponer el endpoint GET /auth/check-permission para verificar los permisos de un usuario.

Version: 1.1.0
"""

import logging
from typing import Annotated, Dict

from fastapi import APIRouter