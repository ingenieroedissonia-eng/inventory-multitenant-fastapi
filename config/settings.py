"""
Modulo: Settings
Capa: Config

Descripcion:
Configuracion centralizada de la aplicacion. Carga y valida las variables
de entorno necesarias para el funcionamiento del sistema.

Responsabilidades:
- Cargar variables de entorno utilizando pydantic-settings.
- Validar que las variables criticas esten presentes.
- Exponer una instancia de configuracion tipada para ser usada en toda la aplicacion.

Version: 1.0.0
"""

import logging
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Configurar el logger para este modulo
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Clase que gestiona la configuracion de la aplicacion.

    Carga automaticamente las variables desde un archivo .env o desde el entorno
    del sistema. Proporciona validacion y tipado estatico.
    """

    # Configuracion de pydantic-settings
    # Lee desde un archivo .env si existe.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

    # Configuracion de JWT
    # Clave secreta para firmar los tokens JWT. Es critica y no tiene valor por defecto.
    # Esta variable DEBE ser proporcionada en el entorno.
    JWT_SECRET: str

    # Algoritmo de firma para los tokens JWT.
    JWT_ALGORITHM: str = "HS256"

    # Tiempo de expiracion del token de acceso en minutos.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Configuracion de Logging
    # Nivel de logging para la aplicacion (e.g., DEBUG, INFO, WARNING, ERROR).
    LOG_LEVEL: str = "INFO"

    # Configuracion de la aplicacion
    # Nombre del proyecto para documentacion y metadatos.
    PROJECT_NAME: str = "Auth Service API"

    # Version de la API para documentacion y gestion de clientes.
    API_VERSION: str = "v1"

    # Prefijo global para todas las rutas de la API.
    API_PREFIX: str = "/api/v1"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia unica (singleton) de la configuracion.

    Utiliza lru_cache para asegurar que la clase Settings se instancie una sola vez,
    evitando la sobrecarga de leer las variables de entorno multiples veces.
    Esto mejora el rendimiento y asegura consistencia en la configuracion.

    Returns:
        Settings: Una instancia de la clase de configuracion.
    """
    logger.info("Cargando la configuracion de la aplicacion...")
    try:
        settings_instance = Settings()
        # Configura el nivel de logging root basado en la variable de entorno
        logging.basicConfig(level=settings_instance.LOG_LEVEL.upper())
        logger.info("Configuracion cargada y logging configurado.")
        return settings_instance
    except ValueError as e:
        logger.critical(f"Error critico al cargar la configuracion. Variables de entorno faltantes o invalidas: {e}")
        raise SystemExit(f"Error de configuracion: {e}") from e

# Instancia global para ser importada por otros modulos.
# El uso de get_settings() asegura que la configuracion se carga de forma lazy
# y una sola vez.
settings = get_settings()