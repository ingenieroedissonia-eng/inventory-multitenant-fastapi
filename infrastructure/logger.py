"""
Modulo: Logger
Capa: Infrastructure

Descripcion:
Configuracion del sistema de logging estructurado en formato JSON.

Responsabilidades:
- Definir un formateador de logs en JSON.
- Configurar el logger raiz de la aplicacion.
- Proveer una funcion para inicializar el logging.

Version: 1.0.0
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from config.settings import Settings


class CustomJsonEncoder(json.JSONEncoder):
    """
    Codificador JSON personalizado para manejar tipos de datos no serializables.
    """
    def default(self, obj: Any) -> Any:
        """
        Sobrescribe el metodo default para manejar tipos especificos.

        Args:
            obj: El objeto a serializar.

        Returns:
            Una representacion serializable del objeto.
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class StructuredJsonFormatter(logging.Formatter):
    """
    Formateador de logs que convierte los registros en cadenas JSON estructuradas.
    """
    def __init__(self, service_name: str):
        """
        Inicializa el formateador con el nombre del servicio.

        Args:
            service_name: El nombre del servicio que se incluira en cada log.
        """
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea el registro de log en una cadena JSON.

        Args:
            record: El objeto LogRecord a formatear.

        Returns:
            Una cadena de texto en formato JSON representando el log.
        """
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "service": self.service_name,
            "message": record.getMessage(),
            "logger": record.name,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
            log_record.update(record.extra_data)

        return json.dumps(log_record, cls=CustomJsonEncoder)


def setup_logging(settings: Settings):
    """
    Configura el logging raiz para la aplicacion.

    Utiliza un manejador de stream para enviar logs a la salida estandar
    y un formateador JSON para estructurar los mensajes.

    Args:
        settings: La configuracion de la aplicacion.
    """
    try:
        root_logger = logging.getLogger()
        root_logger.setLevel(settings.LOG_LEVEL.upper())

        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        handler = logging.StreamHandler(sys.stdout)
        formatter = StructuredJsonFormatter(service_name=settings.SERVICE_NAME)
        handler.setFormatter(formatter)

        root_logger.addHandler(handler)
        
        initial_log = logging.getLogger(__name__)
        initial_log.info(
            "Logging configurado exitosamente",
            extra={'extra_data': {
                'log_level': settings.LOG_LEVEL,
                'service_name': settings.SERVICE_NAME
            }}
        )

    except (IOError, ValueError) as e:
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"Error critico al configurar el logger: {e}", exc_info=True)
        raise SystemExit(f"No se pudo inicializar el logger: {e}") from e