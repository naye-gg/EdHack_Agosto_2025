@echo off
REM Script de actualización para Windows

echo.
echo ==========================================
echo    Coach AI v2 - Actualización Windows
echo ==========================================
echo.

REM Verificar entorno virtual
if not exist "venv\" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta primero: setup.bat
    pause
    exit /b 1
)

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ Error actualizando pip
)

echo 📦 Actualizando dependencias principales...

REM Verificar versión de Python para elegir requirements
python -c "import sys; exit(0 if sys.version_info < (3,13) else 1)" >nul 2>&1
if errorlevel 1 (
    echo 📦 Actualizando para Python 3.13+ (funcionalidad limitada)...
    pip install --upgrade -r requirements-python313.txt
) else (
    echo 📦 Actualizando dependencias completas...
    pip install --upgrade -r requirements.txt
)

if errorlevel 1 (
    echo ❌ Error actualizando dependencias
    echo.
    echo Soluciones:
    echo 1. Verificar conexión a internet
    echo 2. Ejecutar como administrador
    echo 3. Recrear entorno virtual con setup.bat
    pause
    exit /b 1
)

echo 🔍 Verificando instalación actualizada...
python verify_installation.py

echo.
echo ========================================
echo    ✅ Actualización completada
echo ========================================
echo.
echo Para ejecutar: run.bat
echo Para verificar: verify.bat
echo.
pause
