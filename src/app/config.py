import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env (solo para desarrollo local)
load_dotenv()

# Configuración de entorno
ENV = os.getenv("ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


def get_database_url() -> str:
    """Obtiene la URL de la base de datos directamente desde las variables de entorno."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("La variable de entorno DATABASE_URL no está configurada.")
    return db_url
