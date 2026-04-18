"""
Modulo: Settings
Capa: Infrastructure (Config)

Descripcion:
Configuracion centralizada del sistema utilizando variables de entorno.
Este modulo utiliza Pydantic's BaseSettings para cargar, validar y
tipar la configuracion desde el entorno o un archivo .env.

Responsabilidades:
- Cargar variables de entorno de forma segura.
- Validar la presencia y el tipo de las configuraciones criticas.
- Exponer un objeto de configuracion tipado y unico para toda la aplicacion.

Version: 1.0.0
"""

import logging
import os
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configurar un logger para el modulo de settings
logger = logging.getLogger(__name__)

# Determinar la ruta base del proyecto para la carga de archivos de entorno
# Se asume que este archivo esta en config/settings.py, por lo que subimos dos niveles
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """
    Clase que gestiona la configuracion de la aplicacion.
    Carga automaticamente las variables desde un archivo .env y el entorno del sistema.
    La precedencia es: variables de entorno del sistema > variables en .env.
    """

    # Configuracion del modelo Pydantic
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Ignorar variables de entorno extra que no esten definidas aqui
    )

    # Configuracion del proyecto
    PROJECT_NAME: str = Field(
        default="Inventory Management System",
        description="Nombre del proyecto.",
    )
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Entorno de ejecucion de la aplicacion.",
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nivel de logging para la aplicacion.",
    )

    # Configuracion de la base de datos
    DATABASE_URL: str = Field(
        ...,  # '...' indica que es un campo requerido sin default
        description="URL de conexion a la base de datos (e.g., 'mongodb://user:pass@host:port/db').",
    )

    # Configuracion de la API
    API_V1_STR: str = Field(
        default="/api/v1",
        description="Prefijo para la version 1 de la API.",
    )

    # Secret key para JWT u otras operaciones criptograficas
    SECRET_KEY: str = Field(
        ...,
        description="Clave secreta para operaciones de seguridad como la firma de JWTs.",
    )


try:
    settings = Settings()
    logger.info("Configuration loaded successfully for environment: %s", settings.ENVIRONMENT)
except Exception as e:
    logger.critical("Failed to load application settings: %s", e, exc_info=True)
    # En un escenario real, esto deberia detener el arranque de la aplicacion
    raise RuntimeError(f"Could not load settings: {e}") from e