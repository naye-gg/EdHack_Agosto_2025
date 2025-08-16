@echo off
REM Script de activación rápida para Windows

echo.
echo 🚀 Activando entorno virtual Coach AI v2...

REM Verificar que existe el entorno virtual
if not exist "venv\" (
    echo ❌ Entorno virtual no encontrado
    echo.
    echo Ejecuta primero: setup.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar activación
if defined VIRTUAL_ENV (
    echo ✅ Entorno virtual activado
    echo 📍 Ubicación: %VIRTUAL_ENV%
    echo.
    
    REM Mostrar versión de Python
    echo 🐍 Python:
    python --version
    echo.
    
    REM Mostrar comandos útiles
    echo 💡 Comandos útiles:
    echo   streamlit run app.py          - Iniciar aplicación
    echo   python verify_installation.py - Verificar instalación
    echo   deactivate                    - Desactivar entorno virtual
    echo   help.bat                      - Ver más comandos
    echo.
    
    REM Cambiar prompt para mostrar que está activado
    cmd /k "prompt (coach-ai-v2) $P$G"
) else (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)
