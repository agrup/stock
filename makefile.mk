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
	@echo "🧪 Running tests..."
	@$(COMPOSE) --env-file .env.test --profile emulators up -d
	@echo "⏳ Waiting for service to be ready..."
	@bash -c ' \
		for i in $$(seq 1 10); do \
			if $$(docker compose --env-file .env.test logs $(SERVICE) 2>&1 | grep -q "Application startup complete."); then \
				echo "✅ Service is ready!"; \
				exit 0; \
			fi; \
			sleep 1; \
		done; \
		echo "🚨 Service failed to start after 30 seconds. Logs:"; \
		docker compose --env-file .env.test logs $(SERVICE); \
		exit 1; \
	'
	@$(COMPOSE) --env-file .env.test exec -e PYTHONPATH=/app $(SERVICE) pytest -vv; EXIT_CODE=$$?
	@echo "🛑 Stopping test containers..."
	@$(COMPOSE) --env-file .env.test --profile emulators down > /dev/null 2>&1
	@exit $$EXIT_CODE

## ───── Comandos de Calidad de Código ─────

# Aplica black (formatea código)
format:
	$(COMPOSE) run --rm $(SERVICE) black src/ tests/

# Revisión de código con flake8
lint:
	$(COMPOSE) run --rm $(SERVICE) flake8 src/ tests/

typecheck:
	$(COMPOSE) run --rm $(SERVICE) mypy src/

scan:
	$(COMPOSE) run --rm $(SERVICE) bandit -r src/

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
	$(COMPOSE) --env-file $(ENV_FILE) exec -u $$(id -u):$$(id -g) -e PYTHONPATH=/app $(SERVICE) \
	alembic revision --autogenerate -m "$(msg)"

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
