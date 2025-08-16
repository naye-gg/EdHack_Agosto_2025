@echo off
REM Script de configuración completa para Windows - Coach AI v2
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo    Coach AI v2 - Configuracion Windows
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo Por favor instala Python 3.11 o 3.12 desde:
    echo https://python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH"
    pause
    exit /b 1
)

REM Mostrar versión de Python
echo 🐍 Verificando Python...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detectado

REM Verificar si es una versión compatible
python -c "import sys; exit(0 if sys.version_info >= (3,11) and sys.version_info < (3,14) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Advertencia: Se recomienda Python 3.11 o 3.12
    echo Python 3.13+ puede tener problemas con MediaPipe
    echo.
    set /p CONTINUE="¿Continuar de todos modos? (s/N): "
    if /i not "!CONTINUE!" == "s" (
        echo Instalación cancelada
        pause
        exit /b 1
    )
)

REM Verificar si ya existe entorno virtual
if exist "venv\" (
    echo 📁 Entorno virtual encontrado
    set /p RECREATE="¿Recrear entorno virtual? (s/N): "
    if /i "!RECREATE!" == "s" (
        echo 🗑️ Eliminando entorno virtual existente...
        rmdir /s /q venv
    )
)

REM Crear entorno virtual
if not exist "venv\" (
    echo 🔧 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
)

REM Activar entorno virtual y actualizar pip
echo 📦 Configurando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip wheel

REM Instalar dependencias según versión de Python
python -c "import sys; exit(0 if sys.version_info < (3,13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias para Python 3.13+ (funcionalidad limitada)...
    pip install -r requirements-python313.txt
) else (
    echo 📦 Instalando dependencias completas...
    pip install -r requirements.txt
)

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    echo.
    echo Soluciones:
    echo 1. Verificar conexión a internet
    echo 2. Ejecutar como administrador
    echo 3. Instalar Visual Studio Build Tools si es necesario
    pause
    exit /b 1
)

REM Crear directorios necesarios
echo 📁 Creando directorios...
if not exist "data\students" mkdir "data\students"
if not exist "auth" mkdir "auth"
if not exist "reports" mkdir "reports"
if not exist "logs" mkdir "logs"
if not exist "backups" mkdir "backups"

REM Verificar instalación
echo 🔍 Verificando instalación...
python verify_installation.py
if errorlevel 1 (
    echo ⚠️ Advertencia: Algunos componentes pueden no estar disponibles
)

echo.
echo ========================================
echo    ✅ Configuración completada
echo ========================================
echo.
echo Para ejecutar Coach AI v2:
echo   run.bat
echo.
echo Para activar el entorno virtual manualmente:
echo   activate.bat
echo.
echo Para más ayuda:
echo   help.bat
echo.
pause
