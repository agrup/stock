# Etapa 1: "prod-builder" - Instala solo las dependencias de producción
FROM python:3.11-slim as prod-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./

# Instalamos dependencias de producción
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Etapa 2: "dev" - Para desarrollo local (usada en docker-compose)
# Hereda de la etapa anterior y añade las dependencias de desarrollo.
FROM prod-builder as dev

COPY requirements_dev.txt ./
RUN pip install --no-cache-dir -r requirements_dev.txt

# El comando se define en docker-compose.yaml para incluir --reload.


# Etapa 3: "final" - Imagen de producción optimizada y segura
FROM python:3.11-slim as final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Crear un usuario no-root para mejorar la seguridad en producción
RUN adduser --system --group appuser

# Copiar las dependencias de producción desde la etapa "prod-builder"
COPY --from=prod-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=prod-builder /usr/local/bin /usr/local/bin

# Copiar el código fuente de la aplicación
COPY ./src ./src
# COPY ./alembic.ini ./alembic.ini # Descomentar si se usa una DB SQL en producción
# COPY ./alembic ./alembic         # Descomentar si se usa una DB SQL en producción

# Asignar permisos al usuario no-root y cambiar de usuario
RUN chown -R appuser:appuser /app
USER appuser


CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
