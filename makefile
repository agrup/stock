# Makefile para FastAPI + Docker + Clean Architecture

# Configuración
COMPOSE ?= docker compose
SERVICE ?= fastapi-app
ENV_FILE ?= .env
PROFILES ?=

# .PHONY declara targets que no son archivos. Es una buena práctica.
.PHONY: up build down restart logs shell test format lint typecheck scan check makemigration migrate history current downgrade show-migrations migratestamp help

.DEFAULT_GOAL := help

## ───── Comandos de Docker ─────

# Levanta los contenedores por defecto (sin perfiles)
up:
	$(COMPOSE) --env-file $(ENV_FILE) $(if $(PROFILES),--profile $(PROFILES),) up

# Levanta todos los servicios, incluyendo los perfiles opcionales
up-full: ## Levanta todos los servicios (app + emuladores)
	$(MAKE) PROFILES=emulators up

build: up
	$(COMPOSE) build

# Detiene el contenedor
down:
	$(COMPOSE) $(if $(PROFILES),--profile $(PROFILES),) down

# Reinicia limpio
restart:
	$(MAKE) down && $(MAKE) up --build

# Logs en vivo
logs:
	$(COMPOSE) logs -f $(SERVICE)

# Shell en contenedor
shell:
	$(COMPOSE) exec $(SERVICE) /bin/sh

## ───── Comandos de Test ─────
# Corre los tests con pytest dentro del contenedor de desarrollo
test:
	$(MAKE) PROFILES=emulators up -d && $(COMPOSE) exec -e ENV_FILE=.env.test $(SERVICE) pytest -vv && $(MAKE) PROFILES=emulators down

## ───── Comandos de Calidad de Código ─────

# Aplica black (formatea código)
format:
	$(COMPOSE) exec $(SERVICE) black src/ tests/

# Revisión de código con flake8
lint:
	$(COMPOSE) exec $(SERVICE) flake8 src/ tests/

typecheck:
	$(COMPOSE) exec $(SERVICE) mypy src/

scan:
	$(COMPOSE) exec $(SERVICE) bandit -r src/	

bash:
	$(COMPOSE) exec $(SERVICE) bash

# Corre todo: formateo, lint y tests
check:
	@echo "Running format..." && $(MAKE) format
	@echo "Running lint..." && $(MAKE) lint
	@echo "Running typecheck..." && $(MAKE) typecheck
	@echo "Running security scan..." && $(MAKE) scan
	@echo "Running tests..." && $(MAKE) test

# Ejecuta migraciones de Alembic (si usás)
makemigration:
	@if [ -z "$(msg)" ]; then \
		echo "Falta el mensaje: make makemigration msg='mensaje'"; exit 1; \
	fi; \
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic revision --autogenerate -m "$(msg)" && \
	sudo chown -R $(shell id -u):$(shell id -g) alembic/versions/

# Migración en producción (usa .env.production por defecto)
migrate:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic upgrade head

# Lista el historial de migraciones aplicadas
history:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic history

# Muestra el estado actual de la base respecto a las migraciones
current:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic current

# Revierte la última migración
downgrade:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic downgrade -1

# Ejecuta migraciones sin aplicar (simulación)
show-migrations:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic upgrade --sql head

migratestamp:
	$(COMPOSE) --env-file $(ENV_FILE) exec -e PYTHONPATH=/app $(SERVICE) alembic stamp head

## ───── Ayuda ─────

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
