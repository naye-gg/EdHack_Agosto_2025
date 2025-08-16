# Makefile para Coach AI v2
# Facilita el manejo del entorno virtual y tareas comunes

.PHONY: help setup install clean run test lint format check verify dev-install

# Variables
PYTHON := python3.11
VENV := venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# Detectar sistema operativo
ifeq ($(OS),Windows_NT)
    VENV_BIN := $(VENV)/Scripts
    PIP := $(VENV_BIN)/pip.exe
    PYTHON_VENV := $(VENV_BIN)/python.exe
    RM := rmdir /s /q
    ACTIVATE := $(VENV_BIN)/activate.bat
else
    RM := rm -rf
    ACTIVATE := source $(VENV_BIN)/activate
endif

# Comando por defecto
help:
	@echo "🚀 Coach AI v2 - Comandos Disponibles"
	@echo "======================================"
	@echo ""
	@echo "📦 Configuración:"
	@echo "  make setup          - Configurar entorno virtual completo"
	@echo "  make install        - Solo instalar dependencias"
	@echo "  make dev-install    - Instalar dependencias de desarrollo"
	@echo ""
	@echo "🏃 Ejecución:"
	@echo "  make run           - Ejecutar aplicación"
	@echo "  make verify        - Verificar instalación"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean         - Limpiar entorno virtual"
	@echo "  make clean-cache   - Limpiar cache de Python"
	@echo ""
	@echo "🔧 Desarrollo:"
	@echo "  make test          - Ejecutar tests"
	@echo "  make lint          - Verificar código con flake8"
	@echo "  make format        - Formatear código con black"
	@echo "  make check         - Verificar código (lint + format)"
	@echo ""
	@echo "💡 Uso rápido:"
	@echo "  make setup && make run"

# Crear entorno virtual e instalar dependencias
setup: clean
	@echo "🔧 Configurando entorno virtual..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip wheel
	$(PIP) install -r requirements.txt
	@echo "✅ Entorno virtual configurado correctamente"
	@echo ""
	@echo "Para activar manualmente:"
ifeq ($(OS),Windows_NT)
	@echo "  $(VENV)\Scripts\activate"
else
	@echo "  source $(VENV)/bin/activate"
endif

# Solo instalar dependencias (si ya existe el entorno)
install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "📦 Instalando dependencias..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

# Instalar dependencias de desarrollo
dev-install: install
	@echo "🛠️  Instalando dependencias de desarrollo..."
	$(PIP) install -r requirements-dev.txt
	@echo "✅ Dependencias de desarrollo instaladas"

# Ejecutar aplicación
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "🚀 Iniciando Coach AI v2..."
	@echo "🌐 Abriendo en http://localhost:8501"
	$(PYTHON_VENV) -m streamlit run app.py --server.port 8501

# Verificar instalación
verify:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "🔍 Verificando instalación..."
	$(PYTHON_VENV) verify_installation.py

# Ejecutar tests
test:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "🧪 Ejecutando tests..."
	$(PYTHON_VENV) -m pytest tests/ -v

# Verificar código con linter
lint:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "🔍 Verificando código con flake8..."
	$(PYTHON_VENV) -m flake8 . --extend-ignore=E501,W503 --exclude=venv

# Formatear código
format:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Entorno virtual no encontrado. Ejecuta 'make setup' primero"; \
		exit 1; \
	fi
	@echo "🎨 Formateando código con black..."
	$(PYTHON_VENV) -m black . --exclude=venv
	$(PYTHON_VENV) -m isort . --skip=venv

# Verificar código completo
check: lint format
	@echo "✅ Verificación de código completada"

# Limpiar entorno virtual
clean:
	@echo "🧹 Limpiando entorno virtual..."
	$(RM) $(VENV) 2>/dev/null || true
	@echo "✅ Entorno virtual eliminado"

# Limpiar cache de Python
clean-cache:
	@echo "🧹 Limpiando cache de Python..."
	find . -type d -name "__pycache__" -exec $(RM) {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cache limpiado"

# Mostrar información del entorno
info:
	@echo "📊 Información del Entorno"
	@echo "=========================="
	@echo "Sistema: $(shell uname -s 2>/dev/null || echo Windows)"
	@echo "Python: $(shell $(PYTHON) --version 2>/dev/null || echo 'No encontrado')"
	@if [ -d "$(VENV)" ]; then \
		echo "Entorno virtual: ✅ Configurado"; \
		echo "Ubicación: $(VENV)"; \
		echo "Pip: $(shell $(PIP) --version 2>/dev/null || echo 'No encontrado')"; \
	else \
		echo "Entorno virtual: ❌ No configurado"; \
	fi

# Backup de configuración
backup:
	@echo "💾 Creando backup de configuración..."
	tar -czf coach-ai-backup-$(shell date +%Y%m%d_%H%M%S).tar.gz \
		--exclude=venv \
		--exclude=__pycache__ \
		--exclude=*.pyc \
		--exclude=data/students \
		.
	@echo "✅ Backup creado"

# Instalación rápida para desarrollo
dev-setup: setup dev-install
	@echo "🎉 Entorno de desarrollo configurado completamente"
